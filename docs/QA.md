# Nghiệm thu demo

Lệnh: `python -m pytest -q`. AppTest thực thi `app.py` với Streamlit thật.
Lệnh chạy thủ công: `python -m streamlit run app.py`, mở http://127.0.0.1:8501.

`tests/test_ui_flow.py` kiểm tra từng thuật toán qua UI; preset B=0/0.3/0.6,
M'=4/8 qua các tests UI và bảng nguồn; lỗi ID/B/trùng, dòng tắt, M'<M.
Luồng đầy đủ: preset → sửa B/tắt dòng → chạy đơn → chọn vòng 0 → so sánh năm
thuật toán → chọn từng kết quả → tải ZIP và đọc lại. Spy đếm lần fit chứng minh
slider/chọn kết quả không tính lại. Kết quả cũ và ZIP được giữ khi input lỗi;
cấu hình thay đổi có cảnh báo, chạy thành công mới thay kết quả.

Giới hạn tooling: AppTest 1.51 không có API thao tác `data_editor`; tests gửi
`edited_rows` vào widget session_state cùng sự kiện chạy. AppTest có thể xóa
delta đó trong lần rerun kế tiếp vì không có frontend editor giữ nó; khi so sánh
tests gửi lại cùng delta. Đối chiếu kết quả thực nhận B/targets và ZIP sau chạy,
không suy edit thành công chỉ từ bảng render. Đây là kiểm tra backend/widget
state, không thay cho kiểm tra thao tác nhập bảng bằng chuột trên trình duyệt.

Sửa trong QA: giữ lựa chọn preset B khi đổi qua thuật toán không dùng B rồi
quay lại. Trước sửa, widget được tạo lại với mặc định 0.3 có thể reset bảng;
đã thêm test preset0.6 → sSMC → sSFCM giữ0.6. Không sửa thuật toán trong QA.

`tests/test_server.py` tạo server subprocess localhost trên port trống,
kiểm tra health và HTML, dừng trong finally và xác nhận port đóng.
Đây là kiểm tra AppTest + vòng đời HTTP; không tuyên bố đã kiểm tra trực quan
mọi trình duyệt hoặc triển khai hosting. Các biểu đồ dùng Plotly cục bộ,
không có assets CDN/map hoặc dữ liệu mạng do ứng dụng tải.
