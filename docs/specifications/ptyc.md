# Phân tích yêu cầu và đặc tả kỹ thuật sSMC-FCM

Tài liệu này đặc tả việc hiện thực thuật toán sSMC-FCM dựa trên ba bài báo trong workspace. Phạm vi hiện tại chỉ gồm phân tích, thiết kế, lập kế hoạch kiểm thử và đối chiếu khoa học; chưa viết mã thuật toán.

**Rà soát gần nhất: 29/09/2026.** Nội dung đã được đối chiếu với báo cáo tiến độ tuần 1 và vẫn giữ nguyên nguyên tắc: tái lập ví dụ của bài báo trước khi mở rộng sang dữ liệu mới. Bài báo 2021 ký hiệu hệ số giám sát là $M'$. Slide báo cáo dùng $M_0$ để dễ đọc; hai ký hiệu này chỉ cùng một đại lượng. API Python tiếp tục dùng tên `M_prime`.

## 1. Phát biểu bài toán

Cần phân cụm tập dữ liệu số $X$ khi chỉ một phần mẫu có thông tin giám sát. Kết quả chính gồm:

- ma trận độ thuộc mờ $U$;
- tập tâm cụm $V$;
- nhãn cứng suy ra bằng argmax theo từng hàng của $U$;
- lịch sử hội tụ và các chẩn đoán số học.

sSMC-FCM đưa thông tin giám sát vào FCM bằng cách gán hệ số mờ hóa lớn hơn $M'$ (hay $M_0$ trên slide) cho cặp (mẫu được giám sát, cụm đích), trong khi các cặp còn lại dùng $M$. Đây là khác biệt cốt lõi so với sSFCM: sSFCM đưa ma trận độ thuộc giám sát $\bar U$ trực tiếp vào hàm mục tiêu, còn sSMC-FCM thay đổi số mũ $m_{ik}$.

Phạm vi hiện thực sau này:

- FCM làm baseline;
- sSFCM làm baseline bán giám sát;
- sSMC-FCM theo các Phương trình (7)-(20);
- đánh giá bằng ví dụ số trong bài báo và các chỉ số hợp lệ;
- không tự thêm biến thể hoặc công thức ngoài nguồn.

## 2. Kiến thức nền

### 2.1 K-Means

K-Means gán mỗi mẫu vào đúng một cụm và cập nhật tâm bằng trung bình các mẫu đã gán. Kết quả là phân hoạch cứng. Trong bộ tài liệu này, K-Means chỉ xuất hiện trong bài tổng quan chỉ số đánh giá như một thuật toán sinh phân hoạch; không phải thuật toán đích.

### 2.2 Fuzzy C-Means

Fuzzy C-Means cho phép một mẫu có độ thuộc ở nhiều cụm. Mỗi hàng của $U$ nằm trên simplex:

$$
0 \le U_{ik} \le 1,\qquad \sum_{k=1}^{C}U_{ik}=1.
$$

Hệ số mờ hóa $m>1$ điều khiển độ mờ. FCM tối ưu luân phiên ma trận độ thuộc và tâm cụm.

### 2.3 Phân cụm mờ bán giám sát và sSFCM

Bài báo sSFCM cho trước một số độ thuộc $\bar U$. Phần độ thuộc còn lại được phân bổ theo khoảng cách; hàm mục tiêu dùng $|U-\bar U|^m$. Bài báo còn trình bày eSFCM, nhưng eSFCM không thuộc phạm vi baseline bắt buộc.

### 2.4 Động lực của sSMC-FCM

sSMC-FCM không thêm $\bar U$ vào hàm mục tiêu. Mỗi cặp mẫu-cụm có thể có hệ số mờ hóa $m_{ik}$. Với mẫu được giám sát vào cụm $k$, bài báo đặt $m_{ik}=M'>M$; các cụm khác vẫn dùng $M$. Proposition 2 lập luận rằng tăng $M'$ làm tăng độ thuộc vào cụm đích trong điều kiện của bài báo.

## 3. Ánh xạ bài báo

| Tệp | Tên bài báo | Vai trò |
|---|---|---|
| papers/pdf/FCM Bán giám sát - yasunori2009.pdf | *On Semi-Supervised Fuzzy c-Means Clustering* - Endo, Hamasuna, Yamashiro, Miyamoto (FUZZ-IEEE 2009) | Định nghĩa sSFCM và eSFCM; sSFCM là baseline bán giám sát |
| papers/pdf/algorithms-14-00258-v2.pdf | *A Novel Semi-Supervised Fuzzy C-Means Clustering Algorithm Using Multiple Fuzzification Coefficients* - Khang, Tran, Fowler (Algorithms 2021, 14, 258) | Bài báo đích; định nghĩa sSMC-FCM |
| papers/pdf/Relative Clustering Validity Criteria A Comparative Overview 2010.pdf | *Relative Clustering Validity Criteria: A Comparative Overview* - Vendramin, Campello, Hruschka (2010) | Tổng quan 40 tiêu chuẩn tương đối và 3 chỉ số ngoại tại cho phân hoạch cứng |

Các bản văn bản được trích xuất trực tiếp từ text layer, không OCR, nằm trong papers/text/.

## 4. Ký hiệu toán học

Tài liệu chuẩn hóa dữ liệu theo chiều mẫu để phù hợp NumPy. Bài báo sSFCM gốc dùng $x_k$ cho mẫu và $C_i$ cho cụm; khi sang mã nguồn, ánh xạ là k_paper thành i_code và i_paper thành k_code.

| Ký hiệu | Ý nghĩa | Biểu diễn trong mã |
|---|---|---|
| $N$ | Số mẫu | int |
| $D$ | Số chiều/thuộc tính | int |
| $C$ | Số cụm | int |
| $X_i$ | Mẫu thứ $i$ | X[i], shape (D,) |
| $X$ | Tập dữ liệu | float ndarray, shape (N,D) |
| $V_k$ | Tâm cụm $k$ | centers[k], shape (D,) |
| $V$ | Toàn bộ tâm cụm | float ndarray, shape (C,D) |
| $D_{ik}$ | Khoảng cách Euclid $\lVert X_i-V_k\rVert$ | dist[i,k], shape (N,C) |
| $Q_{ik}$ | Bình phương khoảng cách $D_{ik}^2$ | dist_sq[i,k], shape (N,C); $Q$ là quy ước mã nguồn |
| $U_{ik}$ | Độ thuộc của mẫu $i$ trong cụm $k$ | membership[i,k] |
| $U$ | Ma trận độ thuộc | float ndarray, shape (N,C) |
| $\bar U_{ik}$ | Độ thuộc giám sát của sSFCM | supervision[i,k], shape (N,C) |
| $m$ | Hệ số mờ hóa chung của FCM/sSFCM | float > 1; sSFCM còn có nhánh $m=1$ |
| $m_{ik}$ | Hệ số mờ hóa theo cặp của sSMC-FCM | exponents[i,k], shape (N,C) |
| $M$ | Hệ số mờ hóa cơ sở | float > 1 |
| $M'$ / $M_0$ | Hệ số của cặp mẫu-cụm được giám sát; $M'$ là ký hiệu paper, $M_0$ là ký hiệu slide | `M_prime`, float, yêu cầu $M'>M$ |
| $Y$ | Tập cặp $(i,k)$ được giám sát | target_cluster, shape (N,), -1 nếu không nhãn |
| $S$ | Số mẫu được giám sát | sum(target_cluster >= 0) |
| $d_{\min}$ | $\min_jD_{ij}$ cho một mẫu giám sát | scalar |
| $d_{ij}$ | Khoảng cách chuẩn hóa $D_{ij}/d_{\min}$ | vector shape (C,) |
| $\mu_{ij}$ | Biến phụ trước chuẩn hóa | vector shape (C,) |
| $\alpha$ | Mức độ thuộc đích mong muốn | float trong (0,1) |
| $\varepsilon$ | Ngưỡng dừng | float > 0 |
| $l$ | Chỉ số vòng lặp | int |

Các bất biến:

- U.shape = (N,C), V.shape = (C,D), m_ik.shape = (N,C);
- mọi giá trị hữu hạn, $U\ge0$, tổng mỗi hàng của $U$ xấp xỉ 1;
- mỗi cụm có tổng độ thuộc dương;
- target_cluster[i] bằng -1 hoặc thuộc [0,C).

## 5. Công thức sSFCM

Nguồn chính: bài báo sSFCM, Section II-B, PDF trang 2-3, Eqs. (1)-(8). Bài sSMC-FCM Section 2.2 viết lại cùng thuật toán bằng ký hiệu mẫu-trước, Eqs. (4)-(6).

### 5.1 Thông tin giám sát

$$
\bar U_{ik}\in[0,1],\qquad \sum_{k=1}^{C}\bar U_{ik}\le1.
$$

Nếu không có giám sát cho cặp $(i,k)$, $\bar U_{ik}=0$. Khối lượng còn lại là $r_i=1-\sum_k\bar U_{ik}$.

### 5.2 Hàm mục tiêu - Eq. (2)

$$
J(U,V)=\sum_{i=1}^{N}\sum_{k=1}^{C}
|U_{ik}-\bar U_{ik}|^m\lVert X_i-V_k\rVert^2.
$$

Ràng buộc: $\sum_kU_{ik}=1$, $U_{ik}\in[0,1]$. Nghiệm Eq. (6) bảo đảm $U_{ik}\ge\bar U_{ik}$ khi đầu vào hợp lệ.

### 5.3 Cập nhật tâm - Eq. (4)

$$
V_k=
\frac{\sum_i|U_{ik}-\bar U_{ik}|^mX_i}
     {\sum_i|U_{ik}-\bar U_{ik}|^m}.
$$

Ánh xạ mã: update_ssfcm_centers(X, U, U_bar, m).

### 5.4 Cập nhật độ thuộc

Với $m>1$, Eq. (6):

$$
U_{ik}=\bar U_{ik}
+\left(1-\sum_j\bar U_{ij}\right)
\frac{(1/Q_{ik})^{1/(m-1)}}
     {\sum_j(1/Q_{ij})^{1/(m-1)}}.
$$

Với $m=1$, Eq. (8) gán toàn bộ phần dư $r_i$ cho cụm gần nhất và giữ các phần tử còn lại bằng $\bar U$. Bài báo không quy định cách phá hòa khi nhiều tâm cùng khoảng cách.

Benchmark tuần 1 dùng $m=2$, vì vậy nhánh $m=1$ là phần bổ sung sau MVP và không chặn việc tái lập Table II.

### 5.5 Luồng thuật toán

1. Nhận $\bar U$, khởi tạo $V$.
2. Cố định $V$, cập nhật $U$ bằng Eq. (6) hoặc Eq. (8).
3. Cố định $U$, cập nhật $V$ bằng Eq. (4).
4. Dừng khi thỏa điều kiện dừng.

Bài gốc chỉ ghi “stop criterion”. Bài sSMC-FCM khi tóm tắt sSFCM dùng $\lVert V^{(l)}-V^{(l+1)}\rVert<\varepsilon$.

Rủi ro số học:

- $Q_{ik}=0$ làm biểu thức $1/Q_{ik}$ suy biến;
- mẫu số cập nhật tâm có thể bằng 0;
- phải kiểm tra $\sum_k\bar U_{ik}\le1+\mathrm{tol}$.

## 6. Công thức sSMC-FCM

Nguồn chính: bài sSMC-FCM, Section 3, PDF trang 5-9.

### 6.1 Ma trận số mũ và giám sát - Eq. (8)

Với mẫu không được giám sát, $m_{ij}=M$ cho mọi $j$. Với mẫu $i$ được giám sát vào cụm $k$:

$$
m_{ij}=
\begin{cases}
M' & (i,j)\in Y,\\
M  & \text{các trường hợp còn lại}.
\end{cases}
$$

Baseline trung thành với bài báo dùng một $M'$ chung. Dùng $M'_i$ riêng hoặc nhiều cụm đích cho một mẫu là phần mở rộng.

### 6.2 Hàm mục tiêu - Eq. (7)

$$
J(U,V)=\sum_{i=1}^{N}\sum_{k=1}^{C}U_{ik}^{m_{ik}}D_{ik}^{2}.
$$

Ràng buộc:

- $0\le U_{ik}\le1$;
- $\sum_kU_{ik}=1$ với mọi $i$;
- $\sum_iU_{ik}>0$ với mọi $k$;
- $m_{ik}>1$.

### 6.3 Cập nhật tâm - Eq. (10)

$$
V_k=
\frac{\sum_{i=1}^{N}U_{ik}^{m_{ik}}X_i}
     {\sum_{i=1}^{N}U_{ik}^{m_{ik}}}.
$$

weights = U ** exponents có shape (N,C); tử số (C,D); mẫu số (C,). Nếu mẫu số bằng 0, bài báo không đưa quy tắc khởi tạo lại.

### 6.4 Độ thuộc của mẫu không giám sát - Eq. (15)

$$
U_{ik}=
\left[
\sum_{j=1}^{C}
\left(\frac{D_{ik}}{D_{ij}}\right)^{2/(M-1)}
\right]^{-1}.
$$

Đây là cập nhật FCM chuẩn với hệ số $M$. Nên tính bằng chuẩn hóa hoặc log-domain khi số mũ lớn. Trường hợp $D_{ij}=0$ không được bài báo xử lý.

### 6.5 Độ thuộc của mẫu được giám sát - Eqs. (17)-(20)

Với mẫu $i$ được giám sát vào cụm $k$:

1. Eq. (17):

$$
d_{\min}=\min_jD_{ij},\qquad d_{ij}=D_{ij}/d_{\min}.
$$

2. Eq. (18), với $j\ne k$:

$$
\mu_{ij}=
\left(\frac{1}{Md_{ij}^{2}}\right)^{1/(M-1)}.
$$

3. Eq. (19), đặt $A=\sum_{j\ne k}\mu_{ij}$ và $b=(M'-M)/(M'-1)$, giải $\mu_{ik}>0$:

$$
\frac{\mu_{ik}}{(\mu_{ik}+A)^b}
=
\left(\frac{1}{M'd_{ik}^{2}}\right)^{1/(M'-1)}.
$$

4. Eq. (20):

$$
U_{ij}=\frac{\mu_{ij}}{\sum_{l=1}^{C}\mu_{il}}.
$$

Bài báo chứng minh vế trái Eq. (19) tăng đơn điệu theo $\mu_{ik}>0$ khi $M'>M$, nhưng chỉ đề nghị bắt đầu từ 0 rồi tăng dần; không cho bước tăng, tolerance, cận trên hoặc solver cụ thể.

Ánh xạ hàm:

- normalize_supervised_distances - Eq. (17);
- compute_non_target_mu - Eq. (18);
- solve_target_mu - Eq. (19);
- normalize_mu - Eq. (20).

Đề xuất kỹ thuật: chia đôi với cận trên mở rộng động và dừng theo residual Eq. (19). Đây là quyết định hiện thực, không phải chỉ dẫn của bài báo.

### 6.6 Chọn $M'$ theo độ thuộc mong muốn - Eq. (23)

Gọi $U'_{ik}$ là độ thuộc không giám sát từ Eq. (15). Proposition 3 cho điều kiện đủ để $U_{ik}\ge\alpha$:

$$
M'\alpha^{M'-1}
\le
M\left(
\frac{1-\alpha}{1/U'_{ik}-1}
\right)^{M-1}.
$$

Bài báo đề nghị bắt đầu $M'=M$, tăng $M'$ và kiểm tra. Ví dụ: $M=2$, $U'_{91}=0.189$, $\alpha=0.5$, kết quả $M'=5.582$.

API baseline nên nhận $M'$ từ người dùng cho đến khi giải quyết các điểm chưa rõ ở Section 12.

### 6.7 Khởi tạo, lặp, hội tụ và đầu ra

1. Nhận $X,C,M,M',Y,\varepsilon$; khởi tạo $V$.
2. Cập nhật $U$: Eq. (15) cho mẫu không giám sát; Eqs. (17)-(20) cho mẫu giám sát.
3. Tạo $m_{ik}$ bằng Eq. (8), cập nhật $V$ bằng Eq. (10).
4. Dừng nếu $\lVert V^{(l)}-V^{(l+1)}\rVert<\varepsilon$.
5. Trả phân hoạch; API lưu thêm $U,V$, nhãn, objective history và số vòng.

Bài báo không chỉ rõ norm, cách khởi tạo $V$, max iterations hay random seed.

### 6.8 Độ phức tạp

Bài báo không công bố Big-O cho sSMC-FCM. Ước lượng kỹ thuật mỗi vòng:

| Thành phần | Độ phức tạp |
|---|---|
| Khoảng cách và cập nhật tâm | O(N*C*D) |
| Độ thuộc không giám sát | O((N-S)*C) |
| Độ thuộc giám sát | O(S*C + S*I_mu) |
| Bộ nhớ | O(N*C + C*D) |

$I_\mu$ là số vòng của solver Eq. (19).

## 7. So sánh FCM, sSFCM và sSMC-FCM

| Thành phần | FCM | sSFCM | sSMC-FCM |
|---|---|---|---|
| Đầu vào | $X,C,m,\varepsilon,V_0$ | Thêm $\bar U$ | Thêm $Y,M,M'$ |
| Giám sát | Không | Độ thuộc cho trước | Mã hóa bằng hệ số mờ hóa |
| Membership | $U$, tổng hàng bằng 1 | $U\ge\bar U$ | Hàng giám sát cần giải Eq. (19) |
| Fuzzifier | Một $m$ | Một $m$ | Ma trận $m_{ik}$ |
| Objective | $\sum U^mD^2$ | $\sum|U-\bar U|^mD^2$ | $\sum U^{m_{ik}}D^2$ |
| Tâm cụm | Trọng số $U^m$ | Trọng số $|U-\bar U|^m$ | Trọng số $U^{m_{ik}}$ |
| Độ thuộc | Tỷ số khoảng cách | $\bar U$ cộng phần dư | Eq. (15) hoặc Eqs. (17)-(20) |
| Mẫu có nhãn | Không | Độ thuộc tối thiểu | Tăng số mũ tại cụm đích |
| Siêu tham số | $C,m,\varepsilon$ | Thêm $\bar U$ | $C,M,M',Y,\varepsilon$, tolerance solver |
| Điều kiện dừng | Delta tâm | Bài gốc không chỉ rõ | Delta tâm; norm không chỉ rõ |
| Đầu ra | Phân hoạch, $U,V$ | Phân hoạch, $U,V$ | Phân hoạch, $U,V$ |

Thay đổi mã:

- FCM -> sSFCM: thêm $\bar U$, đổi cập nhật độ thuộc, trọng số tâm và objective.
- FCM -> sSMC-FCM: thay fuzzifier scalar bằng $m_{ik}$, tách mẫu có/không giám sát, thêm solver Eq. (19).
- sSFCM -> sSMC-FCM: bỏ $\bar U$ khỏi objective; giám sát chuyển thành hệ số $M'$.

## 8. Thiết kế phần mềm

### 8.1 Cấu trúc dự kiến

    src/
      fcm.py
      ssfcm.py
      ssmc_fcm.py
      distances.py
      supervision.py
      metrics.py
      data.py
      validation.py
    tests/
      test_fcm.py
      test_ssfcm.py
      test_ssmc_equations.py
      test_ssmc_fcm.py
      test_metrics.py
      test_paper_reproduction.py

### 8.2 Module và hàm

| Hàm | Trách nhiệm | Vào -> ra | Tham chiếu |
|---|---|---|---|
| pairwise_euclidean | Tính $D,Q$ | (N,D),(C,D) -> (N,C) | $D_{ik}$ |
| validate_X | Kiểm tra shape, finite | X -> lỗi/None | Tiền điều kiện |
| validate_supervision | Kiểm tra một đích/mẫu | (N,),C -> mask | Eq. (8) |
| fcm.update_membership | Độ thuộc FCM | D,M -> U | Eq. (15) |
| fcm.update_centers | Tâm FCM | X,U,M -> V | FCM Eq. (3) |
| ssfcm.update_membership | Độ thuộc sSFCM | Q,U_bar,m -> U | Eq. (6)/(8) |
| build_exponents | Tạo $m_{ik}$ | targets,C,M,M' -> (N,C) | Eq. (8) |
| solve_target_mu | Giải nghiệm scalar | scalar -> $\mu_{ik}$ | Eq. (19) |
| ssmc.update_membership | Điều phối hai loại mẫu | D,targets,M,M' -> U | Eqs. (15),(17)-(20) |
| ssmc.update_centers | Cập nhật tâm | X,U,m_ik -> V | Eq. (10) |
| ssmc.objective | Objective | U,Q,m_ik -> scalar | Eq. (7) |
| select_m_prime | Tìm $M'$ theo $\alpha$ | scalar -> scalar | Eq. (23), tùy chọn |
| metrics.* | Chỉ số phân hoạch cứng | X,labels[,truth] -> scalar | Bài validity |
| paper_toy_dataset | Dữ liệu Table 1 | none -> (20,2) | Hai bài thuật toán |

### 8.3 API chính

    model = SSMCFCM(
        n_clusters=C,
        base_fuzzifier=M,
        supervised_fuzzifier=M_prime,
        tol=epsilon,
        max_iter=max_iter,
        random_state=seed,
        mu_solver_tol=mu_tol,
    )
    model.fit(X, supervised_targets=target_cluster, initial_centers=V0)

    U = model.membership_
    V = model.cluster_centers_
    labels = model.labels_
    history = model.objective_history_

predict(X_new) chỉ dùng Eq. (15) với tâm đã fit. Dự đoán có thêm giám sát nên là API riêng.

## 9. Thuật toán hiện thực

    Kiểm tra X, C, M > 1, M' > M, epsilon và target_cluster
    Khởi tạo V với shape (C,D)
    Tạo m_ik theo Eq. (8)

    Lặp tối đa max_iter:
        D = pairwise_euclidean(X, V)
        Với từng mẫu i:
            Nếu không giám sát:
                U[i] = Eq. (15)
            Nếu giám sát vào cụm k:
                d = D[i] / min(D[i])      # Eq. (17)
                mu[j != k] = Eq. (18)
                mu[k] = giải Eq. (19)
                U[i] = mu / sum(mu)       # Eq. (20)
        V_new = Eq. (10)
        delta = norm(V_new - V)
        Tính lại khoảng cách từ X đến V_new
        objective = Eq. (7) trên cặp (U, V_new)
        ghi chẩn đoán
        V = V_new
        nếu delta < epsilon: dừng

    Nếu hết max_iter: converged_ = False
    labels = argmax(U, axis=1)

Quy ước hiện tại là ghi objective trên $(U,V_{\mathrm{new}})$. Nếu mã sau này chọn quy ước khác thì phải đổi đồng bộ tài liệu, test và logging; không trộn hai trạng thái trong cùng history. Khi dừng, model phải lưu $V_{\mathrm{new}}$, không giữ nhầm tâm của vòng trước.

## 10. Kế hoạch đánh giá

### 10.1 Phạm vi bài validity

Bài validity chỉ đánh giá phân hoạch cứng. Để áp dụng cho sSMC-FCM phải dùng labels = argmax(U). Bài báo không đưa chỉ số đánh giá trực tiếp membership mờ.

### 10.2 Các chỉ số tương đối kiểu tối ưu

| Chỉ số | Công thức/nguồn | Miền, chiều tốt |
|---|---|---|
| Calinski-Harabasz/VRC | tr(B)/tr(W) * (N-k)/(k-1), Eq. (1) | [0,+inf), cao |
| Davies-Bouldin | Eq. (9) | [0,+inf), thấp |
| Dunn family | min(delta)/max(Delta), Eq. (10) | [0,+inf), cao |
| SWC | (b-a)/max(a,b), Eqs. (18)-(19) | [-1,1], cao |
| ASWC | b/(a+epsilon), Eq. (20) | [0,+inf), cao |
| SSWC | SWC dùng khoảng cách đến tâm | [-1,1], cao |
| ASSWC | ASWC dùng khoảng cách đến tâm | [0,+inf), cao |
| PBM | (E1*DK/(k*EK))^2, Eq. (21) | [0,+inf), cao |
| C-index | Eqs. (22)-(23) | [0,1], thấp |
| Gamma | Eq. (24) | [-1,1], cao |
| G(+) | Eq. (27) | [0,1], thấp |
| Tau | Eqs. (28)-(29) | [-1,1], cao |
| Point-biserial | Eq. (30) | thường [-1,1], cao |
| C/sqrt(k) | Eqs. (31)-(34) | [0,1] khi hợp lệ, cao |

Họ Dunn có 18 cách kết hợp: 6 định nghĩa khoảng cách giữa cụm với 3 định nghĩa đường kính cụm, gồm Dunn gốc và 17 biến thể.

### 10.3 Các chỉ số dạng sai khác

Bài báo biến đổi chuỗi chỉ số bằng Eq. (37):

$$
C_{new}(k)=
\left|
\frac{C_{orig}(k-1)-C_{orig}(k)}
     {C_{orig}(k)-C_{orig}(k+1)}
\right|.
$$

Chín chỉ số gồm trace(W), trace(CovW), trace(W^-1 B), |T|/|W|, Nlog(|T|/|W|), k^2|W|, log(SSB/SSW), Ball-Hall và McClain-Rao. Các công thức nghịch đảo/định thức có rủi ro suy biến.

### 10.4 Chỉ số ngoại tại

| Chỉ số | Công thức | Miền, chiều tốt |
|---|---|---|
| Rand Index | (a+d)/(a+b+c+d), Eq. (51) | [0,1], cao |
| Adjusted Rand Index | Eq. (52) | kỳ vọng 0 khi ngẫu nhiên, 1 khi hoàn hảo; có thể âm |
| Jaccard | a/(a+b+c), Eq. (53) | [0,1], cao |

Bài validity dùng ARI và Jaccard làm tham chiếu ngoại tại. Pearson và WGK đo tương quan giữa các chuỗi score. Accuracy và NMI không được ba bài báo định nghĩa.

### 10.5 Bộ chỉ số tối thiểu đã chốt cho giai đoạn đầu

- Kiểm chứng trực tiếp: membership Table 3, tâm cụm, số vòng.
- Có ground truth: ARI và Jaccard.
- Không ground truth: SWC/SSWC và VRC.
- Chẩn đoán: objective, delta tâm, simplex residual và residual Eq. (19).

PBM vẫn thuộc phạm vi paper và có thể bổ sung sau MVP, nhưng không nằm trong bộ chỉ số bắt buộc của báo cáo tuần 1. FPC, Xie-Beni, NMI và Purity không được gán cho paper validity này.

### 10.6 Dữ liệu và thí nghiệm

1. Bộ 20 điểm trong sSFCM Table I / sSMC-FCM Table 1, C=2, khoảng cách Euclid.
2. FCM: M=2, không giám sát.
3. sSFCM: m=2, mức giám sát 0.3 hoặc 0.6 cho mẫu 9 và 10 vào cụm 1.
4. sSMC-FCM: M=2, M'=4 hoặc 8 cho cùng hai mẫu.
5. Bài sSMC-FCM báo epsilon = 1e-3, khoảng 10 vòng và các tâm:
   - không giám sát: (2.719,5.000), (9.018,5.000);
   - M'=4: (2.735,5.000), (9.200,5.000);
   - M'=8: (2.714,5.000), (9.303,5.000).
6. Dùng synthetic blobs có seed để kiểm tra độ ổn định.

Bảng acceptance tối thiểu cho điểm 9 và 10:

| Phương pháp | Mức giám sát | $U_{C1}$ | $U_{C2}$ | Cụm cứng |
|---|---:|---:|---:|---|
| FCM | không | 0.19 | 0.81 | C2 |
| sSFCM | $\bar u_{i1}=0.3$ | 0.45 | 0.55 | C2 |
| sSFCM | $\bar u_{i1}=0.6$ | 0.69 | 0.31 | C1 |
| sSMC-FCM | $M=2, M'=4$ | 0.43 | 0.57 | C2 |
| sSMC-FCM | $M=2, M'=8$ | 0.60 | 0.40 | C1 |

Bảng này là kiểm tra hành vi và tái lập số liệu, không phải bằng chứng rằng sSMC-FCM tốt hơn sSFCM trên mọi dữ liệu.

## 11. Chiến lược kiểm chứng

### 11.1 Kiểm tra toán học

- Shape của mọi hàm đúng.
- $U$ hữu hạn, không âm, tổng hàng xấp xỉ 1.
- $m_{ik}=M$ ngoài target; $m_{i,target}=M'$.
- Eq. (15) trùng FCM khi mọi mẫu không giám sát.
- Residual Eq. (19) nhỏ hơn tolerance.
- Eq. (20) chuẩn hóa đúng.
- Eq. (10) trùng weighted mean tham chiếu.
- Hoán vị cụm không đổi objective nếu $Y$ được hoán vị tương ứng.

### 11.2 Hội tụ và ổn định số

- Ghi objective, delta tâm và residual solver mỗi vòng.
- Dừng đúng tiêu chuẩn và không vượt max_iter.
- Không NaN/Inf trên dữ liệu hợp lệ.
- Kiểm thử zero distance, tâm trùng, cụm rỗng và $M$ gần 1.
- Kiểm tra objective không tăng như một kiểm thử thực nghiệm; bài báo không đưa định lý riêng về tính giảm đơn điệu.

### 11.3 Tính xác định

- Cùng seed và cấu hình phải cho cùng $U,V$, nhãn và lịch sử.
- Reproduction test nên dùng tâm khởi tạo cố định. Bài báo không công bố initialization.

### 11.4 Tái lập bài báo

- So Table II sSFCM đến 2 chữ số sau khi căn chỉnh hoán vị nhãn.
- So Table 3 sSMC-FCM đến 2 chữ số.
- So tâm đến 3 chữ số.
- sSFCM, mẫu 9 và 10: độ thuộc cụm 1 tăng xấp xỉ 0.19 -> 0.45 -> 0.69 khi $\bar u_{i1}=0,0.3,0.6$.
- sSMC-FCM, mẫu 9 và 10: độ thuộc cụm 1 tăng xấp xỉ 0.19 -> 0.43 -> 0.60 khi $M'=2,4,8$.
- Ví dụ Eq. (23): M'=5.582 với M=2, alpha=0.5, U'=0.189.
- “Khoảng 10 vòng” chỉ là kiểm tra mềm vì thiếu initialization và norm.

### 11.5 So sánh baseline

- Khi mọi mẫu không nhãn và exponent bằng $M$, component sSMC phải trùng FCM.
- sSFCM và sSMC-FCM phải thể hiện xu hướng trong bài báo nhưng không cần cùng ma trận $U$.
- RI/ARI/Jaccard bất biến với hoán vị tên nhãn.

## 12. Câu hỏi mở và điểm chưa rõ

1. **Khởi tạo chưa rõ.** [CẦN XÁC MINH] Section 3.1, Step 1, PDF trang 6 không cho phương pháp, seed hoặc giá trị dùng trong Table 3.
2. **Norm dừng chưa rõ.** [CẦN XÁC MINH] Step 4, PDF trang 7 không nói dùng Frobenius, max-row hay norm khác.
3. **Solver Eq. (19) thiếu chi tiết.** [CẦN XÁC MINH] PDF trang 9 không cho bước tăng, tolerance, cận hoặc số vòng tối đa.
4. **Khoảng cách bằng 0.** [CẦN XÁC MINH] Eqs. (15),(17)-(19) suy biến nếu $D_{ij}=0$.
5. **Cụm rỗng.** [CẦN XÁC MINH] Mẫu số Eq. (10) có thể bằng 0; không có policy khởi tạo lại.
6. **Nhiều target cho một mẫu.** [CẦN XÁC MINH] Eq. (8) dùng tập cặp $Y$, nhưng Eqs. (16)-(20) chỉ suy dẫn cho một cụm đích.
7. **$M'$ chung hay theo mẫu.** Algorithm và ví dụ dùng một $M'$ chung; dùng riêng theo mẫu là phần mở rộng.
8. **Tính đơn điệu khi tìm $M'$.** [CẦN XÁC MINH] Mệnh đề $M'\alpha^{M'-1}$ giảm khi $M'$ tăng không đúng vô điều kiện cho mọi $\alpha\in(0,1)$; đạo hàm log có dấu của $1/M'+\ln\alpha$.
9. **Khẳng định hội tụ.** Ba proposition không tạo thành một định lý riêng chứng minh objective giảm qua toàn bộ vòng lặp.
10. **Điều kiện dừng sSFCM.** Bài gốc chỉ ghi “stop criterion”; bài sSMC-FCM mới dùng delta tâm.
11. **Tái lập chính xác.** Table 3 làm tròn hai chữ số và không có tâm khởi tạo.
12. **Chỉ số mờ.** Bài validity xem chỉ số cho fuzzy partition là hướng nghiên cứu tiếp theo; không có công thức fuzzy validity trong ba nguồn.

