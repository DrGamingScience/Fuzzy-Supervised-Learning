# DATA-001 — dữ liệu 20 điểm và preset

`src/data.py` viết mới, không khôi phục bản nháp. Nguồn tọa độ:

- Endo và cộng sự, *On Semi-Supervised Fuzzy c-Means Clustering* (2009), mục III.A, Table I, trang PDF 4 / trang in 1122; file `FCM Bán giám sát - yasunori2009.pdf`.
- Khang, Tran, Fowler, *A Novel Semi-Supervised Fuzzy C-Means Clustering Algorithm Using Multiple Fuzzification Coefficients* (2021), Algorithms 14, 258, mục 2.2, Table 1, trang 4; file `algorithms-14-00258-v2.pdf`.

Ngày 09/11/2026 đã render và xem hai trang nguồn; đối chiếu đủ 20 ID/tọa độ. Fixture `tests/fixtures/paper_20_points.csv` chép riêng từ bảng, sau đó đối chiếu bằng text extraction trực tiếp từ cả hai PDF. Pytest không cần PDF reader hay Internet; fixture không sinh từ mã dữ liệu.

`load_paper_data()` trả hai mảng riêng: X float64 (20, 2), y int64 (20,). X chỉ chứa hai tọa độ gốc, không chuẩn hóa, không chứa ID/nhãn. Nhóm tham chiếu: ID 1–10 thuộc nhóm hiển thị 1, ID 11–20 thuộc nhóm hiển thị 2; mã nội bộ y = 0/1. Đây là quy ước đánh giá theo mô tả hai nhóm và hình học ví dụ, không phải cột nhãn do Table I/Table 1 công bố, cũng không phải kết quả thuật toán. Mỗi lần gọi trả mảng mới, sửa dữ liệu của một lần gọi không ảnh hưởng lần khác.

ID điểm và cụm hiển thị bắt đầu 1; chỉ số mảng bắt đầu 0. Ví dụ ID 9 → hàng 8, cụm hiển thị 1 → cột 0. `PAPER_POINT_IDS` giữ thứ tự 1–20.

`demo_initial_centers()` trả V0 = [(2.7, 5), (9.1, 5)]. Đây là lựa chọn cố định của dự án theo đặc tả, không phải tâm đầu công bố trong bài và không phải tâm hội tụ. Không có lấy mẫu ngẫu nhiên nên không cần seed. Hàm trả bản sao mới, giữ thứ tự tâm để cụm hiển thị 1 tương ứng hàng 0.

| API | Preset | Nội dung |
| --- | --- | --- |
| `membership_preset(level)` | 0 / 0.3 / 0.6 | B (20, 2), B[8,0] = B[9,0] = level, còn lại 0 |
| `ssmc_preset(m_prime)` | 2 / 4 / 8 | M = 2; M' = 2 không giám sát; 4/8 chỉ tiết lộ ID 9, 10 → cụm 1 |

Preset B theo ba case ở mục III.A (2009) và mục 2.2 (2021); áp dụng sSFCM/eSFCM. B là cận dưới/chỉ dẫn, không phải độ thuộc cuối cùng. sSMC theo ba case mục 4 (2021), trang 10: `SSMCPreset` giữ M, M' và tuple targets bất biến; -1 nghĩa chưa giám sát, 0 nghĩa cụm hiển thị 1. Không suy toàn bộ targets từ y. M' là số mũ, không quy đổi thành B = 0.3/0.6.

Hàm chọn preset từ chối giá trị ngoài danh sách bằng ValueError; validation cấu hình thuật toán tổng quát thuộc CORE-001. Chưa tính số mũ theo từng ô, chạy fit, tạo snapshot, metrics, bảng sửa giám sát hoặc UI dữ liệu.

Nghiệm thu: `python -m pytest -q tests/test_data.py`, rồi `python -m pytest -q` để regression gồm môi trường, AppTest và vòng đời server local. Tests kiểm tra toàn bộ tọa độ/nhóm so fixture, tách nhãn, bản sao độc lập, tâm đầu và từng preset/ID. Kiểm chứng dữ liệu không phải bằng chứng thuật toán đúng.
