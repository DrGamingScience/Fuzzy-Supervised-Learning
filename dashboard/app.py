"""Interactive Streamlit dashboard for FCM, sSFCM, and sSMC-FCM."""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from fuzzy_supervised_learning.dashboard_support import (
    fit_dashboard_models,
    generate_demo_data,
    maximum_solver_residual,
    project_to_2d,
)


st.set_page_config(
    page_title="Fuzzy Clustering Lab",
    page_icon="◉",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem;}
    [data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,.22);
        border-radius: 12px;
        padding: 12px 16px;
        background: rgba(128,128,128,.04);
    }
    .dashboard-subtitle {color: #777; margin-top: -.6rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Fuzzy Clustering Lab")
st.markdown(
    '<p class="dashboard-subtitle">Khám phá và so sánh FCM, sSFCM, sSMC-FCM trên cùng một tập dữ liệu.</p>',
    unsafe_allow_html=True,
)


with st.sidebar:
    st.header("Cấu hình")
    algorithm = st.selectbox(
        "Thuật toán",
        ("sSMC-FCM", "sSFCM", "FCM", "So sánh cả ba"),
    )
    data_source = st.radio("Nguồn dữ liệu", ("Dữ liệu mẫu", "Tải CSV"))
    n_clusters = st.slider("Số cụm", 2, 8, 3)
    seed = st.number_input("Random seed", min_value=0, value=42, step=1)

    if data_source == "Dữ liệu mẫu":
        n_samples = st.slider("Số mẫu", 30, 500, 150, step=10)
        cluster_std = st.slider("Độ phân tán", 0.1, 2.5, 0.7, step=0.1)
        X, demo_labels = generate_demo_data(
            n_samples, n_clusters, cluster_std, int(seed)
        )
        feature_names = ["x1", "x2"]
    else:
        upload = st.file_uploader("Tệp CSV", type=("csv",))
        if upload is None:
            st.info("Hãy tải một tệp CSV để tiếp tục.")
            st.stop()
        try:
            uploaded_frame = pd.read_csv(upload)
        except Exception as error:
            st.error(f"Không đọc được CSV: {error}")
            st.stop()
        numeric_columns = uploaded_frame.select_dtypes(include="number").columns.tolist()
        if not numeric_columns:
            st.error("CSV phải có ít nhất một cột số.")
            st.stop()
        feature_names = st.multiselect(
            "Cột đặc trưng",
            numeric_columns,
            default=numeric_columns[: min(4, len(numeric_columns))],
        )
        if not feature_names:
            st.warning("Chọn ít nhất một cột đặc trưng.")
            st.stop()
        clean_frame = uploaded_frame[feature_names].dropna()
        if len(clean_frame) < n_clusters:
            st.error("Số dòng hợp lệ phải lớn hơn hoặc bằng số cụm.")
            st.stop()
        X = clean_frame.to_numpy(dtype=np.float64)
        demo_labels = None

    st.divider()
    fuzzifier = st.slider("Hệ số mờ m / M", 1.1, 5.0, 2.0, step=0.1)
    if algorithm in ("sSMC-FCM", "So sánh cả ba"):
        supervised_fuzzifier = st.slider(
            "Hệ số giám sát M′",
            min_value=float(fuzzifier + 0.1),
            max_value=12.0,
            value=max(4.0, float(fuzzifier + 0.1)),
            step=0.1,
        )
    else:
        supervised_fuzzifier = max(4.0, float(fuzzifier + 0.1))
    if algorithm in ("sSFCM", "So sánh cả ba"):
        supervision_strength = st.slider(
            "Độ mạnh giám sát sSFCM", 0.0, 1.0, 0.6, step=0.05
        )
    else:
        supervision_strength = 0.6
    tol = st.select_slider(
        "Tolerance",
        options=(1e-3, 1e-4, 1e-5, 1e-6, 1e-7),
        value=1e-5,
        format_func=lambda value: f"{value:.0e}",
    )
    max_iter = st.number_input("Số vòng tối đa", 10, 2000, 300, step=10)


targets = np.full(X.shape[0], -1, dtype=np.int64)
uses_supervision = algorithm != "FCM"
if uses_supervision:
    with st.expander("Gán thông tin giám sát", expanded=True):
        st.caption(
            "Chọn mẫu và gán cụm đích. Chỉ số cụm trên giao diện bắt đầu từ 1."
        )
        label_options = list(range(X.shape[0]))
        default_samples: list[int] = []
        if demo_labels is not None:
            for cluster_index in range(n_clusters):
                candidates = np.flatnonzero(demo_labels == cluster_index)
                if candidates.size:
                    default_samples.append(int(candidates[0]))
        selected_samples = st.multiselect(
            "Mẫu được giám sát",
            label_options,
            default=default_samples,
            format_func=lambda index: "#{} · {}".format(
                index,
                ", ".join(
                    f"{feature_names[col]}={X[index, col]:.2f}"
                    for col in range(min(2, X.shape[1]))
                ),
            ),
        )
        if selected_samples:
            default_targets = (
                [int(demo_labels[index]) + 1 for index in selected_samples]
                if demo_labels is not None
                else [1] * len(selected_samples)
            )
            assignment_frame = pd.DataFrame(
                {
                    "sample": selected_samples,
                    "target_cluster": default_targets,
                }
            )
            edited_assignments = st.data_editor(
                assignment_frame,
                hide_index=True,
                disabled=("sample",),
                column_config={
                    "sample": st.column_config.NumberColumn("Mẫu", format="#%d"),
                    "target_cluster": st.column_config.NumberColumn(
                        "Cụm đích", min_value=1, max_value=n_clusters, step=1
                    ),
                },
                width="stretch",
                key="supervision_editor",
            )
            for row in edited_assignments.itertuples(index=False):
                targets[int(row.sample)] = int(row.target_cluster) - 1
        else:
            st.caption("Chưa có mẫu nào được giám sát.")


run_clicked = st.button(
    "Chạy thuật toán",
    type="primary",
    width="stretch",
)

if run_clicked:
    try:
        with st.spinner("Đang tối ưu các tâm cụm và membership..."):
            models = fit_dashboard_models(
                algorithm,
                X,
                targets,
                n_clusters=n_clusters,
                fuzzifier=float(fuzzifier),
                supervised_fuzzifier=float(supervised_fuzzifier),
                supervision_strength=float(supervision_strength),
                tol=float(tol),
                max_iter=int(max_iter),
                random_state=int(seed),
            )
        st.session_state["dashboard_result"] = {
            "models": models,
            "X": X.copy(),
            "targets": targets.copy(),
            "feature_names": tuple(feature_names),
            "n_clusters": n_clusters,
        }
    except Exception as error:
        st.error(f"Không thể chạy thuật toán: {error}")

result = st.session_state.get("dashboard_result")
if result is None:
    st.info("Cấu hình dữ liệu và nhấn **Chạy thuật toán** để xem kết quả.")
    st.stop()

models = result["models"]
result_X = result["X"]
result_targets = result["targets"]
result_feature_names = list(result["feature_names"])
result_n_clusters = int(result["n_clusters"])

if len(models) > 1:
    st.subheader("So sánh nhanh")
    comparison = pd.DataFrame(
        [
            {
                "Thuật toán": name,
                "Hội tụ": "Có" if model.converged_ else "Không",
                "Số vòng": model.n_iter_,
                "Objective cuối": model.objective_,
                "Delta tâm cuối": model.center_shift_history_[-1],
                "Residual Eq. (19)": maximum_solver_residual(model),
            }
            for name, model in models.items()
        ]
    )
    st.dataframe(comparison, hide_index=True, width="stretch")

tabs = st.tabs(list(models.keys()))
for tab, (name, model) in zip(tabs, models.items()):
    with tab:
        residual = maximum_solver_residual(model)
        metric_columns = st.columns(4)
        metric_columns[0].metric("Trạng thái", "Hội tụ" if model.converged_ else "Chưa hội tụ")
        metric_columns[1].metric("Số vòng", model.n_iter_)
        metric_columns[2].metric("Objective", f"{model.objective_:.6g}")
        metric_columns[3].metric(
            "Residual Eq. (19)", "—" if residual is None else f"{residual:.2e}"
        )

        cluster_tab, membership_tab, convergence_tab, data_tab = st.tabs(
            ("Phân cụm", "Membership", "Hội tụ", "Dữ liệu")
        )

        with cluster_tab:
            projected, projected_centers, axes = project_to_2d(
                result_X, model.cluster_centers_
            )
            point_frame = pd.DataFrame(
                {
                    axes[0]: projected[:, 0],
                    axes[1]: projected[:, 1],
                    "Cụm": [f"Cụm {value + 1}" for value in model.labels_],
                    "Kích thước": 45,
                    "Loại": "Mẫu",
                }
            )
            center_frame = pd.DataFrame(
                {
                    axes[0]: projected_centers[:, 0],
                    axes[1]: projected_centers[:, 1],
                    "Cụm": [
                        f"Cụm {value + 1}" for value in range(result_n_clusters)
                    ],
                    "Kích thước": 220,
                    "Loại": "Tâm",
                }
            )
            plot_frame = pd.concat((point_frame, center_frame), ignore_index=True)
            st.scatter_chart(
                plot_frame,
                x=axes[0],
                y=axes[1],
                color="Cụm",
                size="Kích thước",
                width="stretch",
            )
            if result_X.shape[1] > 2:
                st.caption("Biểu đồ dùng PCA hai chiều; thuật toán vẫn chạy trên toàn bộ đặc trưng.")

        with membership_tab:
            sample_index = st.number_input(
                "Xem chi tiết mẫu",
                min_value=0,
                max_value=result_X.shape[0] - 1,
                value=0,
                step=1,
                key=f"sample_{name}",
            )
            membership_columns = [
                f"membership_C{index + 1}" for index in range(result_n_clusters)
            ]
            membership_frame = pd.DataFrame(
                model.membership_, columns=membership_columns
            )
            membership_frame.insert(0, "sample", np.arange(result_X.shape[0]))
            membership_frame["predicted_cluster"] = model.labels_ + 1
            membership_frame["supervised_target"] = np.where(
                result_targets >= 0, result_targets + 1, np.nan
            )
            st.bar_chart(
                pd.Series(
                    model.membership_[int(sample_index)],
                    index=[
                        f"Cụm {index + 1}" for index in range(result_n_clusters)
                    ],
                    name="Membership",
                )
            )
            st.dataframe(membership_frame, hide_index=True, width="stretch")
            export_frame = pd.DataFrame(result_X, columns=result_feature_names)
            export_frame = pd.concat((export_frame, membership_frame), axis=1)
            st.download_button(
                "Tải kết quả CSV",
                data=export_frame.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"{name.lower().replace(' ', '_')}_results.csv",
                mime="text/csv",
                key=f"download_{name}",
            )

        with convergence_tab:
            history = pd.DataFrame(
                {
                    "Vòng": np.arange(1, model.n_iter_ + 1),
                    "Objective": model.objective_history_,
                    "Delta tâm": model.center_shift_history_,
                }
            ).set_index("Vòng")
            left, right = st.columns(2)
            left.line_chart(history[["Objective"]])
            right.line_chart(history[["Delta tâm"]])
            st.dataframe(history, width="stretch")

        with data_tab:
            data_frame = pd.DataFrame(result_X, columns=result_feature_names)
            data_frame.insert(0, "sample", np.arange(result_X.shape[0]))
            data_frame["supervised_target"] = np.where(
                result_targets >= 0, result_targets + 1, np.nan
            )
            st.dataframe(data_frame, hide_index=True, width="stretch")
