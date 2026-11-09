# Bắt đầu nhanh cho mỗi session

Đọc file này → **Trạng thái Đã xác minh Hiện tại** đầu `progress.md` → feature trong `feature_list.json`.
Chỉ đọc sâu `docs/` khi công việc cần công thức hoặc chi tiết yêu cầu.
Quy trình chi tiết và Definition of Done: `docs/WORKFLOW.md`; giữ AGENTS dưới 100 dòng.

## 1. Project làm gì?

- Đồ án tái hiện phân cụm mờ bán giám sát; ưu tiên tính đúng và demo dễ giải thích.
- Thuật toán: FCM, sSFCM (m > 1 / m = 1), eSFCM, sSMC-FCM.
- Python + NumPy/SciPy + pandas; UI Streamlit/Plotly tiếng Việt, chạy local/offline sau cài đặt.
- Bản đầu: 20 điểm trong bài, preset + bảng giám sát, M' nhập tay 4/8, xem từng vòng U/tâm.
- Metrics: Silhouette, CH, DB, Dunn, PBM, ARI, Jaccard theo cặp.
- Phase sau: notebook, CSV/dữ liệu lớn, benchmark, chọn M' theo alpha và metrics mở rộng.

## 2. Project cấu trúc như nào?

```text
src/data.py          Dự kiến: dữ liệu/preset — mã nháp ĐÃ XÓA
src/algorithms.py    Dự kiến: lõi 5 thuật toán — mã nháp ĐÃ XÓA
src/metrics.py       Dự kiến: metrics — mã nháp ĐÃ XÓA
src/experiments.py   Dự kiến: điều phối/xuất — mã nháp ĐÃ XÓA
app.py              Entry point Streamlit — CHƯA CÓ
tests/              Kiểm thử tự động — CHƯA CÓ
docs/               Ba PDF, KE_HOACH_TRIEN_KHAI.md, DAC_TA_BAN_DAU.md
feature_list.json   Feature, phase, dependency, acceptance criteria, evidence
progress.md         Trạng thái đã xác minh + Nhật ký Phiên; phiên mới nhất trước
```

## 3. Project chạy như nào?

Chạy PowerShell tại thư mục gốc. Cài một lần; dùng môi trường đã có nếu đủ dependencies.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

- UI dự kiến: `http://127.0.0.1:8501`; dừng bằng Ctrl+C.
- **Hiện chưa có `app.py`, nên chưa khởi động được UI.** Không báo đã chạy ứng dụng.
- Nếu không dùng venv, thay `.\.venv\Scripts\python.exe` bằng `python` đúng môi trường.

## 4. Project check/run như nào?

```powershell
python -m json.tool feature_list.json > $null  # Check JSON hiện tại (PowerShell)
python -m pytest -q                  # Toàn bộ tests, sau khi tạo tests/
python -m pytest -q tests/test_algorithms.py   # Ví dụ test riêng, khi file tồn tại
```

- Dùng Python của venv nếu đã tạo ở bước 3. Không cài lại dependencies mỗi session.
- **Chưa có tests/mã src**; `no tests ran`/exit 5 không phải pass. Check JSON không kiểm chứng phần mềm.
- Thuật toán: đối chiếu bảng bài báo, baseline, ràng buộc U, KKT/residual và trường hợp biên.
- Metrics: đối chiếu độc lập; export: đọc lại; UI: preset → sửa → chạy → xem vòng → xuất.
- Chi tiết công thức, dung sai và sai khác eSFCM: `docs/KE_HOACH_TRIEN_KHAI.md`.

## 5. Project đến đâu rồi?

- Đọc **Trạng thái Đã xác minh Hiện tại** và phiên đầu `progress.md`: task, check, lỗi và bước tiếp.
- Đọc `feature_list.json` để biết trạng thái và dependency; kiểm tra file thực tế trước khi làm.
- Mốc sau DOC-001: Git đã có baseline; src đã dọn sạch trước triển khai mới. Đọc progress để biết trạng thái task mới nhất.
- `implemented_unverified` = có mã chưa nghiệm thu; `planned` = chưa làm; `deferred` = phase sau.
- Chỉ `verified` mới có `passes: true`: đủ acceptance criteria, evidence đã chạy và Git commit/checkpoint.
- Không suy phần trăm hoàn thành từ số file hoặc số đầu việc; không coi tính thử khảo sát là test src.

## WID = 1 — INIT → EXE → COMMIT

- Chỉ một task ID hoạt động, kể cả đang blocked/chờ commit; chưa đóng task trước không mở task sau.
- Chỉ làm task được giao; backlog không phải quyền tự chọn task. Phase được giao thì làm từng task tuần tự.
- Ghi scope, files, acceptance criteria và lệnh nghiệm thu trước khi sửa; không tự thêm feature/refactor.
- **INIT:** ghi branch/HEAD/status và thay đổi có sẵn; kiểm tra interpreter, dependencies, baseline liên quan.
- Khởi tạo môi trường/entry point tối thiểu là phase độc lập trước feature; không đưa thuật toán vào smoke test.
- INIT chưa pass thì không EXE. Thiếu Git/prerequisite ngoài scope thì ghi blocked, không giả checkpoint.
- **EXE:** chỉ sửa trong scope; kiểm thử task và regression liên quan; không đổi tiêu chí để làm test xanh.
- Lỗi phải có bước tái hiện và phân loại environment/product/unknown; chưa rõ không coi là tính năng.
- Lỗi môi trường tái xuất hiện: quay về INIT của cùng task; không mở task khác hoặc bẻ thuật toán để né lỗi.
- **COMMIT / DONE:** acceptance tests pass → review diff → cập nhật hồ sơ → commit local riêng task.
- Ghi checkpoint: task ID, baseline, files, commands/results, commit hash, git status và bước tiếp.
- Chỉ sau commit đặt verified/passes và completion_commit; metadata hậu commit phải được commit trước handoff.
- Kết thúc phải sạch thay đổi của task; giữ nguyên/liệt kê thay đổi có sẵn của người dùng. Không tự push.
- Test fail, thiếu commit/checkpoint hoặc lẫn scope: chưa DONE; giữ task hiện tại, không làm tiếp backlog.
- Trước đổi phiên cập nhật JSON + trạng thái hiện tại; phiên mới tiếp tục đúng task và stage còn dở.
- Feature giữ thứ tự kế hoạch sequence từ 0; không đảo theo hoàn thành. Progress chèn phiên mới đầu, giữ mọi phiên cũ.
- Phạm vi được giao ngày 09/11/2026: DOC-001 → ENV-001 → INIT-001 → DATA-001, gồm Git/môi trường tiên quyết; dừng trước CORE-001.
- Tách lõi/UI; chú thích Việt, nguồn rõ; U hợp lệ, nhãn thật không vào X, snapshot U/V cùng trạng thái.
- Đúng trọng số từng bài; không ép bảng eSFCM, không so J khác định nghĩa; Jaccard theo cặp, ID UI từ 1.
