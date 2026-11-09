# Quy trình WID = 1: INIT → EXE → COMMIT

Áp dụng từ yêu cầu ngày 09/11/2026. Đây là quy trình thực hiện tác vụ, tách khỏi các phase sản phẩm P0–P4. Mỗi tác vụ được giao đều đi qua ba bước theo thứ tự.

## 1. Một tác vụ được phép làm

- WID = 1: chỉ một task ID đang hoạt động, kể cả khi task đó đang chờ commit hoặc bị blocked. Không bắt đầu task tiếp theo khi task hiện tại chưa đóng.
- Chỉ thực hiện task người dùng giao. `feature_list.json` là backlog, không phải giấy phép tự lấy task khác để làm.
- Nếu người dùng giao một phase, lập thứ tự các task trong phase và thực hiện tuần tự; không tự mở phase tiếp theo.
- Trước khi làm, ghi task ID, yêu cầu gốc, phạm vi file/hành vi, phần không làm, acceptance criteria và lệnh nghiệm thu. Nếu mục tiêu chưa rõ, chỉ làm rõ yêu cầu và khảo sát cần thiết.
- Không thêm tính năng, refactor hoặc sửa lỗi ngoài scope vì thấy thuận tiện. Vấn đề ngoài scope được ghi lại, không âm thầm sửa.
- Dependency phải được nghiệm thu trước. Nếu cần thay đổi dependency/prerequisite ngoài phạm vi được giao, báo trở ngại và chờ người dùng điều chỉnh phạm vi; không chuyển task.
- Người dùng đã yêu cầu xóa bản nháp src để bắt đầu lại; không tự khôi phục hoặc tái sử dụng. Các feature tương ứng trở về planned, không phải nhiều task đang làm.

## 2. INIT — chuẩn bị độc lập, chưa làm tính năng

### Đầu vào

Đọc AGENTS, Trạng thái Đã xác minh Hiện tại và phiên mới nhất trong progress, task được giao, dependency và acceptance criteria. Kiểm tra repo và thay đổi của người dùng trước khi sửa.

### Checklist

1. Xác định task ID duy nhất; ghi scope, acceptance criteria và các file dự kiến thay đổi.
2. Ghi checkpoint xuất phát: branch, HEAD, `git status --short` và các thay đổi có sẵn của người dùng. Không reset, stash hoặc commit hộ những thay đổi ngoài scope.
3. Kiểm tra đúng Python/interpreter, môi trường, dependencies và phiên bản bằng lệnh thực thi.
4. Chạy kiểm tra baseline liên quan; ghi command, exit code và kết quả. Khi chưa có test tính năng, ghi rõ chưa có; không gọi trạng thái đó là pass.
5. Phân loại lỗi: `environment`, `product`, hoặc `unknown`. Lỗi môi trường gồm import, dependency, cấu hình, port và entry point; lỗi thuật toán/sai kết quả là lỗi sản phẩm. Chưa đủ bằng chứng thì giữ `unknown`.
6. Chỉ sửa prerequisite nằm trong scope của INIT được giao. Chạy lại đúng kiểm tra đã lỗi; không nới kỳ vọng hay sửa thuật toán để che lỗi môi trường.
7. Ghi kết quả INIT và checkpoint baseline. Chỉ sang EXE khi mọi điều kiện INIT bắt buộc đã pass.

### Khởi tạo project lần đầu

Đây là phase độc lập phải được giao và đóng trước khi thực hiện feature:

| Task | Phạm vi | Nghiệm thu |
| --- | --- | --- |
| Gate Git trong INIT của task được giao | Repo và baseline, chỉ khi phạm vi đã cho phép | Có HEAD, phạm vi tracking rõ, baseline ghi mã chưa kiểm chứng, status được ghi nhận |
| `ENV-001` | Interpreter, dependencies, cấu hình local | Cài/kiểm tra dependencies và imports thành công; có lệnh lặp lại được, không phụ thuộc thuật toán |
| `INIT-001` | Kiểm tra môi trường và entry point tối thiểu | Có kiểm tra môi trường bằng pytest; UI tối thiểu khởi động local và dừng được; không chạy clustering/metrics; có bằng chứng rồi commit |

INIT tối thiểu chỉ hiển thị trạng thái sẵn sàng, không đưa chức năng phân cụm vào để chứng minh môi trường hoạt động. Sau khi INIT đóng mới xử lý DATA/CORE/ALG theo tác vụ được giao.

Nếu thư mục chưa có Git, không báo có HEAD hay giả commit. Việc khởi tạo repo là prerequisite cần được giao/phạm vi được mở rõ; cho đến lúc đó COMMIT không thể hoàn tất.

## 3. EXE — chỉ thực hiện task được giao

- Bắt đầu từ checkpoint INIT đã pass; giữ nguyên phạm vi và acceptance criteria đã ghi.
- Sửa code cùng kiểm thử trực tiếp liên quan, theo từng thay đổi có thể kiểm chứng.
- Dùng baseline để phân biệt lỗi cũ với lỗi mới. Ghi điều kiện tái hiện trước khi kết luận lỗi là hành vi mong muốn.
- Không đổi dữ liệu chuẩn, expected output hoặc dung sai để làm test xanh; thay đổi giả thiết cần căn cứ bài báo hoặc chỉ dẫn người dùng, có nhật ký.
- Nếu lỗi môi trường xuất hiện lại, dừng EXE và quay về INIT của cùng task; không mở task thứ hai.
- Chạy acceptance tests của task và regression liên quan; không coi compile/import hoặc test môi trường là bằng chứng thuật toán đúng.
- Khi chưa pass hoặc chưa đủ bằng chứng, giữ task mở. Không làm UI/metric/feature tiếp theo để tránh vấn đề đang tồn tại.

## 4. COMMIT — điều kiện đóng tác vụ

Một tác vụ chỉ **DONE** khi đồng thời có đủ:

1. Tất cả acceptance criteria đạt, các lệnh kiểm thử bắt buộc thực sự chạy và pass; không có lỗi chưa xử lý trong scope.
2. Đã tự xem diff, không có thay đổi ngoài scope, không lẫn dữ liệu bí mật/output tạm hoặc thay đổi có sẵn của người dùng.
3. `feature_list.json` và `progress.md` cập nhật đúng; có lệnh/kết quả kiểm tra, giới hạn và bước tiếp theo. Feature giữ thứ tự kế hoạch sequence từ 0, không đảo khi hoàn thành; trạng thái hiện tại đầu progress, phiên mới chèn đầu Nhật ký Phiên.
4. Có Git commit local riêng cho tác vụ, ví dụ `feat(ALG-001): implement FCM`, `test(INIT-001): verify local environment` hoặc `docs(DOC-001): define task workflow`.
5. Có checkpoint sau commit: task ID, commit hash, kết quả kiểm tra, file thay đổi và trạng thái `git status --short` được báo trong bàn giao.
6. Working tree sạch đối với phần thay đổi của tác vụ. Nếu có thay đổi của người dùng trước INIT, chúng phải được giữ nguyên và liệt kê; không cần ép toàn repo sạch bằng thao tác phá hủy.

Chỉ sau bước 4 mới đặt `status: verified`, `passes: true` và ghi `completion_commit`. Commit hash được đọc từ `git log -1` và báo trong handoff/checkpoint sau commit; không cố ghi hash của commit vào chính commit đó. Nếu cập nhật metadata hậu commit, gom vào commit bàn giao cuối cùng và xác nhận status sạch.

Khi đóng task, ghi `completed_at` theo ISO 8601 có múi giờ từ thời điểm hoàn thành thực tế; task chưa xong để null. Không dùng completed_at/status để đổi vị trí feature: giữ sequence từ 0 theo kế hoạch. Chỉ chèn phiên mới đầu Nhật ký Phiên, kể cả cùng ngày; giữ nguyên mọi phiên cũ bên dưới và không đổi ID phiên. Thứ tự hiển thị không thay đổi dependency hoặc WID=1.

Checkpoint trước commit nằm trong progress, gồm task, baseline hash, files, commands/results và trạng thái chờ commit. Checkpoint sau commit là commit chứa hồ sơ này cùng hash/status trong handoff; không cần tạo một file sửa thêm sau mỗi lần commit.

Nếu chưa có Git, test fail, thiếu bằng chứng, có scope lẫn chưa tách được hoặc commit thất bại: COMMIT chưa xong, `passes` phải false; giữ cùng task và ghi lý do. Không báo DONE và không chuyển task khác. Không push remote trừ khi người dùng yêu cầu.

## 5. Đổi phiên khi chưa xong

Trước khi kết thúc session, cập nhật đúng mẫu `progress.md` và trạng thái máy đọc được trong JSON:

```text
# Nhật ký Tiến độ
## Trạng thái Đã xác minh Hiện tại
- Thư mục gốc kho lưu trữ:
- Đường dẫn khởi động chuẩn:
- Đường dẫn xác minh chuẩn:
- Tính năng chưa hoàn thành có mức ưu tiên cao nhất hiện tại:
- Sự cố chặn hiện tại:
## Nhật ký Phiên
### Phiên NNN (phiên mới nhất chèn tại đây; không xóa phiên cũ)
- Ngày:
- Mục tiêu:
- Đã hoàn thành:
- Xác minh đã chạy:
- Bằng chứng đã ghi lại:
- Commit:
- Tệp hoặc artifact đã cập nhật:
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết:
- Bước tốt nhất tiếp theo:
```

Task chưa đóng vẫn là task duy nhất của phiên sau. Người dùng có thể yêu cầu hủy hoặc đổi ưu tiên; khi đó ghi rõ bàn giao thay đổi dang dở, không âm thầm coi task cũ đã hoàn thành.

## 6. Phạm vi giao mới ngày 09/11/2026

- Yêu cầu mới “Thực hiện đến hết data-001 trong feature” mở phạm vi cho prerequisite: Git baseline, đóng DOC-001, ENV-001, INIT-001 rồi DATA-001, theo WID=1.
- Baseline `4f7fd34` lưu nguyên văn hồ sơ/cấu hình/PDF có sẵn; không coi baseline là phần mềm đã kiểm chứng. Artifact tmp và cache không được tracking.
- Kiểm tra đầu phiên: src không còn file/cache. Lệnh xóa đệ quy bị automatic policy chặn; lệnh xóa thư mục rỗng không đệ quy đã thành công. Blocker cũ được giữ nguyên như lịch sử.
- Không khôi phục bản nháp; DATA-001 viết mới từ bảng nguồn sau ENV/INIT verified. Dừng trước CORE-001.
