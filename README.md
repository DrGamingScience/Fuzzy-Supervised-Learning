# Dự án sSMC-FCM

Workspace này chuẩn bị cho việc hiện thực thuật toán **Semi-Supervised Fuzzy C-Means Clustering with Multiple Fuzzification Coefficients (sSMC-FCM)**.

Hiện tại dự án mới hoàn thành giai đoạn khảo sát, đặc tả và lập backlog. **Chưa có mã hiện thực sSMC-FCM.**

## Bắt đầu từ đâu?

Đọc theo thứ tự:

1. [Đặc tả kỹ thuật](docs/ptyc.md)
2. [Product backlog](docs/product-backlog.md)
3. Các bản TXT trong [papers/text](papers/text/) khi cần tìm kiếm nhanh
4. PDF gốc trong [papers/pdf](papers/pdf/) khi cần kiểm tra công thức, bảng hoặc hình

## Cấu trúc thư mục

    .
    ├── README.md
    ├── description.md
    ├── docs/
    │   ├── ptyc.md
    │   └── product-backlog.md
    ├── papers/
    │   ├── pdf/
    │   │   ├── algorithms-14-00258-v2.pdf
    │   │   ├── FCM Bán giám sát - yasunori2009.pdf
    │   │   └── Relative Clustering Validity Criteria A Comparative Overview 2010.pdf
    │   └── text/
    │       ├── novel-semi-supervised-fcm-multiple-fuzzification-coefficients.txt
    │       ├── on-semi-supervised-fuzzy-c-means-clustering.txt
    │       └── relative-clustering-validity-criteria-comparative-overview.txt
    └── tmp/
        └── pdfs/
            └── rendered/

Thư mục tmp/ chứa dữ liệu trung gian dùng để kiểm tra trực quan PDF; không phải đầu ra chính.

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

Các điểm này được đánh dấu **[CẦN XÁC MINH]** trong [docs/ptyc.md](docs/ptyc.md).

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
- [ ] Hiện thực FCM
- [ ] Hiện thực sSFCM
- [ ] Hiện thực sSMC-FCM
- [ ] Tái lập kết quả bài báo

