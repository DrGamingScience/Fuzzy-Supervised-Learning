# Nhật ký Tiến độ

## Trạng thái Đã xác minh Hiện tại

- Repo: `D:\Downloads\Semi-supervised-learning`; branch `main`; baseline task `e8394943e24b1d6bf1d9537f583a94d180e687eb`; working tree sạch trước INIT.
- Khởi động: `python -m streamlit run app.py`; kiểm tra: `python -m pytest -q`.
- Task duy nhất: `CORE-001` — INIT pass, EXE đang làm; phạm vi đã giao đến DOC-002, không làm LATER.
- Môi trường: Anaconda Python 3.13.9; imports NumPy/SciPy/pandas/sklearn/Streamlit/Plotly đã kiểm tra.
- Blocker: không có; không có thay đổi người dùng có sẵn.

## Nhật ký Phiên

### Phiên 011

- Ngày: 2026-11-09T23:08:25+07:00 (Asia/Saigon).
- Mục tiêu: CORE-001 — Cấu hình và validation đầu vào. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/algorithms.py, tests/test_algorithms.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Kiểm tra shape, số hữu hạn, miền tham số và tổng hàng B; Thông báo lỗi rõ cho cấu hình sai; Tham số không áp dụng không gây hạn chế vô lý cho thuật toán khác.
- INIT: branch main, HEAD `e8394943e24b1d6bf1d9537f583a94d180e687eb`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q PASS: 49 tests; shape/finiteness/config/B/targets và tham số không áp dụng; git diff --check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: chờ acceptance tests và review diff.
- Tệp hoặc artifact đã cập nhật: src/algorithms.py, tests/test_algorithms.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: hoàn tất EXE và COMMIT của CORE-001.

### Phiên 010

- Ngày: 09/11/2026 (Asia/Saigon); bắt đầu 2026-11-09T22:59:18+07:00.
- Mục tiêu: DATA-001 — Viết mới bộ 20 tọa độ, nhãn tham chiếu tách khỏi X, tâm đầu demo và preset đúng nguồn/quy ước ID; không viết thuật toán/UI dữ liệu. Phạm vi: src/__init__.py, src/data.py, tests/test_data.py, tests/fixtures/paper_20_points.csv, docs/DATA.md, AGENTS.md, feature_list.json, progress.md. Tiêu chí: giữ nguyên acceptance_criteria của task trong JSON.
- Đã hoàn thành: DATA-001: viết mới đủ 20 tọa độ nguồn; X (20,2) và nhãn tham chiếu (20,) tách riêng, hai nhóm 10 điểm; tâm đầu cố định của demo, preset B 0/0.3/0.6 và M' 2/4/8 với ID 9,10 → cụm 1; bản sao độc lập và tài liệu nguồn/ID. INIT baseline 9149f4f và 10 regression tests PASS trước EXE.
- Xác minh đã chạy: 09/11/2026: python -m pytest -q tests/test_data.py PASS exit 0 (18 tests); python -m pytest -q PASS exit 0 (28 tests). Hai PDF trang 4 đã render bằng pdftoppm và xem; python tmp/check_pdf_data.py PASS exit 0 sau khi giới hạn đúng vùng bảng, đối chiếu cả 20 tọa độ với fixture và src. python tmp/check_records.py; python -m json.tool feature_list.json; git diff --check PASS.
- Bằng chứng đã ghi lại: yêu cầu người dùng “Thực hiện đến hết data-001”; làm DOC → ENV → INIT → DATA tuần tự, không triển khai CORE/ALG/UI.
- Commit: `95c3b77ae2063b74d6f138ac22d6196739680f7e` (DATA-001); metadata hậu commit được lưu bằng commit riêng trước task tiếp theo/handoff. Working tree sau commit triển khai sạch.
- Tệp hoặc artifact đã cập nhật: src/__init__.py, src/data.py, tests/test_data.py, tests/fixtures/paper_20_points.csv, docs/DATA.md, AGENTS.md, feature_list.json, progress.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Lỗi tooling tái hiện bằng python tmp/check_pdf_data.py bản đầu: pypdf layout không bắt được tọa độ; PyMuPDF đọc được nhưng parser ban đầu lấy cả Table 2 (U). Phân loại environment/tooling, đã sửa reader/vùng trích xuất, không đổi dữ liệu/expected/test để né lỗi. Không có lỗi sản phẩm đang mở; chưa triển khai CORE/ALG/UI dữ liệu.
- Bước tốt nhất tiếp theo: Đã hoàn thành phạm vi đến DATA-001. CORE-001 planned, chưa được giao; không có task đang mở.

### Phiên 009

- Ngày: 09/11/2026 (Asia/Saigon); bắt đầu 2026-11-09T22:57:55+07:00.
- Mục tiêu: INIT-001 — Tạo smoke tests môi trường độc lập thuật toán và entry point Streamlit chỉ báo sẵn sàng; xác minh chạy/trả trang/dừng. Phạm vi: app.py, tests/test_environment.py, tests/test_app.py, tests/test_server.py, AGENTS.md, feature_list.json, progress.md. Tiêu chí: giữ nguyên acceptance_criteria của task trong JSON.
- Đã hoàn thành: INIT-001: entry point chỉ báo sẵn sàng; smoke dependency, AppTest chạy script thật; subprocess server localhost trả health và HTML, dừng và xác nhận port đã đóng. INIT baseline 7b08bcc/imports/config pass trước EXE.
- Xác minh đã chạy: 09/11/2026: python -m pytest -q PASS exit 0, 10 tests (7 imports, numeric/table/chart smoke, AppTest, HTTP server lifecycle). python tmp/check_records.py và git diff --check PASS. Server test dùng port local trống, luôn dừng tiến trình trong finally; không có thuật toán/metrics.
- Bằng chứng đã ghi lại: yêu cầu người dùng “Thực hiện đến hết data-001”; làm DOC → ENV → INIT → DATA tuần tự, không triển khai CORE/ALG/UI.
- Commit: `e00fba79674ee892f8b8a3858febacc377b9de56` (INIT-001); metadata hậu commit được lưu bằng commit riêng trước task tiếp theo/handoff. Working tree sau commit triển khai sạch.
- Tệp hoặc artifact đã cập nhật: app.py, tests/test_environment.py, tests/test_app.py, tests/test_server.py, AGENTS.md, feature_list.json, progress.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi trong scope; thuật toán/metrics/UI demo chưa triển khai.
- Bước tốt nhất tiếp theo: Tiếp tục DATA-001: dữ liệu 20 điểm và preset có nguồn.

### Phiên 008

- Ngày: 09/11/2026 (Asia/Saigon); bắt đầu 2026-11-09T22:56:57+07:00.
- Mục tiêu: ENV-001 — Xác minh interpreter/dependencies/config local, ghi setup lặp lại được; không chạy thuật toán. Phạm vi: requirements.txt, requirements-dev.txt, pyproject.toml, .streamlit/config.toml, .gitignore, docs/ENVIRONMENT.md, feature_list.json, progress.md. Tiêu chí: giữ nguyên acceptance_criteria của task trong JSON.
- Đã hoàn thành: ENV-001: tái sử dụng Anaconda Python 3.13.9, import đúng pin runtime; cấu hình localhost và pytest hợp lệ; docs/ENVIRONMENT.md có setup lặp lại được.
- Xác minh đã chạy: 09/11/2026: python tmp/check_environment.py PASS exit 0: NumPy 2.3.5, SciPy 1.16.3, pandas 2.3.3, sklearn 1.7.2, Streamlit 1.51.0, Plotly 6.3.0, pytest 8.4.2; python -m pip check PASS exit 0; python -m pip install --dry-run -r requirements-dev.txt PASS exit 0 (already satisfied); python tmp/check_records.py và git diff --check PASS.
- Bằng chứng đã ghi lại: yêu cầu người dùng “Thực hiện đến hết data-001”; làm DOC → ENV → INIT → DATA tuần tự, không triển khai CORE/ALG/UI.
- Commit: `bc404c2ed255c082b4e2e06af3db62c6d30ae270` (ENV-001); metadata hậu commit được lưu bằng commit riêng trước task tiếp theo/handoff. Working tree sau commit triển khai sạch.
- Tệp hoặc artifact đã cập nhật: requirements.txt, requirements-dev.txt, pyproject.toml, .streamlit/config.toml, .gitignore, docs/ENVIRONMENT.md, feature_list.json, progress.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không kiểm chứng cài đặt venv mới; chưa có entry point/tests ở task ENV. Không có lỗi môi trường đang mở.
- Bước tốt nhất tiếp theo: Tiếp tục INIT-001: smoke test và entry point tối thiểu.

### Phiên 007

- Ngày: 09/11/2026 (Asia/Saigon); bắt đầu 2026-11-09T22:55:55+07:00.
- Mục tiêu: DOC-001 — Đóng hồ sơ, dọn cache bản nháp và Git checkpoint; bootstrap Git là prerequisite được mở bởi yêu cầu đến DATA-001. Phạm vi: AGENTS.md, docs/WORKFLOW.md, feature_list.json, progress.md, src/__pycache__. Tiêu chí: giữ nguyên acceptance_criteria của task trong JSON.
- Đã hoàn thành: Git baseline 4f7fd34 giữ nguyên file có sẵn; xác nhận src rỗng và xóa thư mục bằng lệnh không đệ quy; mở scope đến DATA-001, giữ nguyên lịch sử.
- Xác minh đã chạy: 09/11/2026: python tmp/check_records.py PASS; git diff --check PASS; Test-Path src = False sau cleanup. Lệnh xóa đệ quy bị automatic policy chặn; xóa rỗng không đệ quy thành công. Nghiệm thu hồ sơ, không phải thuật toán.
- Bằng chứng đã ghi lại: yêu cầu người dùng “Thực hiện đến hết data-001”; làm DOC → ENV → INIT → DATA tuần tự, không triển khai CORE/ALG/UI.
- Commit: `1dcb6fd266a5f0b4a9860988a2599425aa9f20d4` (DOC-001); metadata hậu commit được lưu bằng commit riêng trước task tiếp theo/handoff. Working tree sau commit triển khai sạch.
- Tệp hoặc artifact đã cập nhật: AGENTS.md, docs/WORKFLOW.md, feature_list.json, progress.md, src/__pycache__.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi trong scope; thuật toán/metrics/UI demo chưa triển khai.
- Bước tốt nhất tiếp theo: Tiếp tục ENV-001 theo yêu cầu đến DATA-001.

### Phiên 006

- Ngày: 09/11/2026 (Asia/Saigon).
- Mục tiêu: sửa progress theo đúng mẫu Nhật ký Phiên; chỉ nhật ký mới nhất lên đầu, feature list giữ thứ tự kế hoạch từ đầu.
- Đã hoàn thành: chuyển 5 mốc cũ thành Phiên 001–005 và giữ nội dung nguyên văn; chèn phiên này đầu; bổ sung sequence 0–28 cho feature theo đúng thứ tự đang có; sửa quy ước sai trong AGENTS và WORKFLOW. Đây là thay đổi nội dung, DOC-001 chưa DONE theo điều kiện commit/checkpoint.
- Xác minh đã chạy: `python tmp/check_session_format.py` PASS (exit 0): đúng 2 phần của mẫu, 5 trường trạng thái, 9 trường mỗi phiên; thứ tự Phiên 006–001; bảo toàn 5 khối lịch sử; giữ nguyên 29 ID/thứ tự/trạng thái feature, sequence 0–28, JSON/dependency/WID=1; AGENTS 87 < 100 dòng. Script kiểm tra tạm đã được dọn sau khi chạy.
- Bằng chứng đã ghi lại: 29 feature giữ nguyên ID/trạng thái; 5 khối nhật ký cũ được giữ nguyên văn dưới Bằng chứng của từng phiên; không ghi giả kết quả chạy ứng dụng hoặc commit.
- Commit: chưa có; thư mục chưa là Git repo theo lần kiểm tra gần nhất.
- Tệp hoặc artifact đã cập nhật: progress.md, feature_list.json, AGENTS.md, docs/WORKFLOW.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: DOC-001 vẫn COMMIT/blocked do thiếu Git/checkpoint; src/__pycache__ còn 5 file .pyc do lệnh dọn trước bị policy chặn. Chưa có src/*.py, app.py, tests/ hoặc README.
- Bước tốt nhất tiếp theo: bàn giao đúng hồ sơ này; chưa tự triển khai tính năng. Chỉ xử lý phần dọn còn thiếu và bootstrap Git khi phạm vi được giao cho cùng task.

### Phiên 005

- Ngày: 09/11/2026 (Asia/Saigon); mốc gốc: 2026-11-09T22:42:32+07:00.
- Mục tiêu: Sắp xếp mới nhất trước và reset mã nguồn theo yêu cầu.
- Đã hoàn thành: Xóa 5 file src/*.py, đưa 14 feature về planned, sửa UTF-8 và đảo nhật ký. Quy tắc đảo feature của phiên này được sửa ở Phiên 006.
- Xác minh đã chạy: Python kiểm tra hồ sơ/UTF-8/WID/dependency/reset: PASS; lệnh xóa thư mục/cache bị policy từ chối.
- Bằng chứng đã ghi lại: bảo toàn nội dung nhật ký gốc bên dưới; các trạng thái cũ chỉ mô tả thời điểm ghi.

  > - Người dùng giao cập nhật feature list/progress, đặt feature hoàn thành mới nhất trên đầu và xóa src để bắt đầu lại.
  > - Đã xóa 5 file mã nguồn .py trong src bằng apply_patch; chưa xóa hết thư mục vì còn __pycache__.
  > - Hai lệnh xóa qua PowerShell bị policy từ chối; không có lý do chi tiết. Không dùng đường vòng để xóa cache/thư mục.
  > - Đưa 14 feature có mã bị xóa về planned; giữ expected_files để biết nơi dự kiến triển khai lại. ENV-001 còn cấu hình nên vẫn implemented_unverified.
  > - Thêm completed_at (null cho task chưa DONE), quy tắc verified mới nhất trước và nhật ký mới nhất trước. Không tự tạo timestamp hoàn thành hoặc commit.
  > - Sửa các chuỗi metadata JSON bị lỗi mã hóa tiếng Việt từ lần cập nhật trước; dùng script UTF-8 để ghi đúng.
  > - Không chạy lại thuật toán, không tạo src mới, không mở task khác. Git/checkpoint còn thiếu; DOC-001 vẫn COMMIT/blocked.
  > - Kiểm tra qua stdin lần đầu gặp lỗi mã hóa ở chuỗi đối chiếu tiêu đề; lần chạy lại dùng Unicode escape đã PASS (exit 0), không sửa dữ liệu chuẩn để bỏ qua kiểm tra.
  > - Kiểm tra cuối PASS: JSON/UTF-8, thứ tự feature/nhật ký, WID=1, dependency, trạng thái reset, AGENTS 87 dòng; xác nhận chưa dọn hết cache. Không coi kiểm tra hồ sơ là kiểm thử phần mềm.

- Commit: chưa có; không suy ra commit từ việc kiểm tra tài liệu pass.
- Tệp hoặc artifact đã cập nhật: src/*.py đã xóa; AGENTS.md, docs/WORKFLOW.md, feature_list.json, progress.md cập nhật.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: src/__pycache__ còn 5 file .pyc; chưa có Git/checkpoint; không có phần mềm đã nghiệm thu.
- Bước tốt nhất tiếp theo: Sửa cách tổ chức nhật ký và giữ thứ tự feature theo làm rõ của người dùng.

### Phiên 004

- Ngày: 09/11/2026 (Asia/Saigon); mốc gốc: 09/11/2026.
- Mục tiêu: WID=1, gate INIT/EXE/COMMIT và Definition of Done.
- Đã hoàn thành: Thêm WID=1, INIT → EXE → COMMIT, phase INIT và Definition of Done.
- Xác minh đã chạy: Kiểm tra hồ sơ: PASS; git rev-parse/status/log: not a git repository.
- Bằng chứng đã ghi lại: bảo toàn nội dung nhật ký gốc bên dưới; các trạng thái cũ chỉ mô tả thời điểm ghi.

  > - Người dùng yêu cầu chỉ làm task được giao, chưa đóng việc trước không làm việc sau, có kiểm thử/commit/checkpoint để đổi phiên sạch.
  > - Đã cập nhật AGENTS còn 86 dòng; quy trình chi tiết tách sang `docs/WORKFLOW.md`.
  > - Thêm INIT độc lập trước execute: ENV-001 chỉ kiểm tra interpreter/dependencies/config; INIT-001 tạo smoke test và entry point tối thiểu khi được giao, chưa làm thuật toán.
  > - Gate DATA-001 và UI-001 được nối qua INIT-001; không dùng kiểm thử môi trường làm bằng chứng thuật toán đúng.
  > - Definition of Done: acceptance checks pass, review diff đúng scope, hồ sơ đồng bộ, Git commit/checkpoint có thật, working tree sạch trong scope; giữ thay đổi của người dùng.
  > - Kiểm tra `git rev-parse --is-inside-work-tree`, `git status --short`, `git log -1` đều thất bại: `not a git repository`. Không tự git init/commit hoặc cài môi trường trong task chỉnh hồ sơ này.
  > - DOC-001 được chuyển từ verified cũ sang blocked/passes=false vì tiêu chuẩn mới yêu cầu commit/checkpoint chưa có; evidence kiểm tra tài liệu trước đây vẫn được bảo toàn.
  > - Python qua stdin kiểm tra AGENTS < 100 dòng/đủ 5 mục, JSON, WID=1, trạng thái/commit, file references và dependency không chu trình: **PASS, exit 0**.
  > - Không sửa src, không chạy thêm thuật toán, không mở task mới. Chưa có Git commit; chưa DONE theo quy trình mới.

- Commit: chưa có; không suy ra commit từ việc kiểm tra tài liệu pass.
- Tệp hoặc artifact đã cập nhật: AGENTS.md, docs/WORKFLOW.md, feature_list.json, progress.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: DOC-001 chuyển blocked vì chưa có Git/checkpoint.
- Bước tốt nhất tiếp theo: Giữ cùng task; chỉ bootstrap Git khi phạm vi được giao.

### Phiên 003

- Ngày: 09/11/2026 (Asia/Saigon); mốc gốc: 09/11/2026.
- Mục tiêu: Tối ưu bàn giao giữa các session.
- Đã hoàn thành: Rút AGENTS còn 76 dòng tại thời điểm đó và thêm lệnh khởi động/kiểm tra.
- Xác minh đã chạy: python -m compileall -q src: PASS, exit 0 trước khi src bị xóa; kiểm tra AGENTS: PASS.
- Bằng chứng đã ghi lại: bảo toàn nội dung nhật ký gốc bên dưới; các trạng thái cũ chỉ mô tả thời điểm ghi.

  > - Viết lại `AGENTS.md` thành 76 dòng, trả lời trực tiếp: mục tiêu, cấu trúc, khởi động, kiểm tra và tiến độ.
  > - Bổ sung lệnh tạo venv/cài dependencies/chạy Streamlit, check nhanh cú pháp, chạy toàn bộ test hoặc một file test.
  > - Ghi rõ `app.py` và `tests/` chưa tồn tại; lệnh UI/pytest là hướng dẫn cho khi các entry point đó được tạo, không tuyên bố đã chạy.
  > - Thêm **Bàn giao nhanh** đầu file này và quy định cập nhật sau mỗi feature/session.
  > - Đã chạy `python -m compileall -q src`: **PASS, exit 0**. Kết quả chỉ xác nhận cú pháp, không xác nhận công thức hay kết quả tính toán.
  > - Đã kiểm tra số dòng AGENTS (76 < 100), đủ 5 mục và các lệnh chính: **PASS**.
  > - Không sửa hay tiếp tục triển khai tính năng trong `src/`; trạng thái feature phần mềm giữ nguyên.

- Commit: chưa có; không suy ra commit từ việc kiểm tra tài liệu pass.
- Tệp hoặc artifact đã cập nhật: AGENTS.md, feature_list.json, progress.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Compile chỉ kiểm tra cú pháp; chưa có ứng dụng hoặc tests.
- Bước tốt nhất tiếp theo: Chốt WID và điều kiện đóng task.

### Phiên 002

- Ngày: 09/11/2026 (Asia/Saigon); mốc gốc: 09/11/2026.
- Mục tiêu: Chuẩn hóa hồ sơ quản lý triển khai.
- Đã hoàn thành: Tạo AGENTS, feature list và progress theo hiện trạng thời điểm đó.
- Xác minh đã chạy: Python kiểm tra JSON, ID, phase/status, dependency và file references: PASS.
- Bằng chứng đã ghi lại: bảo toàn nội dung nhật ký gốc bên dưới; các trạng thái cũ chỉ mô tả thời điểm ghi.

  > - Tạo `AGENTS.md`: phạm vi, workflow, trạng thái, yêu cầu khoa học, bằng chứng nghiệm thu và cách bàn giao.
  > - Tạo `feature_list.json`: công việc nhỏ theo P0–P4, dependency, acceptance criteria, files, evidence và passes.
  > - Tạo file tiến độ này; đánh dấu mã đang có là `implemented_unverified`, UI/tests là `planned`, phần mở rộng là `deferred`.
  > - Đã chạy kiểm tra bằng Python qua stdin: JSON hợp lệ, ID duy nhất, phase/status hợp lệ, `passes` đồng nhất với trạng thái, đường dẫn file tồn tại, dependency không có chu trình và tài liệu không rỗng. Kết quả: **PASS**.
  > - Đã đối chiếu preference với các câu trả lời phỏng vấn. Chỉ `DOC-001` được đánh dấu `verified` cho bộ hồ sơ; không có feature phần mềm nào được đánh dấu pass.

- Commit: chưa có; không suy ra commit từ việc kiểm tra tài liệu pass.
- Tệp hoặc artifact đã cập nhật: AGENTS.md, feature_list.json, progress.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Kết quả pass tài liệu cũ không đáp ứng Definition of Done có commit được bổ sung ở Phiên 004.
- Bước tốt nhất tiếp theo: Làm rõ quy trình bắt đầu và bàn giao phiên.

### Phiên 001

- Ngày: 09/11/2026 (Asia/Saigon); mốc gốc: 09/11/2026.
- Mục tiêu: Khảo sát, phỏng vấn và khởi tạo mã.
- Đã hoàn thành: Khảo sát tài liệu, phỏng vấn và tạo các bản nháp ban đầu; trạng thái này là lịch sử, mã đã bị xóa ở Phiên 005.
- Xác minh đã chạy: Phép tính khảo sát độc lập và đọc phiên bản môi trường; chưa có tests cho mã src.
- Bằng chứng đã ghi lại: bảo toàn nội dung nhật ký gốc bên dưới; các trạng thái cũ chỉ mô tả thời điểm ghi.

  > - Hoàn thành khảo sát và ghi preference như trên.
  > - Đã viết các bản nháp mã và cấu hình; chưa kiểm chứng thực thi chúng.
  > - Người dùng yêu cầu dừng để viết `AGENTS.md`, feature list JSON và progress, đồng thời báo cáo những gì đã làm.

- Commit: chưa có; không suy ra commit từ việc kiểm tra tài liệu pass.
- Tệp hoặc artifact đã cập nhật: docs/KE_HOACH_TRIEN_KHAI.md, docs/DAC_TA_BAN_DAU.md; các file src/cấu hình tại thời điểm đó.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Mã nháp chưa kiểm chứng; sai khác số liệu eSFCM cần phân tích.
- Bước tốt nhất tiếp theo: Chốt hồ sơ trước khi tiếp tục implementation.
