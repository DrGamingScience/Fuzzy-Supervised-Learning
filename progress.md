# Nhật ký Tiến độ

## Trạng thái Đã xác minh Hiện tại

- Thư mục gốc kho lưu trữ: `D:\Downloads\Semi-supervised-learning` (thư mục dự án; chưa là Git repo theo kiểm tra gần nhất).
- Đường dẫn khởi động chuẩn: `app.py` — dự kiến dùng `python -m streamlit run app.py`; hiện chưa có entry point, chưa khởi động được ứng dụng.
- Đường dẫn xác minh chuẩn: kiểm tra hồ sơ hiện tại bằng `python -m json.tool feature_list.json > $null` trong PowerShell; kiểm thử phần mềm dự kiến `python -m pytest -q`, hiện chưa có `tests/`.
- Tính năng chưa hoàn thành có mức ưu tiên cao nhất hiện tại: `DOC-001`, task duy nhất theo WID=1, stage `COMMIT`, trạng thái `blocked`; chưa chuyển ENV/INIT hoặc thuật toán.
- Sự cố chặn hiện tại: chưa có Git/checkpoint; reset thư mục src còn cache chưa dọn được do policy. Các kiểm tra hồ sơ không phải bằng chứng thuật toán/ứng dụng hoạt động.

## Nhật ký Phiên

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
