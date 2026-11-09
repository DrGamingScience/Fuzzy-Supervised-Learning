# Giao thức kiểm chứng lõi

Các tests chạy trực tiếp trên `src`, viết mới sau khi xóa bản nháp. Các số tính thử
trong kế hoạch không thay cho test. Chạy `python -m pytest -q` tại gốc repo.

- `test_algorithms.py`: kiểm tra validation, công thức U, tâm một vòng độc lập,
  B=0/M'=M thu về FCM, entropy và KKT nhiều cụm. KKT dùng gradient
  `m_ik U_ik^(m_ik-1) d_ik²` bằng nhau trong từng hàng.
- `test_paper.py`: bảng U 20 hàng (hai cột bổ sung nhau) và tối ưu SLSQP độc lập
  cho 5 hàm mục tiêu tại tâm cố định; không gọi công thức cập nhật src làm oracle.
- `test_numerics.py`: điểm/tâm trùng, B đầy, mất trọng số, số mũ lớn,
  khoảng cách overflow/underflow báo lỗi yêu cầu đổi thang dữ liệu.
- `test_history.py`: U tính từ chính V của mọi snapshot, J/shift, J không tăng,
  vòng 0, epsilon/max_iter và bản sao không bị sửa khi fit tiếp tục.

Fixture `paper_memberships.csv` chép cột độ thuộc cụm 1 từ Endo 2009 Table II
(PDF trang 5) và Khang 2021 Table 3 (PDF trang 10). Đã xem ảnh render để đối chiếu.
Dung sai bảng U là 0.005 theo hai chữ số in; tâm 2021 là 0.001 theo ba chữ số.
Không cam kết số vòng lặp giống bài vì tâm đầu/tiêu chí dừng nguồn không đầy đủ.
Table III (m=1) kiểm tra toàn bộ 20 hàng ở ba case bằng giá trị chính xác.

eSFCM: thực hiện Endo (9),(10),(14), trọng số tâm U, `0 log 0 = 0`.
Thay tâm Table V `(4.60,5),(8.33,5)` vào (14), lambda=1, X1=(0,4.5),
cho U1,2 khoảng 1.13e-21 thay vì 0.24 của Table IV. Vì vậy không ép bảng này.
FCM tâm thứ hai tính được 9.017398 khớp 9.018 của 2021, khác 9.08 của 2009.
Nguyên nhân sai khác nguồn chưa xác định. UI/export phải giữ cảnh báo này.

Sai khác bổ sung khi chạy test toàn bảng: Table 3 (2021), M'=4, ID 17 và 19
in U1=0.11. Thay trực tiếp tâm nguồn `(2.735,5),(9.200,5)` vào (15) cho
0.10452027; hội tụ src cho 0.10451687, làm tròn 0.10. Hai hàng này được
kiểm tra bằng test sai khác riêng, giữ nguyên fixture 0.11 và dung sai 0.005
cho các hàng còn lại; không sửa thuật toán hay nới dung sai cả bảng.

Nghiệm thu tích hợp ngày 09/11/2026: `python -m pytest -q` — 139 tests PASS.
Nhóm metrics đối chiếu Silhouette/CH/DB và ARI với sklearn, Dunn/PBM và cặp
Jaccard với ví dụ tính tay; export đọc lại strict JSON, CSV BOM và mọi snapshot.
Luồng AppTest và giới hạn editor được mô tả trong `docs/QA.md`.
