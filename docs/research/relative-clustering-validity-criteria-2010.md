# Phân tích bài báo *Relative Clustering Validity Criteria: A Comparative Overview* (2010)

## 1. Thông tin bài báo

- **Tên:** *Relative Clustering Validity Criteria: A Comparative Overview*
- **Tác giả:** Lucas Vendramin, Ricardo J. G. B. Campello và Eduardo R. Hruschka
- **Năm:** 2010
- **Tạp chí:** *Statistical Analysis and Data Mining*, tập 3, trang 209-235
- **DOI:** 10.1002/sam.10080
- **PDF trong dự án:** [Relative Clustering Validity Criteria A Comparative Overview 2010.pdf](<../../papers/pdf/Relative Clustering Validity Criteria A Comparative Overview 2010.pdf>)
- **Vai trò trong dự án:** cung cấp cơ sở lựa chọn và hiện thực các chỉ số đánh giá phân cụm cho FCM, sSFCM và sSMC-FCM.

## 2. Bài báo này nghiên cứu điều gì?

Bài báo nghiên cứu các **relative clustering validity criteria**, tức các tiêu chuẩn đánh giá chất lượng của một phân hoạch chỉ dựa trên dữ liệu và kết quả phân cụm, không cần biết nhãn thật khi sử dụng.

Một tiêu chuẩn loại này thường đánh giá hai đặc tính:

1. **Cohesion/compactness:** các điểm trong cùng cụm phải gần nhau.
2. **Separation:** các cụm khác nhau phải cách xa nhau.

Các tiêu chuẩn relative có thể được dùng để:

- so sánh nhiều kết quả phân cụm của cùng một tập dữ liệu;
- chọn số cụm `C`;
- chọn một lần khởi tạo tốt trong nhiều lần chạy;
- so sánh các thuật toán hoặc cấu hình tham số khác nhau khi không có nhãn thật.

Bài báo không chỉ tổng hợp công thức. Ba đóng góp chính của nó là:

1. tổng quan **40 tiêu chuẩn relative**;
2. phân tích độ phức tạp tính toán của từng tiêu chuẩn;
3. đề xuất một phương pháp thực nghiệm mới để so sánh độ tin cậy của các tiêu chuẩn trên toàn bộ tập phân hoạch, thay vì chỉ xét tiêu chuẩn có chọn đúng số cụm hay không.

## 3. Vì sao cần nghiên cứu này?

### 3.1 Số cụm thường không biết trước

Các thuật toán như K-Means, FCM và sSMC-FCM thường yêu cầu số cụm `C` trước khi chạy. Trong dữ liệu thực tế, `C` thường chưa biết và khó xác định bằng quan sát, đặc biệt khi dữ liệu có nhiều chiều.

Cách làm phổ biến là:

1. chạy thuật toán với nhiều giá trị `C`;
2. tạo nhiều phân hoạch ứng viên;
3. tính một chỉ số validity cho mỗi phân hoạch;
4. chọn phân hoạch có giá trị tốt nhất.

Vấn đề là có rất nhiều chỉ số validity và chúng không luôn đồng ý với nhau.

### 3.2 Chọn đúng số cụm chưa chắc đã tạo ra phân hoạch tốt

Phương pháp đánh giá truyền thống thường xem một tiêu chuẩn là tốt nếu nó chọn được phân hoạch có đúng số cụm thật `k*`.

Bài báo chỉ ra rằng lập luận này chưa đủ:

- có thể có một phân hoạch với đúng `k*` nhưng các điểm bị nhóm rất phi tự nhiên;
- có thể có một phân hoạch với `k* + 1` cụm nhưng vẫn phản ánh cấu trúc dữ liệu khá tốt, chẳng hạn một vài ngoại lệ được tách thành cụm nhỏ;
- sai lệch `|k-k*|` không phản ánh trực tiếp mức độ sai của cấu trúc phân hoạch;
- chỉ kiểm tra phân hoạch được chọn tốt nhất sẽ bỏ qua khả năng của metric trong việc xếp hạng tất cả các phân hoạch còn lại.

Do đó, một metric tốt không chỉ phải chọn một giá trị `C` hợp lý, mà còn nên xếp các phân hoạch từ xấu đến tốt gần giống với một tiêu chuẩn ngoại tại đáng tin cậy.

## 4. Ý tưởng phương pháp mới của bài báo

Giả sử một tập dữ liệu có nhãn thật chỉ để phục vụ nghiên cứu đánh giá metric. Với tập dữ liệu đó, ta tạo nhiều phân hoạch ứng viên có chất lượng và số cụm khác nhau.

Với mỗi phân hoạch `P_r`, tính:

- một giá trị relative validity, ví dụ Silhouette;
- một giá trị external validity, ví dụ ARI hoặc Jaccard, sử dụng nhãn thật.

Ta thu được hai chuỗi:

```text
relative_scores = [R(P1), R(P2), ..., R(Pm)]
external_scores = [E(P1), E(P2), ..., E(Pm)]
```

Sau đó tính tương quan giữa hai chuỗi. Nếu tương quan cao, metric relative có xu hướng xếp hạng các phân hoạch giống với đánh giá dựa trên nhãn thật.

Quy trình tổng quát của bài báo:

1. Chuẩn bị nhiều tập dữ liệu có cấu trúc cụm đã biết.
2. Với mỗi tập dữ liệu, tạo nhiều phân hoạch có chất lượng và số cụm khác nhau.
3. Tính tất cả relative score và external score cho từng phân hoạch.
4. Với mỗi relative criterion, tính tương quan giữa chuỗi relative score và external score.
5. Lặp lại trên nhiều tập dữ liệu.
6. So sánh phân phối các hệ số tương quan bằng kiểm định thống kê.

Bài báo dùng:

- **external criteria:** Adjusted Rand Index và Jaccard;
- **correlation:** Pearson và Weighted Goodman-Kruskal;
- **statistical tests:** Wilcoxon/Mann-Whitney và Friedman.

Đối với metric có chiều “thấp hơn là tốt hơn”, chẳng hạn Davies-Bouldin, C-index hoặc G(+), giá trị phải được đổi chiều trước khi tính tương quan với external metric có chiều “cao hơn là tốt hơn”.

## 5. Hai nhóm tiêu chuẩn trong bài báo

### 5.1 Optimization-like criteria

Đây là các metric mà một giá trị cực đại hoặc cực tiểu trực tiếp chỉ ra phân hoạch tốt hơn.

| Metric | Chiều tốt | Ý tưởng chính | Độ phức tạp trong bài |
|---|---:|---|---:|
| Calinski-Harabasz/VRC | Lớn | Tỷ lệ phân tán giữa cụm trên phân tán trong cụm | `O(dN)` |
| Davies-Bouldin | Nhỏ | Trung bình trường hợp xấu nhất của tỷ lệ độ phân tán/độ tách cụm | `O(d(N+C^2))` |
| Dunn và 17 biến thể | Lớn | Khoảng cách nhỏ nhất giữa cụm chia đường kính cụm lớn nhất | thường `O(dN^2)` |
| Silhouette/SWC | Lớn | So sánh khoảng cách trong cụm với cụm lân cận gần nhất | `O(dN^2)` |
| Alternative Silhouette/ASWC | Lớn | Biến thể phi tuyến của Silhouette | `O(dN^2)` |
| Simplified Silhouette/SSWC | Lớn | Thay khoảng cách tới mọi điểm bằng khoảng cách tới tâm | `O(dNC)` |
| Alternative Simplified Silhouette/ASSWC | Lớn | Kết hợp ASWC và SSWC | `O(dNC)` |
| PBM | Lớn | Kết hợp độ phân tán toàn cục, trong cụm và khoảng cách tâm lớn nhất | `O(d(N+C^2))` |
| C-index | Nhỏ | So sánh tổng khoảng cách trong cụm với các biên tốt/xấu lý thuyết | `O(N^2(d+log N))` |
| Gamma | Lớn | So sánh cặp khoảng cách đồng thuận và bất đồng | rất lớn, có thành phần bậc bốn |
| G(+) | Nhỏ | Tỷ lệ cặp bất đồng | rất lớn, có thành phần bậc bốn |
| Tau | Lớn | Chuẩn hóa chênh lệch cặp đồng thuận/bất đồng | rất lớn, có thành phần bậc bốn |
| Point-biserial | Lớn | Tương quan giữa khoảng cách và trạng thái cùng/khác cụm | `O(dN^2)` |
| `C/sqrt(k)` | Lớn | Kết hợp tỷ lệ phương sai theo thuộc tính với số cụm | `O(dN)` |

Trong bảng, `N` là số mẫu, `d` là số chiều và `C` là số cụm.

### 5.2 Difference-like criteria

Nhóm này thường tạo một đường cong tăng hoặc giảm đơn điệu theo số cụm. Ta tìm một “knee/elbow” thay vì lấy trực tiếp cực trị.

Chín tiêu chuẩn được khảo sát gồm:

- `trace(W)`;
- `trace(CovW)`;
- `trace(W^-1 B)`;
- `|T|/|W|`;
- `N log(|T|/|W|)`;
- `k^2 |W|`;
- `log(SSB/SSW)`;
- Ball-Hall;
- McClain-Rao.

Bài báo đề xuất chuyển một chuỗi difference-like thành optimization-like:

$$
C_{new}(k)=
\left|
\frac{C_{orig}(k-1)-C_{orig}(k)}
     {C_{orig}(k)-C_{orig}(k+1)}
\right|.
$$

Một đỉnh của `C_new(k)` biểu diễn thay đổi tương đối lớn tại `k`, tức một ứng viên cho số cụm phù hợp.

Nhóm này cần kết quả tại `k-1`, `k` và `k+1`. Vì vậy nó phù hợp hơn khi có một chuỗi phân hoạch liên tiếp theo số cụm; nó không phải lựa chọn đầu tiên cho việc đánh giá một lần chạy sSMC-FCM đơn lẻ.

## 6. Các công thức quan trọng nên dùng trong dự án

Bài báo khảo sát 40 tiêu chuẩn, nhưng không cần hiện thực tất cả ngay. Với sSMC-FCM, bộ tối thiểu hợp lý là Silhouette/SSWC, VRC, PBM và các external metric ARI/Jaccard.

### 6.1 Silhouette Width Criterion - SWC

Với điểm `x_i` thuộc cụm `p`:

- `a(i)`: khoảng cách trung bình từ `x_i` đến các điểm khác trong cùng cụm;
- `b(i)`: khoảng cách trung bình nhỏ nhất từ `x_i` đến một cụm khác.

$$
s(i)=\frac{b(i)-a(i)}{\max(a(i),b(i))},
$$

$$
SWC=\frac{1}{N}\sum_{i=1}^{N}s(i).
$$

Miền giá trị:

$$
SWC\in[-1,1].
$$

Giá trị lớn hơn tốt hơn:

- gần `1`: điểm nằm phù hợp trong cụm;
- gần `0`: điểm nằm ở biên;
- âm: điểm có thể đang ở sai cụm.

SWC gốc có chi phí khoảng `O(dN^2)` vì cần khoảng cách giữa các cặp điểm.

### 6.2 Simplified Silhouette - SSWC

SSWC thay khoảng cách trung bình đến toàn bộ điểm trong một cụm bằng khoảng cách đến tâm cụm:

```text
a(i) = distance(x_i, center_of_assigned_cluster)
b(i) = minimum distance(x_i, any_other_center)
```

Sau đó vẫn dùng:

$$
s(i)=\frac{b(i)-a(i)}{\max(a(i),b(i))}.
$$

Ưu điểm chính là chi phí giảm xuống khoảng:

$$
O(dNC).
$$

Bài báo nhận thấy các simplified silhouettes có hiệu năng tổng thể gần với Silhouette gốc, nên có thể ưu tiên khi dữ liệu lớn.

### 6.3 Calinski-Harabasz - VRC

$$
VRC=
\frac{\operatorname{trace}(B)}{\operatorname{trace}(W)}
\frac{N-C}{C-1},
$$

trong đó:

- `W`: độ phân tán trong cụm;
- `B`: độ phân tán giữa các cụm;
- `N`: số mẫu;
- `C`: số cụm.

Giá trị lớn hơn tốt hơn. VRC nhanh, khoảng `O(dN)`, nhưng kết quả thực nghiệm trong bài cho thấy nó nhạy hơn Silhouette đối với số chiều và số cụm.

### 6.4 Davies-Bouldin - DB

Với mỗi cụm `l`, tìm cụm `m` có tỷ lệ xấu nhất giữa độ phân tán trong cụm và khoảng cách giữa hai tâm:

$$
D_l=
\max_{m\ne l}
\frac{\bar d_l+\bar d_m}{\|v_l-v_m\|}.
$$

Sau đó:

$$
DB=\frac{1}{C}\sum_{l=1}^{C}D_l.
$$

Giá trị nhỏ hơn tốt hơn. DB dễ hiện thực và hữu ích như một chỉ số phụ, nhưng không nằm trong nhóm mạnh nhất tổng thể của bài báo.

### 6.5 PBM

$$
PBM=
\left(
\frac{1}{C}\frac{E_1}{E_C}D_C
\right)^2,
$$

với:

$$
E_1=\sum_i\|x_i-\bar x\|,
$$

$$
E_C=\sum_{k=1}^{C}\sum_{x_i\in C_k}\|x_i-v_k\|,
$$

$$
D_C=\max_{k,l}\|v_k-v_l\|.
$$

PBM lớn hơn tốt hơn. Nó cho kết quả mạnh trong nhiều thí nghiệm của bài báo và có chi phí khoảng `O(d(N+C^2))`.

### 6.6 External metrics

Khi có nhãn thật, nên dùng ARI và Jaccard để đánh giá trực tiếp khả năng khôi phục cấu trúc lớp.

Với các cặp điểm:

- `a`: cùng lớp thật và cùng cụm dự đoán;
- `b`: cùng lớp thật nhưng khác cụm dự đoán;
- `c`: khác lớp thật nhưng cùng cụm dự đoán;
- `d`: khác lớp thật và khác cụm dự đoán.

Jaccard:

$$
Jaccard=\frac{a}{a+b+c}.
$$

Rand Index:

$$
RI=\frac{a+d}{a+b+c+d}.
$$

ARI là phiên bản Rand Index đã hiệu chỉnh theo mức đồng thuận do ngẫu nhiên. ARI bằng `1` khi hai phân hoạch trùng nhau, kỳ vọng gần `0` khi kết quả tương đương ngẫu nhiên và có thể nhận giá trị âm.

ARI và Jaccard không cần căn chỉnh tên cụm vì chúng so sánh quan hệ giữa các cặp điểm, không so trực tiếp mã nhãn.

## 7. Bài báo thực nghiệm như thế nào?

### 7.1 Quy mô chung

Bài báo đánh giá:

- 40 relative criteria;
- 1080 tập dữ liệu tổng hợp;
- 962.928 phân hoạch;
- năm thuật toán sinh phân hoạch: bốn thuật toán phân cụm phân cấp và K-Means.

### 7.2 Phần I

Phần I tái tạo thiết kế thí nghiệm cổ điển của Milligan và Cooper:

- 108 tập dữ liệu;
- `N = 50` mẫu;
- số chiều thuộc `{4, 6, 8}`;
- số cụm thật thuộc `{2, 3, 4, 5}`;
- ba mức cân bằng kích thước cụm;
- bốn thuật toán phân cấp: single, complete, average và Ward linkage.

Bài báo đánh giá cả hai khoảng số cụm ứng viên:

- `C = 2,...,8`;
- `C = 2,...,25`.

### 7.3 Phần II

Phần II dùng các tập dữ liệu lớn và đa dạng hơn:

- 972 tập dữ liệu;
- `N = 500`;
- số chiều thấp `{2,3,4}` hoặc cao `{22,23,24}`;
- số cụm ít `{2,4,6}` hoặc nhiều `{12,14,16}`;
- K-Means với 20 lần khởi tạo cho mỗi giá trị số cụm.

Phần này tạo nhiều phân hoạch có cùng `C` nhưng chất lượng khác nhau, giúp đánh giá khả năng xếp hạng toàn bộ phân hoạch của các metric.

## 8. Kết luận chính của bài báo

Kết quả tổng thể cho lớp dữ liệu được nghiên cứu là:

1. **Silhouette và các biến thể** cho hiệu năng mạnh và ổn định nhất qua nhiều kịch bản.
2. **Simplified Silhouette** có hiệu năng gần Silhouette gốc nhưng rẻ hơn về tính toán, phù hợp dữ liệu lớn.
3. **PBM, VRC và point-biserial** cũng đạt kết quả tốt, nhưng nhạy hơn với số cụm hoặc số chiều.
4. Một số biến thể Dunn tốt hơn Dunn gốc, nhưng chi phí thường cao.
5. Các optimization-like criteria nhìn chung tốt hơn các difference-like criteria trong phương pháp so sánh mới.
6. Một metric có thể hoạt động tốt trong một kịch bản nhưng giảm mạnh khi tập phân hoạch chứa nhiều nghiệm xấu hoặc số cụm ứng viên quá xa số cụm thật.

Giới hạn quan trọng: kết luận thực nghiệm chủ yếu áp dụng cho dữ liệu có các cụm dạng thể tích, phân bố gần chuẩn, khá tách biệt và tương đối “well-behaved”. Không nên mặc định thứ hạng metric giữ nguyên cho cụm phi lồi, dữ liệu chuỗi, manifold hoặc dữ liệu có nhiễu mạnh.

## 9. Áp dụng cho bài toán sSMC-FCM

### 9.1 Đầu ra nào của sSMC-FCM được đưa vào metric?

sSMC-FCM trả về:

- `U`, shape `(N, C)`: ma trận membership mờ;
- `V`, shape `(C, d)`: tâm cụm;
- có thể suy ra nhãn cứng:

```python
labels = U.argmax(axis=1)
```

Các metric trong bài báo 2010 được nghiên cứu cho **phân hoạch cứng**. Vì vậy, để áp dụng trung thành với bài báo:

```text
sSMC-FCM -> U -> argmax theo từng hàng -> hard labels -> validity metric
```

Không được diễn giải SWC, VRC, DB hoặc PBM trong bài báo này là metric đánh giá trực tiếp mức mờ của `U`. Bài báo xem việc đánh giá fuzzy partitions là hướng nghiên cứu tiếp theo.

### 9.2 Ba mục đích đánh giá khác nhau

#### Mục đích A: Chọn số cụm `C`

Chạy sSMC-FCM với:

```text
C in {2, 3, ..., C_max}
```

Với mỗi `C`:

1. chạy nhiều seed;
2. lấy `labels = argmax(U)`;
3. tính SWC hoặc SSWC;
4. dùng VRC và PBM làm chỉ số đối chiếu;
5. chọn `C` tại vùng các metric cùng ủng hộ, không chỉ dựa vào một đỉnh đơn lẻ.

Khuyến nghị ban đầu:

- metric chính: SWC nếu `N` nhỏ/vừa;
- metric chính: SSWC nếu `N` lớn;
- metric phụ: VRC và PBM;
- DB dùng như chẩn đoán bổ sung.

#### Mục đích B: So sánh FCM, sSFCM và sSMC-FCM

Với cùng dữ liệu, cùng `C` và cùng chiến lược khởi tạo:

```text
FCM   -> labels_fcm
sSFCM -> labels_ssfcm
sSMC  -> labels_ssmc
```

Nếu không có nhãn thật, so sánh:

- SWC/SSWC;
- VRC;
- PBM;
- DB;
- objective riêng của từng thuật toán;
- số vòng lặp và thời gian chạy.

Không nên so trực tiếp giá trị objective của FCM, sSFCM và sSMC-FCM như cùng một thang đo, vì ba thuật toán có hàm mục tiêu khác nhau. Objective chỉ nên dùng để theo dõi hội tụ bên trong từng thuật toán.

Nếu có nhãn thật, bổ sung:

- ARI;
- Jaccard theo cặp;
- báo cáo riêng trên toàn bộ dữ liệu và trên phần chưa dùng làm giám sát.

#### Mục đích C: Chọn `M'` và tỷ lệ giám sát

Có thể chạy lưới:

```text
M_prime in {M + delta, 4, 6, 8, ...}
supervision_ratio in {0.05, 0.10, 0.20, ...}
```

Nhưng cần lưu ý một xung đột quan trọng:

- internal metric ưu tiên các cụm chặt và tách biệt về hình học;
- semi-supervision có thể cố ý chuyển một điểm sang cụm đúng theo kiến thức miền dù điểm đó gần tâm khác hơn.

Vì vậy, không nên dùng riêng Silhouette để điều chỉnh `M'`. Nếu có nhãn giữ lại, nên chọn `M'` bằng ARI/Jaccard trên tập validation chưa dùng làm supervision. Internal metric chỉ đóng vai trò cảnh báo cấu trúc cụm bị méo quá mức.

## 10. Quy trình đánh giá đề xuất khi lập trình

### 10.1 Trường hợp có ground truth

Chia nhãn thật thành hai vai trò độc lập:

1. **supervision set:** một phần nhỏ nhãn được đưa vào `Y` để huấn luyện sSMC-FCM;
2. **evaluation set:** phần nhãn còn lại chỉ dùng để đánh giá.

Không dùng cùng một tập nhãn vừa để tạo `Y` vừa để chọn tham số, vì điều đó gây rò rỉ thông tin.

Quy trình:

```text
for each random seed:
    split labeled data into supervision_indices and evaluation_indices

    for each C:
        for each M_prime:
            fit sSMC-FCM on X using supervision_indices
            validate U and convergence
            labels = argmax(U, axis=1)

            compute internal metrics on all X
            compute ARI/Jaccard on evaluation_indices
            save centers, U, labels, objective history and runtime

aggregate scores over seeds
select configuration using held-out external score
report internal and external metrics together
```

Nên báo cáo trung bình và độ lệch chuẩn, hoặc median và khoảng tứ phân vị nếu phân phối lệch.

### 10.2 Trường hợp không có ground truth

Không thể tính ARI hoặc Jaccard có ý nghĩa. Khi đó:

1. tạo nhiều nghiệm ứng viên qua `C`, `M'` và seed;
2. tính SWC/SSWC, VRC, PBM và DB;
3. loại nghiệm vi phạm ràng buộc hoặc không hội tụ;
4. kiểm tra độ ổn định của phân hoạch giữa các seed;
5. kết hợp metric với kiến thức miền thay vì coi một metric là chân lý tuyệt đối.

## 11. Thiết kế module `metrics.py`

API tối thiểu đề xuất:

```python
def hard_labels_from_membership(U: np.ndarray) -> np.ndarray:
    """U: (N, C) -> labels: (N,)"""

def silhouette_score(X: np.ndarray, labels: np.ndarray) -> float:
    """SWC; lớn hơn tốt hơn."""

def simplified_silhouette_score(
    X: np.ndarray,
    labels: np.ndarray,
    centers: np.ndarray,
) -> float:
    """SSWC; lớn hơn tốt hơn."""

def calinski_harabasz_score(X: np.ndarray, labels: np.ndarray) -> float:
    """VRC; lớn hơn tốt hơn."""

def davies_bouldin_score(X: np.ndarray, labels: np.ndarray) -> float:
    """DB; nhỏ hơn tốt hơn."""

def pbm_score(
    X: np.ndarray,
    labels: np.ndarray,
    centers: np.ndarray,
) -> float:
    """PBM; lớn hơn tốt hơn."""

def adjusted_rand_index(y_true: np.ndarray, labels: np.ndarray) -> float:
    """External; lớn hơn tốt hơn."""

def pairwise_jaccard(y_true: np.ndarray, labels: np.ndarray) -> float:
    """External; lớn hơn tốt hơn."""
```

Kết quả của một lần chạy nên được lưu ở dạng:

```python
result = {
    "n_clusters": C,
    "base_fuzzifier": M,
    "supervised_fuzzifier": M_prime,
    "supervision_ratio": ratio,
    "seed": seed,
    "converged": model.converged_,
    "n_iter": model.n_iter_,
    "objective": model.objective_history_[-1],
    "silhouette": swc,
    "simplified_silhouette": sswc,
    "calinski_harabasz": vrc,
    "davies_bouldin": db,
    "pbm": pbm,
    "ari_eval": ari,
    "jaccard_eval": jaccard,
}
```

## 12. Kiểm thử cần có

### 12.1 Kiểm thử nhãn từ membership

- `U.shape == (N, C)`;
- mọi hàng có tổng xấp xỉ `1`;
- `labels.shape == (N,)`;
- `labels[i] == argmax(U[i])`;
- quy định rõ cách phá hòa khi hai membership bằng nhau.

### 12.2 Kiểm thử internal metrics

- cụm chặt và tách xa phải có SWC/VRC/PBM cao hơn;
- cụm chặt và tách xa phải có DB thấp hơn;
- hoán vị mã nhãn không làm thay đổi score;
- xử lý hoặc báo lỗi rõ khi `C < 2`;
- xử lý singleton theo đúng quy ước SWC: silhouette của singleton bằng `0`;
- báo lỗi hoặc quy ước rõ nếu một cụm rỗng;
- bảo vệ chia cho 0 khi tâm trùng nhau hoặc độ phân tán bằng 0.

### 12.3 Kiểm thử external metrics

- phân hoạch giống hệt nhãn thật cho ARI và Jaccard bằng `1`;
- hoán vị tên cụm không đổi ARI/Jaccard;
- phân hoạch ngẫu nhiên có ARI trung bình gần `0` qua nhiều lần thử;
- chỉ tính score trên evaluation indices khi đánh giá held-out.

### 12.4 Kiểm thử tích hợp với sSMC-FCM

Trên bộ 20 điểm của bài sSMC-FCM:

1. chạy `M=2, M'=2`;
2. chạy `M=2, M'=4`;
3. chạy `M=2, M'=8`;
4. kiểm tra membership cụm 1 của điểm 9 và 10 tăng xấp xỉ:

$$
0.19\rightarrow0.43\rightarrow0.60;
$$

5. tính các metric trên nhãn cứng của ba nghiệm;
6. ghi nhận rằng internal metric không nhất thiết tăng theo `M'`, vì mục tiêu giám sát và mục tiêu compactness/separation có thể xung đột.

## 13. Bộ metric tối thiểu nên hiện thực trước

Thứ tự đề xuất:

1. **ARI:** kiểm chứng bằng ground truth, không cần căn chỉnh nhãn.
2. **Jaccard theo cặp:** external metric thứ hai đúng với phương pháp của bài báo.
3. **SWC:** metric internal chính, mạnh và ổn định trong nghiên cứu.
4. **SSWC:** biến thể nhanh cho dữ liệu lớn.
5. **VRC:** nhanh, dễ hiện thực, hữu ích để đối chiếu.
6. **PBM:** hiệu năng thực nghiệm tốt và chi phí hợp lý.
7. **DB:** metric phụ quen thuộc, chiều tối ưu ngược với các metric trên.

Không nên ưu tiên ngay Gamma, G(+) hoặc Tau vì chi phí rất lớn. Không nên hiện thực toàn bộ 18 biến thể Dunn trước khi lõi sSMC-FCM và bộ metric tối thiểu đã được kiểm chứng.

## 14. Kết luận áp dụng

Bài báo 2010 giúp dự án trả lời hai câu hỏi khác nhau:

1. **Kết quả phân cụm hiện tại có compact và separated không?**  
   Dùng SWC/SSWC, VRC, PBM và DB trên nhãn `argmax(U)`.

2. **Kết quả có khôi phục đúng cấu trúc lớp không?**  
   Nếu có ground truth giữ lại, dùng ARI và Jaccard trên phần không đưa vào supervision.

Lựa chọn thực dụng nhất cho sSMC-FCM là:

```text
Internal: SWC hoặc SSWC + VRC + PBM
External: ARI + Jaccard
Diagnostics: objective, delta tâm, số vòng lặp, residual solver Eq. (19)
```

Các metric validity không thay thế các kiểm tra đúng đắn toán học của sSMC-FCM. Một kết quả có Silhouette cao vẫn có thể là kết quả của công thức membership bị cài sai. Trước tiên phải kiểm tra simplex của `U`, residual của Equation (19), công thức tâm Equation (10), hội tụ và khả năng tái lập Table 3; sau đó mới dùng validity metrics để so sánh chất lượng các phân hoạch hợp lệ.
