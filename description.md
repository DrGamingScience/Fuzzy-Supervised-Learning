Tôi được giao nhiệm vụ:

> Có 3 bài báo đính kèm:
> - một bài về sSFCM,
> - một bài về sSMC-FCM,
> - một bài về các độ đo đánh giá kết quả.
>
> Nhiệm vụ cuối cùng của tôi là **lập trình thuật toán sSMC-FCM**.

Trong workspace hiện tại có 3 file PDF tương ứng. Hãy làm việc theo quy trình dưới đây.

## Mục tiêu

Tôi chưa muốn bạn code sSMC-FCM ngay.

Trước tiên hãy:

1. Bóc nội dung 3 PDF thành text để giảm token khi phân tích về sau.
2. Xác định chính xác:
   - paper nào là sSFCM;
   - paper nào là sSMC-FCM;
   - paper nào nói về evaluation metrics.
3. Đọc và đối chiếu 3 paper.
4. Hiểu đầy đủ thuật toán sSMC-FCM cần implement.
5. Tạo hai tài liệu:
   - `product-backlog.md`
   - `ptyc.md`

Hai tài liệu này phải đủ chi tiết để sau khi tôi đọc xong, tôi biết:
- bài toán đang giải quyết là gì;
- sSFCM hoạt động thế nào;
- sSMC-FCM cải tiến điểm nào;
- các công thức toán học cần implement;
- input/output là gì;
- dữ liệu supervised/semi-supervised được biểu diễn ra sao;
- cần viết những module/function nào;
- trình tự implementation;
- đánh giá kết quả bằng metric nào;
- làm thế nào để kiểm tra implementation đúng với paper.

---

# PHASE 1 — Khảo sát workspace

Trước tiên:

- tìm tất cả file `.pdf` liên quan trong workspace;
- liệt kê tên file;
- không suy đoán paper dựa chỉ vào filename;
- đọc title/abstract/keywords để xác định nội dung thực tế.

Không chỉnh sửa hay xóa PDF gốc.

---

# PHASE 2 — Chuyển PDF sang TXT

Tạo thư mục:

```text
papers_txt/
```

Mỗi PDF phải có một file `.txt` tương ứng, ví dụ:

```text
papers_txt/
├── paper_ssfcm.txt
├── paper_ssmc_fcm.txt
└── paper_evaluation.txt
```

Tên cụ thể có thể điều chỉnh theo title thực tế của paper.

Ưu tiên extraction text trực tiếp từ PDF, ví dụ:

- `pdftotext` nếu có;
- PyMuPDF;
- pypdf;
- công cụ local tương đương.

**Không OCR nếu PDF đã có text layer.**

Chỉ dùng OCR như fallback nếu xác nhận PDF là scan/image hoặc extraction thông thường thất bại.

Sau khi extract, kiểm tra nhanh:

- title;
- abstract;
- section headings;
- mathematical expressions;
- references;

để đảm bảo text không bị rỗng hoặc hỏng hoàn toàn.

Nếu công thức toán bị mất format khi convert TXT thì giữ PDF làm nguồn tham chiếu cho đúng công thức; không tự đoán công thức bị thiếu.

---

# PHASE 3 — Xác định vai trò từng paper

Từ nội dung thật của paper, xác định:

### Paper A — sSFCM

Tìm và ghi lại:

- tên đầy đủ của thuật toán;
- bài toán paper giải quyết;
- FCM baseline;
- phần semi-supervised được đưa vào như thế nào;
- objective function;
- membership matrix;
- cluster centers;
- supervised information;
- update rules;
- stopping condition;
- hyperparameters;
- algorithm/pseudocode nếu paper có.

### Paper B — sSMC-FCM

Đây là paper quan trọng nhất.

Phân tích thật kỹ:

- sSMC-FCM viết đầy đủ là gì;
- motivation của thuật toán;
- khác biệt với FCM;
- khác biệt với sSFCM;
- mathematical formulation;
- objective function;
- mọi biến/ký hiệu;
- constraints;
- membership update;
- prototype/centroid update;
- cách dùng labeled samples;
- cách dùng unlabeled samples;
- multiple fuzzification coefficients nếu có;
- các tham số cần khởi tạo;
- convergence criterion;
- algorithm flow;
- computational complexity nếu paper đề cập.

Với **mỗi công thức quan trọng**, hãy giải thích:

1. công thức gốc;
2. ý nghĩa từng biến;
3. dimensions / shape khi implement bằng NumPy;
4. công thức đó sẽ nằm ở function/module nào;
5. lưu ý numerical stability.

Không tự sáng tạo công thức nếu paper không nói rõ.

Nếu paper có equation number, ghi lại số equation để tôi tra cứu PDF.

### Paper C — Evaluation Metrics

Xác định toàn bộ metric paper đề xuất hoặc sử dụng để đánh giá clustering.

Với mỗi metric:

- tên;
- công thức;
- ý nghĩa;
- input;
- expected range;
- giá trị cao hay thấp là tốt;
- metric cần ground-truth label hay không;
- dùng được cho fuzzy clustering hay hard clustering;
- cách áp dụng vào sSMC-FCM.

Phân biệt nếu có:

- internal clustering metrics;
- external clustering metrics;
- fuzzy clustering validity indices;
- accuracy / ARI / NMI / Rand Index hoặc metric tương tự.

Không mặc định metric nào sẽ được dùng nếu paper không nói như vậy.

---

# PHASE 4 — Đối chiếu sSFCM và sSMC-FCM

Tạo một comparison table trong tài liệu phân tích gồm ít nhất:

| Thành phần | FCM | sSFCM | sSMC-FCM |
|---|---|---|---|
| Input | | | |
| Supervision | | | |
| Membership | | | |
| Fuzzifier | | | |
| Objective | | | |
| Cluster center update | | | |
| Membership update | | | |
| Labeled data treatment | | | |
| Hyperparameters | | | |
| Stop condition | | | |
| Output | | | |

Mục tiêu là chỉ ra chính xác:

> Để đi từ implementation FCM → sSFCM → sSMC-FCM cần thay đổi phần nào.

---

# PHASE 5 — Tạo `ptyc.md`

Tạo file:

```text
ptyc.md
```

Đây là tài liệu **phân tích yêu cầu + technical specification** cho implementation sSMC-FCM.

Cấu trúc mong muốn:

# 1. Problem Statement

Giải thích bài toán clustering mà sSMC-FCM giải quyết.

# 2. Background

Tóm tắt vừa đủ:

- K-Means;
- FCM;
- semi-supervised fuzzy clustering;
- sSFCM;
- lý do xuất hiện sSMC-FCM.

Không viết textbook quá dài.

# 3. Paper Mapping

Bảng:

| File | Paper title | Vai trò |
|---|---|---|
| ... | ... | sSFCM |
| ... | ... | sSMC-FCM |
| ... | ... | Evaluation |

# 4. Mathematical Notation

Tạo bảng toàn bộ ký hiệu:

| Symbol | Meaning | Code representation / shape |
|---|---|---|

Ví dụ:

```text
X: dataset, shape (n_samples, n_features)
U: membership matrix
V: cluster centers
C: number of clusters
...
```

Nhưng phải lấy ký hiệu thực tế từ paper.

# 5. sSFCM Formulation

Ghi:

- objective;
- constraints;
- update equations;
- algorithm flow.

# 6. sSMC-FCM Formulation

Đây là section chi tiết nhất.

Bao gồm:

- objective function;
- từng term trong objective;
- update equations;
- initialization;
- iteration;
- convergence;
- output.

Mỗi equation cần mapping sang implementation.

# 7. Difference: FCM vs sSFCM vs sSMC-FCM

Dùng bảng comparison ở trên.

# 8. Software Design

Đề xuất cấu trúc code Python hợp lý, ví dụ:

```text
src/
├── fcm.py
├── ssfcm.py
├── ssmc_fcm.py
├── metrics.py
├── data.py
└── utils.py

tests/
├── test_fcm.py
├── test_ssfcm.py
├── test_ssmc_fcm.py
└── test_metrics.py
```

Không bắt buộc đúng cấu trúc trên nếu có cách tốt hơn.

Với từng module/function, mô tả:

- responsibility;
- input;
- output;
- ndarray shape;
- equation tương ứng trong paper.

Đặc biệt đề xuất API chính kiểu:

```python
model = SSMCFCM(...)
model.fit(X, ...)
labels = model.predict(...)
```

nhưng API cuối cùng phải phù hợp thuật toán paper.

# 9. Implementation Algorithm

Viết pseudocode sát paper:

```text
Initialize ...
repeat:
    ...
    update ...
    update ...
until convergence
```

Sau pseudocode, mapping từng step → Python function.

# 10. Evaluation Plan

Xác định:

- metrics;
- datasets;
- baseline;
- expected experiments;
- comparison sSFCM vs sSMC-FCM.

Nếu paper có experimental setup cụ thể thì ghi rõ.

# 11. Verification Strategy

Phải trả lời:

**Làm sao biết implementation sSMC-FCM của chúng ta đúng?**

Bao gồm ít nhất:

- mathematical sanity checks;
- membership constraints;
- shape checks;
- convergence;
- objective non-increase nếu lý thuyết yêu cầu;
- deterministic test với seed;
- synthetic dataset tests;
- comparison với kết quả/table/figure trong paper nếu có thể reproduce;
- comparison với FCM/sSFCM baseline.

# 12. Open Questions / Ambiguities

Nếu paper thiếu chi tiết hoặc công thức không rõ:

- ghi rõ;
- dẫn section/equation/page;
- KHÔNG tự suy đoán rồi coi đó là fact.

---

# PHASE 6 — Tạo `product-backlog.md`

Tạo:

```text
product-backlog.md
```

Backlog phải biến paper thành **các task implementation nhỏ, có thứ tự phụ thuộc rõ ràng**.

Dùng format:

```markdown
## PB-01 — ...

### Goal

### Why

### Inputs

### Outputs

### Implementation

### Paper reference

### Acceptance criteria

### Dependencies
```

Backlog nên được chia thành các milestone.

## Milestone 0 — Paper understanding

Ví dụ:

- extract PDFs;
- identify papers;
- notation mapping;
- verify equations.

## Milestone 1 — FCM baseline

Ví dụ:

- distance computation;
- membership initialization;
- center update;
- membership update;
- objective;
- convergence.

## Milestone 2 — sSFCM

Implement phần semi-supervised cần thiết để làm baseline và hiểu progression của thuật toán.

## Milestone 3 — sSMC-FCM core

Tách nhỏ từng mathematical component của sSMC-FCM thành task.

Không tạo một task chung chung kiểu:

> Implement sSMC-FCM.

Phải chia nhỏ đủ để có thể implement/test từng phần độc lập.

## Milestone 4 — Evaluation Metrics

Implement các metric thực sự cần thiết từ paper metric.

## Milestone 5 — Experiments

- dataset;
- preprocessing;
- labeled/unlabeled split;
- experiment runner;
- seeds;
- hyperparameters;
- logging results.

## Milestone 6 — Verification

- unit tests;
- numerical tests;
- reproduction tests;
- regression tests.

### Acceptance criteria

Mỗi backlog item phải có acceptance criteria cụ thể, ví dụ:

```text
- U.shape == (n_samples, n_clusters)
- sum(U[i, :]) ≈ 1
- no NaN/Inf
- objective converges according to paper criterion
```

Không dùng acceptance criteria mơ hồ kiểu "algorithm works correctly".

---

# PHASE 7 — Token-efficiency rules

Sau khi tạo `.txt`:

- ưu tiên search/read `.txt`;
- không đọc lại toàn bộ PDF liên tục;
- chỉ quay lại PDF khi cần:
  - kiểm tra equation;
  - figure/table;
  - ký hiệu bị extract sai;
  - text extraction thiếu.

Khi phân tích paper dài, tìm trước các keyword như:

```text
objective
membership
fuzzification
fuzzifier
semi-supervised
constraint
algorithm
update
centroid
prototype
convergence
evaluation
validity
metric
experiment
```

Đọc section liên quan thay vì nạp toàn bộ tài liệu vào context cùng lúc.

---

# PHASE 8 — Scientific accuracy

Đây là yêu cầu quan trọng.

Không được:

- tự đoán equation;
- thay đổi ký hiệu mà không giải thích;
- coi implementation phổ biến trên Internet là giống paper;
- tự thêm một biến thể FCM rồi gọi nó là sSMC-FCM;
- suy luận kết quả thí nghiệm mà paper không báo cáo.

Nếu có phần không chắc chắn, viết:

```text
[NEEDS VERIFICATION]
```

và ghi:

- paper;
- page;
- section;
- equation/table/figure liên quan.

Nếu có mâu thuẫn giữa 2 paper, ghi rõ cả hai.

---

# PHASE 9 — Kết quả cuối cùng

Khi hoàn thành, workspace phải có ít nhất:

```text
papers_txt/
├── <paper-1>.txt
├── <paper-2>.txt
└── <paper-3>.txt

ptyc.md
product-backlog.md
```

Chưa implement thuật toán sSMC-FCM trong phase này.

Cuối cùng báo cáo ngắn cho tôi:

1. tên và vai trò của 3 paper;
2. sSMC-FCM khác sSFCM quan trọng nhất ở đâu;
3. có equation/chi tiết nào chưa rõ không;
4. tổng số backlog items;
5. backlog item nào là điểm bắt đầu tốt nhất cho coding;
6. file nào tôi nên đọc trước.

Hãy thực hiện trực tiếp việc khảo sát workspace, extract PDF và tạo các file trên. Không chỉ mô tả cho tôi cách làm.