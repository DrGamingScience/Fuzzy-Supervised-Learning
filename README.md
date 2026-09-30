# Dự án sSMC-FCM

Workspace này chuẩn bị cho việc hiện thực thuật toán **Semi-Supervised Fuzzy C-Means Clustering with Multiple Fuzzification Coefficients (sSMC-FCM)**.

Ba thuật toán **FCM, sSFCM và sSMC-FCM** đã được hiện thực bằng NumPy trong
`src/fuzzy_supervised_learning/`, kèm kiểm thử mức phương trình và end-to-end.

## Cài đặt và chạy nhanh

```bash
python -m pip install -e ".[dashboard]"
python -m unittest discover -s tests -v
```

Khởi động dashboard:

```bash
python -m streamlit run dashboard/app.py
```

Dashboard hỗ trợ dữ liệu mẫu hoặc CSV, gán mẫu giám sát, chạy riêng từng thuật
toán hoặc so sánh cả ba, theo dõi hội tụ và tải kết quả membership dưới dạng CSV.

```python
import numpy as np
from fuzzy_supervised_learning import FCM, SSFCM, SSMCFCM

X = np.array([[0.0, 0.0], [0.2, 0.1], [4.9, 5.0], [5.1, 4.8]])

fcm = FCM(n_clusters=2, random_state=0).fit(X)

# sSFCM: U_bar[i, k] là độ thuộc giám sát tối thiểu.
U_bar = np.zeros((len(X), 2))
U_bar[0, 0] = 0.6
ssfcm = SSFCM(n_clusters=2, random_state=0).fit(X, U_bar)

# sSMC-FCM: -1 là không nhãn; số còn lại là chỉ số cụm đích (0-based).
targets = np.array([0, -1, 1, -1])
ssmc = SSMCFCM(
    n_clusters=2,
    fuzzifier=2.0,
    supervised_fuzzifier=4.0,
    random_state=0,
).fit(X, targets)

print(ssmc.cluster_centers_)
print(ssmc.membership_)
```

## Bắt đầu từ đâu?

Đọc theo thứ tự:

1. [Đặc tả kỹ thuật](docs/specifications/ptyc.md)
2. [Product backlog](docs/specifications/product-backlog.md)
3. Các bản TXT trong [papers/text](papers/text/) khi cần tìm kiếm nhanh
4. PDF gốc trong [papers/pdf](papers/pdf/) khi cần kiểm tra công thức, bảng hoặc hình

## Cấu trúc thư mục

    .
    ├── README.md
    ├── dashboard/
    │   └── app.py                    # Giao diện Streamlit
    ├── docs/
    │   ├── project-brief.md
    │   ├── specifications/           # Đặc tả và backlog
    │   └── research/                 # Tài liệu phân tích và workbook
    ├── papers/
    │   ├── pdf/                      # Bài báo gốc
    │   └── text/                     # Text đã trích xuất
    ├── reports/
    │   ├── pdf/                      # Báo cáo đã dựng
    │   └── slides/week1/             # Nguồn slide và theme
    ├── artifacts/                    # Kết quả build/trung gian
    ├── scripts/                      # Script tạo artifact
    ├── src/fuzzy_supervised_learning/
    │   ├── fcm.py
    │   ├── ssfcm.py
    │   ├── ssmc_fcm.py
    │   └── dashboard_support.py
    ├── tests/
    │   └── test_algorithms.py
    └── pyproject.toml

`artifacts/` chứa dữ liệu trung gian; `reports/` chỉ chứa đầu ra báo cáo cần giữ lại.

## Vai trò của ba bài báo

| Bài báo | Vai trò |
|---|---|
| *On Semi-Supervised Fuzzy c-Means Clustering* | Định nghĩa sSFCM, baseline bán giám sát |
| *A Novel Semi-Supervised Fuzzy C-Means Clustering Algorithm Using Multiple Fuzzification Coefficients* | Định nghĩa thuật toán đích sSMC-FCM |
| *Relative Clustering Validity Criteria: A Comparative Overview* | Tổng quan các chỉ số đánh giá phân cụm |

## Khác biệt cốt lõi

- **FCM:** dùng một hệ số mờ hóa chung.
- **sSFCM:** đưa ma trận độ thuộc giám sát vào hàm mục tiêu.
- **sSMC-FCM:** dùng hệ số mờ hóa lớn hơn tại cặp mẫu-cụm được giám sát.

Phần khó nhất khi hiện thực sSMC-FCM là giải số Phương trình (19) cho từng mẫu được giám sát.

## Những điểm chưa được bài báo quy định đầy đủ

- cách khởi tạo tâm cụm;
- loại norm dùng trong điều kiện dừng;
- tolerance, bước tăng và cận của solver Phương trình (19);
- xử lý khoảng cách bằng 0;
- xử lý cụm có tổng trọng số bằng 0;
- nhiều cụm đích cho cùng một mẫu;
- tính đơn điệu toàn cục khi tìm hệ số M' bằng Phương trình (23).

Các điểm này được đánh dấu **[CẦN XÁC MINH]** trong
[đặc tả kỹ thuật](docs/specifications/ptyc.md).

## Backlog

Backlog có 37 hạng mục, chia thành 7 milestone:

1. Hiểu và chuẩn hóa bài báo
2. FCM baseline
3. sSFCM baseline
4. Lõi sSMC-FCM
5. Chỉ số đánh giá
6. Thí nghiệm
7. Kiểm chứng

Điểm bắt đầu lập trình được khuyến nghị là **PB-06 - Khởi tạo package, kiểu dữ liệu và validation**.

## Nguyên tắc khoa học

- Không tự suy đoán công thức bị thiếu.
- Khi TXT làm mất định dạng, phải đối chiếu PDF.
- Tách rõ dữ kiện trong bài báo và quyết định kỹ thuật.
- Không coi một biến thể FCM phổ biến trên Internet là sSMC-FCM của bài báo.
- Tái lập Table II và Table 3 trước khi mở rộng thí nghiệm.
- Mọi kết quả phải lưu seed, initialization, tolerance và cấu hình solver.

## Trạng thái hiện tại

- [x] Trích xuất ba PDF thành TXT
- [x] Xác định vai trò từng bài báo
- [x] Đối chiếu các công thức trọng yếu
- [x] Hoàn thành đặc tả kỹ thuật
- [x] Hoàn thành product backlog
- [ ] Chốt các quyết định kỹ thuật còn mở
- [x] Hiện thực FCM
- [x] Hiện thực sSFCM
- [x] Hiện thực sSMC-FCM
- [x] Dashboard tương tác và so sánh ba thuật toán
- [x] Hệ thống hóa cấu trúc thư mục
- [ ] Tái lập kết quả bài báo

