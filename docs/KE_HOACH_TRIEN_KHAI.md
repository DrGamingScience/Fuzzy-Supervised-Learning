# Kế hoạch tái hiện phân cụm mờ bán giám sát

Ngày khảo sát: 09/11/2026. Phạm vi hiện tại: đọc tài liệu, kiểm tra công thức và đề xuất triển khai; chưa xây dựng ứng dụng.

## 1. Kết luận và phạm vi đề xuất

Nên xây dựng một phần mềm thực nghiệm: nạp dữ liệu, cung cấp một phần thông tin giám sát, chạy các thuật toán, xem diễn biến hội tụ và so sánh kết quả. Thứ tự thực hiện là **thuật toán → tái hiện ví dụ → đánh giá → giao diện → thực nghiệm mở rộng**.

Phần cốt lõi gồm FCM làm đối chứng, sSFCM và eSFCM của bài 2009, sSMC-FCM của bài 2021. Để bao phủ bài 2009 cần cả nhánh sSFCM m = 1 và m > 1. Bài metrics 2010 là một hướng thực nghiệm riêng về độ đo, không phải thuật toán phân cụm thứ ba.

Phiên bản đầu nên có đủ các thuật toán trên cùng một nhóm metrics đại diện. Nếu yêu cầu của môn học là tái hiện toàn bộ bài metrics, cần mở thêm danh mục đủ 40 tiêu chí và quy trình so sánh của bài; không được gọi phiên bản chỉ có vài metrics là tái hiện trọn vẹn nghiên cứu này.

## 2. Vai trò của ba tài liệu

| Tài liệu | Nội dung cần chuyển thành chương trình |
| --- | --- |
| Endo và cộng sự, *On Semi-Supervised Fuzzy c-Means Clustering*, 2009, 6 trang | sSFCM, gồm m > 1 và m = 1; eSFCM dùng entropy; bộ 20 điểm 2D, ba mức giám sát 0 / 0.3 / 0.6; Tables I–V. |
| Khang, Tran, Fowler, *A Novel Semi-Supervised Fuzzy C-Means Clustering Algorithm Using Multiple Fuzzification Coefficients*, 2021, 12 trang | sSMC-FCM dùng M và M'; cách cập nhật độ thuộc bằng giải phương trình; điều kiện chọn M' theo ngưỡng alpha; ví dụ cùng 20 điểm, M = 2 và M' = 4 / 8. |
| Vendramin, Campello, Hruschka, *Relative Clustering Validity Criteria: A Comparative Overview*, 2010, 27 trang | 40 tiêu chí tương đối, độ phức tạp, Rand / ARI / Jaccard theo cặp; phương pháp so sánh độ đo qua tương quan với đánh giá ngoài. |

Bài 2021 tham chiếu trực tiếp cả bài gốc 2009 và bài metrics 2010. Hai bài thuật toán dùng chung bộ ví dụ nên rất thuận lợi cho kiểm chứng.

## 3. Chuẩn hóa ký hiệu và công thức trước khi viết mã

Quy ước thống nhất trong mã: X có kích thước N × D; U có kích thước N × C; V có kích thước C × D. Bài 2009 dùng chỉ số điểm k, cụm i, trong khi bài 2021 dùng điểm i, cụm k. Cần chuyển đổi nhất quán để tránh lỗi chuyển vị.

U là **độ thuộc mờ**, không mặc nhiên là xác suất đã hiệu chuẩn. Mỗi hàng U không âm và có tổng bằng 1. Nhãn cứng được suy ra bằng argmax trên từng hàng.

### FCM làm thuật toán đối chứng

- Hàm mục tiêu: J = sum_ik U_ik^m ||X_i - V_k||².
- Cập nhật U và V theo (2), (3) của bài 2021; m > 1.
- Lưu U, V, J, độ dịch chuyển tâm, số vòng lặp và thời gian.
- Đây là trường hợp không giám sát để đối chiếu với các mở rộng.

### sSFCM của bài 2009

- Đầu vào giám sát là ma trận B, tương ứng với U có gạch trên trong bài; 0 ≤ B_ik ≤ 1 và tổng hàng ≤ 1.
- Hàm mục tiêu: J = sum_ik |U_ik - B_ik|^m ||X_i - V_k||², công thức (2).
- Với m > 1: U_ik = B_ik + (1 - sum_j B_ij) × U_FCM,ik, công thức (6).
- Tâm cụm dùng trọng số |U_ik - B_ik|^m, công thức (4). Không được dùng nhầm trọng số U_ik^m của FCM.
- Với m = 1: phân bổ phần độ thuộc còn lại cho cụm gần nhất theo (8); cần nhánh riêng, không đưa m = 1 vào công thức có 1/(m - 1).
- B_ik = 0 nghĩa là không cung cấp mức giám sát ở ô đó, không phải cấm điểm vào cụm k.
- B_ik là cận dưới trong công thức cập nhật, không phải độ thuộc cuối cùng bắt buộc bằng đúng B_ik.
- Khi tổng một hàng B bằng 1, hàng U bị cố định và trọng số phần dư của điểm đó bằng 0; cần giải thích rõ và xử lý mẫu số tâm cụm bằng 0.

### eSFCM của bài 2009

- Hàm mục tiêu gồm sai số khoảng cách có trọng số U và hạng entropy của |U - B|, công thức (9).
- Cập nhật độ thuộc theo (14): B cộng phần dư nhân softmax(-lambda × khoảng cách bình phương).
- Tâm cụm dùng trọng số U, công thức (10), khác cả FCM lẫn sSFCM.
- lambda > 0; tính softmax ổn định bằng cách trừ giá trị lớn nhất của các logit; quy ước 0 log 0 = 0 khi tính hàm mục tiêu.
- Cần ghi nhận riêng vấn đề tái hiện số liệu eSFCM ở mục 4.

### sSMC-FCM của bài 2021

- Hàm mục tiêu: J = sum_ik U_ik^(m_ik) ||X_i - V_k||², công thức (7).
- M > 1 là hệ số thông thường. Với điểm i được giám sát vào cụm k, đặt m_ik = M' > M; các ô khác dùng M, theo (8).
- Điểm không giám sát cập nhật U như FCM theo (15).
- Điểm giám sát: chuẩn hóa khoảng cách theo (17), tính các mu không giám sát theo (18), giải phương trình một ẩn (19), chuẩn hóa theo (20).
- Tâm cụm dùng trọng số U_ik^(m_ik), công thức (10).
- Dùng giải nghiệm có khoảng chặn, chẳng hạn chia đôi hoặc Brent, kèm kiểm tra sai số và giới hạn số bước. Không thay bằng ép nhãn sau khi FCM chạy xong.
- Tách hai chế độ: nhập M' cố định để tái hiện Tables 3; hỗ trợ chọn M' theo alpha bằng điều kiện (23) ở bước mở rộng.
- Điều kiện alpha phụ thuộc khoảng cách ở trạng thái đang xét. Không mặc nhiên bảo đảm một M' được chọn một lần sẽ duy trì cùng cận dưới sau mọi lần cập nhật tâm.
- Đặc tả trước mỗi điểm có tối đa một cụm đích trong nhánh tái hiện bài. Không tự mở rộng thành nhiều chỉ dẫn mâu thuẫn hoặc ràng buộc must-link/cannot-link.
- Không tăng M' tùy ý theo từng vòng rồi dùng lịch sử J như thể đang tối ưu cùng một hàm mục tiêu cố định.

### Các trường hợp số học bắt buộc xử lý

- Khoảng cách bằng 0, nhiều tâm trùng một điểm, các điểm trùng nhau.
- Cụm rỗng, tổng trọng số tâm bằng hoặc gần 0.
- Mẫu số bằng 0, số mũ lớn, underflow/overflow, dữ liệu NaN/Inf.
- Tiêu chí dừng epsilon, chuẩn đo độ dịch chuyển tâm, số vòng lặp tối đa, dung sai giải nghiệm.
- Seed và tâm khởi tạo có thể nhập/lưu để tái lập và so sánh công bằng.

## 4. Mốc kiểm chứng và sai khác đã phát hiện

Đã tính thử độc lập bằng NumPy/SciPy trên đúng 20 điểm của Table I (2009) / Table 1 (2021), với tâm đầu (2.7, 5) và (9.1, 5), không chuẩn hóa dữ liệu. Đây là phép đối chiếu nghiên cứu, chưa phải thư viện thuật toán hay bộ kiểm thử của dự án.

| Thuật toán | Cấu hình | Độ thuộc của điểm 9 vào cụm 1 tính thử | Bảng bài báo |
| --- | --- | --- | --- |
| FCM | m = 2 | 0.188663 | 0.19 |
| sSFCM | m = 2, B_9,1 = B_10,1 = 0.3 | 0.451669 | 0.45 |
| sSFCM | m = 2, B_9,1 = B_10,1 = 0.6 | 0.693818 | 0.69 |
| sSMC-FCM | M = 2, M' = 4 | 0.428699 | 0.43 |
| sSMC-FCM | M = 2, M' = 8 | 0.604491 | 0.60 |

Điểm 10 cho cùng kết quả do tính đối xứng. Hai điểm chuyển sang cụm 1 khi độ thuộc cụm 1 lớn hơn cụm 2; việc tăng mức giám sát chưa chắc đã đủ để đổi nhãn.

**Sai khác cần ghi nhận, không sửa công thức để chạy theo bảng:**

1. Table V bài 2009 ghi tâm FCM không giám sát thứ hai xấp xỉ (9.08, 5). Tính theo công thức thu được (9.017398, 5), phù hợp giá trị xấp xỉ (9.018, 5) của bài 2021.
2. Table IV bài 2009 ghi eSFCM với lambda = 1 có U_1 = (0.76, 0.24), và Table V ghi tâm (4.60, 5), (8.33, 5). Thay trực tiếp các tâm này và X_1 = (0, 4.5) vào (14), B = 0, cho độ thuộc cụm 2 khoảng 1.13 × 10^-21, không phải 0.24. Vì vậy các số liệu này không thể đồng thời thỏa công thức và tham số được công bố. Cần kiểm tra thêm giả thiết về thang dữ liệu, lambda hoặc lỗi in; hiện chưa xác định nguyên nhân.

Hai bài chưa cung cấp đầy đủ mọi thiết lập để cam kết số vòng lặp giống hệt. Mốc nghiệm thu cần dựa trên công thức, ràng buộc U, sai số nghiệm, độ thuộc/tâm sau khi ghép đúng cụm và mức làm tròn; không yêu cầu bằng từng bit hoặc bằng chính xác số vòng lặp của bài.

## 5. Thiết kế phần đánh giá

### Nhóm triển khai đầu tiên

| Metric | Dữ liệu đầu vào | Chiều tốt |
| --- | --- | --- |
| Silhouette / SWC | X và nhãn cụm cứng | Lớn |
| Calinski–Harabasz / VRC | X và nhãn cụm cứng | Lớn |
| Davies–Bouldin | X và nhãn cụm cứng | Nhỏ |
| Dunn nguyên bản | X và nhãn cụm cứng | Lớn |
| PBM | X và nhãn cụm cứng | Lớn |
| Adjusted Rand Index / ARI | Nhãn thật và nhãn cụm cứng | Lớn |
| Jaccard theo cặp điểm | Nhãn thật và nhãn cụm cứng | Lớn |

Đây là lựa chọn triển khai đề xuất, không phải kết luận rằng bảy metric này tốt nhất trên mọi dữ liệu. Nghiên cứu 2010 báo cáo kết quả tốt của các biến thể silhouette, PBM, VRC và point-biserial trong các kịch bản dữ liệu của nghiên cứu; kết luận có giới hạn theo dạng cụm/dữ liệu.

- Bài metrics đánh giá phân hoạch cứng. Với FCM và các mở rộng, lấy nhãn bằng argmax U và vẫn lưu U để người dùng xem tính mờ. Chỉ số tính trên nhãn cứng không đánh giá toàn bộ thông tin mờ.
- Jaccard trong bài là a/(a+b+c) trên **các cặp điểm**, không phải Jaccard phân loại tính trực tiếp trên dãy mã cụm.
- Khi không có nhãn thật, không hiển thị ARI/Jaccard như một kết quả hợp lệ.
- ARI/Jaccard không phụ thuộc tên mã cụm. Nếu bổ sung accuracy thì phải ghép cụm với lớp; không so sánh trực tiếp mã cụm và mã lớp.
- Tâm dùng cho các metric phân hoạch cứng được tính theo đúng định nghĩa metric từ các nhóm điểm; không tự thay bằng tâm mờ V.
- J của các thuật toán khác nhau có định nghĩa khác nhau. Dùng để theo dõi hội tụ từng thuật toán, không chọn thuật toán tốt nhất bằng cách so trực tiếp các J.
- Tính metric trong không gian đặc trưng đã dùng để phân cụm. PCA 2D/3D mặc định chỉ dùng hiển thị, trừ khi người dùng chủ động chọn phân cụm trên PCA.
- Phân biệt một cụm có trọng số mờ dương với việc nó có điểm được gán bằng argmax hay không. Kiểm tra số cụm cứng thực tế trước khi tính metric.
- Các metric không xác định phải trả trạng thái và nguyên nhân, không âm thầm thay bằng 0. Quy định rõ cụm singleton, tâm trùng, đường kính bằng 0 và số cụm không hợp lệ.

### Nếu tái hiện trọn bài metrics

- Lập danh mục 40 tiêu chí kèm tên, biến thể, công thức, điều kiện xác định, chiều tối ưu và độ phức tạp: 31 tiêu chí optimization-like, bao gồm Dunn gốc và 17 biến thể, cùng 9 tiêu chí difference-like.
- Bổ sung các biến thể silhouette, point-biserial, C-index, Gamma, G(+), Tau, C/sqrt(k) và các tiêu chí ma trận/độ phân tán còn lại theo bài.
- Với difference-like, triển khai biến đổi (37) có dùng các mức k-1, k, k+1 và xử lý biên. Bài không áp dụng nhóm này trong thí nghiệm k-means độc lập vì thiếu quan hệ kế tiếp phân cấp; không tự gắn chúng vào các lần chạy FCM độc lập rồi coi là tái hiện nguyên bản.
- So sánh độ đo bằng nhiều phân hoạch có chất lượng và số cụm khác nhau, sau đó đo tương quan giữa từng metric nội tại và ARI/Jaccard. Đổi chiều metric tối thiểu hóa trước khi tính tương quan.
- Tái hiện đầy đủ thực nghiệm còn gồm sinh dữ liệu, các thuật toán phân cụm dùng trong bài và đánh giá thống kê. Quy mô bài là 1.080 bộ dữ liệu và 962.928 phân hoạch; đây là khối lượng riêng so với việc lập trình các công thức metric.
- Silhouette và Dunn nguyên bản cần tính khoảng cách theo cặp, có chi phí thời gian bậc hai theo N. Bổ sung SSWC cho dữ liệu lớn; nếu lấy mẫu thì ghi rõ đang tính xấp xỉ. Không cấp phát ma trận N × N mà không kiểm tra kích thước.

## 6. Giao thức thực nghiệm đề xuất

1. **Tái hiện giấy:** bộ 20 điểm, không chuẩn hóa, 2 cụm, đủ cấu hình của hai bài; hiển thị điểm 9 và 10 nổi bật; so bảng U và tâm.
2. **Kiểm tra dữ liệu tổng hợp:** cụm tách biệt, chồng lấn, mất cân bằng, điểm trùng, nhiễu; dùng để kiểm tra giới hạn và độ ổn định, không gán thành thực nghiệm có sẵn trong bài.
3. **Đánh giá mở rộng:** thêm bộ dữ liệu dạng bảng có nhãn, chẳng hạn Iris/Wine, cùng dữ liệu CSV người dùng. Ghi rõ đây là mở rộng ngoài hai ví dụ thuật toán gốc.
4. **Mức giám sát:** thử 0%, 5%, 10%, 20%, 30% số điểm, lấy mẫu theo lớp khi phù hợp; đây là thiết kế đề xuất, không phải tham số báo cáo gốc.
5. **So sánh công bằng:** dùng cùng dữ liệu, phép tiền xử lý, tâm đầu, seed, tập điểm được tiết lộ nhãn và ánh xạ cụm đích. Mức B và M' không có quy đổi tương đương mặc định.
6. **Tránh rò rỉ nhãn:** cột nhãn thật không nằm trong X; thuật toán chỉ nhận phần giám sát đã tiết lộ. Báo cáo chỉ số ngoài trên các điểm chưa được giám sát, có thể kèm toàn bộ dữ liệu ở cột riêng.
7. **Lặp lại:** dùng nhiều seed, gợi ý 10–30 lần cho benchmark nhỏ; báo trung bình, độ lệch chuẩn và thời gian. Tách biến thiên khởi tạo khỏi biến thiên tập giám sát khi cần phân tích.
8. **Lưu kết quả:** dữ liệu/định danh dữ liệu, cấu hình, seed, preprocessing, chỉ dẫn giám sát, U, V, nhãn, metrics, lịch sử hội tụ, thời gian, trạng thái dừng. Không chọn tham số theo kết quả trên tập đánh giá cuối rồi báo là kết quả độc lập.

Các thuật toán này phân cụm trên tập dữ liệu được đưa vào chạy. Nếu cần phân loại điểm mới sau huấn luyện, phải đặc tả một luồng suy luận riêng.

## 7. Giao diện đề xuất

Luồng chính: **Chọn dữ liệu → chọn đặc trưng/tiền xử lý → cung cấp giám sát → cấu hình → chạy → xem/so sánh → xuất**.

- Dữ liệu: preset 20 điểm, CSV, chọn cột đặc trưng và cột nhãn tùy chọn; xem lỗi thiếu/không phải số; bật/tắt chuẩn hóa. Chế độ tái hiện bài dùng dữ liệu gốc.
- Giám sát: chọn điểm trên biểu đồ hoặc theo ID trong bảng; nhập cụm đích; nhập B cho sSFCM/eSFCM hoặc M' cho sSMC-FCM. Có cách xem/xóa chỉ dẫn và nhận biết điểm đã được giám sát.
- Cấu hình: thuật toán, C, m hoặc M/M', lambda theo thuật toán, epsilon, max_iter, seed, tâm đầu; không hiển thị tham số không áp dụng.
- Kết quả: biểu đồ 2D/3D, tâm cụm, ký hiệu điểm giám sát, bảng/heatmap U, nhãn cứng, metrics với mũi tên chiều tốt, số vòng, thời gian và lý do dừng.
- Diễn biến: đường J theo vòng lặp, độ dịch chuyển tâm, chọn vòng lặp để xem U/V đã lưu. Giải thích tên và ý nghĩa tham số bằng tiếng Việt.
- So sánh: các thuật toán trên cùng điều kiện đầu vào; phân biệt cải thiện nhãn với cải thiện độ compact/tách biệt hình học.
- Xuất: CSV cho nhãn và U; JSON cho cấu hình/kết quả; hình biểu đồ cho báo cáo.

## 8. Công nghệ và cấu trúc đề xuất

Với mục đích học thuật và trình diễn trên máy cá nhân, đề xuất Python + NumPy/SciPy cho tính toán, pandas cho dữ liệu, Plotly cho biểu đồ và Streamlit cho giao diện chạy qua trình duyệt cục bộ. Đây là lựa chọn kiến trúc đề xuất; chưa có yêu cầu từ người dùng về ứng dụng desktop hay triển khai nhiều người dùng.

Streamlit có hỗ trợ sự kiện chọn điểm/vùng trên Plotly. SciPy có brentq để giải nghiệm một chiều trong khoảng có đổi dấu. Khi triển khai cần khóa phiên bản tương thích và kiểm tra khoảng chặn, không mặc nhiên gọi solver là đủ bảo đảm thuật toán đúng.

Thuật toán phải tách khỏi giao diện để có thể kiểm thử và chạy benchmark độc lập. Tự viết các cập nhật của bài báo; có thể dùng thư viện để đối chiếu FCM/metrics. Với metrics có định nghĩa/biến thể riêng trong bài, cần kiểm tra công thức thay vì chỉ dựa vào tên hàm thư viện.

```text
src/
  algorithms/       # FCM, sSFCM (m>1/m=1), eSFCM, sSMC-FCM
  metrics/          # internal, external, metric registry
  data/             # preset 20 điểm, nạp CSV, preprocessing
  experiments/      # cấu hình, chạy lặp, tổng hợp, xuất kết quả
  ui/               # giao diện và trực quan hóa
tests/              # tính đúng của thuật toán, bài báo, các metric thiết yếu
results/            # đầu ra thực nghiệm có thể tái lập
docs/               # tài liệu gốc và đặc tả
```

Tài liệu công nghệ đã đối chiếu:

- https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html

## 9. Các mốc thực hiện và nghiệm thu

| Mốc | Công việc | Điều kiện hoàn thành |
| --- | --- | --- |
| 1. Đặc tả | Chốt công thức, ký hiệu, phạm vi thuật toán/metric, dữ liệu và quy tắc giám sát | Có bảng ánh xạ công thức → hàm mã, ghi nhận sai khác số liệu nguồn |
| 2. Lõi thuật toán | FCM → sSFCM → sSMC-FCM → eSFCM; nhánh m = 1 của sSFCM | U hợp lệ; các trường hợp không giám sát thu về baseline tương ứng; ví dụ 20 điểm khớp trong dung sai hợp lý; sai khác eSFCM được báo minh bạch |
| 3. Metrics và benchmark | Bảy metrics ban đầu, thiết kế chạy nhiều seed và nhiều mức giám sát | Metrics đúng định nghĩa; hoán vị tên cụm không đổi ARI/Jaccard; không đưa nhãn thật vào đặc trưng; lưu đủ cấu hình |
| 4. Giao diện | Nạp dữ liệu, nhập giám sát, chạy, xem U/V/metrics/hội tụ, so sánh, xuất | Có thể thao tác toàn bộ luồng với preset và CSV; dữ liệu hiển thị khớp kết quả lõi |
| 5. Mở rộng và báo cáo | Dữ liệu ngoài ví dụ, đủ 40 metrics nếu được yêu cầu, phương pháp so sánh metrics | Báo cáo tách kết quả tái hiện khỏi mở rộng; nêu giới hạn, thiết lập và sai khác với bài |

Đề xuất bắt đầu mốc 1–2 bằng bộ 20 điểm và ba thuật toán FCM, sSFCM, sSMC-FCM đã có mốc đối chiếu rõ; giải quyết eSFCM trước khi nghiệm thu đầy đủ bài 2009. Giao diện được phát triển sau khi phần lõi đã kiểm chứng.
