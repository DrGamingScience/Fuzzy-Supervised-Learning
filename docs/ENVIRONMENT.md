# Môi trường local — ENV-001

Kiểm tra ngày 09/11/2026 tại branch `main`, baseline task `977b9dc`.
Interpreter đang dùng: `D:\Downloads\ANACONDA\python.exe`, Python 3.13.9 64 bit.
Tái sử dụng môi trường này vì các dependency đã đủ; không cài lại và không thay đổi package toàn máy.

| Package | Phiên bản đã import |
| --- | --- |
| numpy | 2.3.5 |
| scipy | 1.16.3 |
| pandas | 2.3.3 |
| scikit-learn | 1.7.2 |
| streamlit | 1.51.0 |
| plotly | 6.3.0 |
| pytest | 8.4.2 |

Các package runtime được pin trong requirements.txt; pytest dùng khoảng tương thích `>=8,<10` trong requirements-dev.txt. Cấu hình Streamlit bind `127.0.0.1`, headless, tắt gửi usage stats. Pytest tìm tests/ và thêm thư mục gốc vào đường import.

Lệnh PowerShell tại thư mục gốc để kiểm tra môi trường hiện có:

```powershell
python -c "import sys; print(sys.executable); print(sys.version)"
python -c "import numpy, scipy, pandas, sklearn, streamlit, plotly, pytest; print([(m.__name__, m.__version__) for m in (numpy, scipy, pandas, sklearn, streamlit, plotly, pytest)])"
python -m pip check
python -m pip install --dry-run -r requirements-dev.txt
```

Đã chạy: imports/pin/config PASS, `pip check` exit 0 (No broken requirements found), dry-run exit 0 (mọi requirement đã satisfied). Không chạy thuật toán để kiểm tra môi trường; smoke test và entry point thuộc INIT-001.

Tạo môi trường riêng trên máy khác hoặc khi chưa đủ dependency:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Chỉ chạy hai lệnh cuối sau khi INIT-001 tạo tests/app.py. Nếu dùng môi trường hiện có, thay đường Python venv bằng `python`. Chưa kiểm chứng cài đặt mới trong venv; dry-run không phải bằng chứng cài đặt sạch. Cần Internet hoặc wheel cache khi cài dependency; ứng dụng local không tải dataset/CDN lúc chạy.

Nếu lỗi import/pin/port/entry point: phân loại `environment`, quay lại INIT của chính task; không sửa thuật toán hay expected output để bỏ qua lỗi. Không có lỗi dependency đang mở sau các lệnh trên.
