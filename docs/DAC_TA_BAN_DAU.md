# Đặc tả đã chốt qua phỏng vấn

Ngày: 09/11/2026. Mục đích: đồ án, giải thích được thuật toán và demo rõ ràng. Người dùng yêu cầu triển khai nhanh, mục tiêu khoảng 2 tiếng.

## Preference đã xác nhận

- Chạy trên trình duyệt ở máy cá nhân, dùng offline sau khi cài dependencies.
- Giao diện đơn giản, tiếng Việt; ưu tiên tính đúng của lõi.
- Bao phủ FCM đối chứng, sSFCM (m > 1 và m = 1), eSFCM, sSMC-FCM.
- Bộ dữ liệu 20 điểm trong hai bài là đủ cho bản đầu; dữ liệu và thực nghiệm lớn để phase sau.
- Giám sát: preset đúng bài + bảng sửa ID điểm, cụm đích và độ thuộc giám sát.
- sSMC-FCM nhập M' thủ công; preset M' = 4 / 8; tự chọn theo alpha để phase sau.
- Xem kết quả cuối và chọn từng vòng lặp để xem U, tâm cụm và hội tụ.
- Nhóm metrics chính trước: Silhouette, CH, DB, Dunn, PBM, ARI, Jaccard theo cặp.
- Mã có chú thích tiếng Việt và README. Notebook giải thích để phase sau.
- Người dùng không có ràng buộc công nghệ; lựa chọn triển khai: Python, NumPy, SciPy, pandas, Streamlit, Plotly, pytest.

## Công việc và điều kiện nghiệm thu

### Phase 1 — Lõi và tái hiện

- [ ] Đóng gói bộ 20 điểm, nhãn tham chiếu theo hai nhóm được mô tả trong ví dụ, tâm khởi tạo có thể tái lập.
- [ ] Cài đặt 5 lựa chọn thuật toán, ánh xạ công thức vào chú thích.
- [ ] Chuẩn hóa đầu vào, kiểm tra ma trận B, xử lý khoảng cách 0 / cụm mất trọng số.
- [ ] Lưu snapshot nhất quán U và V sau mỗi vòng, J và độ dịch chuyển tâm.
- [ ] Kiểm chứng bảng bài báo trong dung sai làm tròn, điều kiện KKT cho sSMC-FCM, trường hợp thu về FCM và các trường hợp biên.
- [ ] Báo rõ sai khác eSFCM 2009; không sửa công thức chỉ để khớp bảng.

### Phase 2 — Metrics và kết quả

- [ ] Cài đặt 7 metrics đúng định nghĩa; Jaccard trên cặp điểm.
- [ ] Báo riêng toàn bộ điểm và điểm chưa giám sát với ARI/Jaccard.
- [ ] Xuất U, tâm, nhãn, lịch sử, cấu hình, metrics và trạng thái dừng.
- [ ] Các J chỉ được so theo lịch sử của cùng một thuật toán.

### Phase 3 — UI và demo

- [ ] Preset 0 / 0.3 / 0.6 và M' = 4 / 8.
- [ ] Bảng chỉnh sửa chỉ dẫn giám sát; kiểm tra lỗi ngay khi chạy.
- [ ] Chọn thuật toán, tham số phù hợp, epsilon, giới hạn vòng, seed và khởi tạo.
- [ ] Chạy một thuật toán / so sánh tất cả trên cùng điều kiện.
- [ ] Biểu đồ điểm, tâm, điểm giám sát; bảng U; thanh chọn snapshot; hội tụ; metrics.
- [ ] Cấu hình thay đổi phải được phân biệt với kết quả cũ; đổi vòng xem không chạy lại thuật toán.
- [ ] Kiểm tra luồng sử dụng thực tế, README và lệnh khởi động Windows.

### Phase sau

- Notebook thuyết trình; CSV/dữ liệu lớn; benchmark nhiều seed/tỷ lệ nhãn.
- Chọn M' theo alpha; các metrics bổ sung, hướng đến đủ 40 nếu cần.
- Kiểm thử và tối ưu cho dữ liệu lớn; không diễn giải kết quả bộ 20 điểm thành bằng chứng tổng quát về ưu thế thuật toán.

## Phạm vi bản đầu

Không thêm tài khoản, database hay hosting. Các số đo và snapshot được tính trong Python và giữ trong phiên ứng dụng; người dùng tải kết quả về tệp. Tâm khởi tạo mặc định của demo là (2.7, 5) và (9.1, 5), lựa chọn được công bố rõ trong ứng dụng và README, không tuyên bố đây là tâm khởi tạo do bài báo cung cấp.
