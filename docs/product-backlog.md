# Product Backlog - sSMC-FCM

Backlog gồm 37 hạng mục, được sắp theo quan hệ phụ thuộc. Các công việc khảo sát đã hoàn thành; chưa có hạng mục lập trình nào được thực hiện.

Quy ước ưu tiên:

- P0: bắt buộc để có hiện thực đúng bài báo.
- P1: bắt buộc để đánh giá và tái lập đầy đủ.
- P2: mở rộng sau khi phần lõi đã đúng.
- Số trang là số trang của tệp PDF.

## Milestone 0 - Hiểu và chuẩn hóa bài báo

## PB-01 - Trích xuất ba PDF thành văn bản

### Mục tiêu

Tạo bản văn bản có thể tìm kiếm cho từng bài báo. Trạng thái: Hoàn thành.

### Lý do

Giảm chi phí phân tích và chỉ quay lại PDF khi cần kiểm tra công thức, bảng hoặc hình.

### Đầu vào

Ba PDF gốc trong papers/pdf/.

### Đầu ra

Ba tệp TXT trong papers/text/.

### Hiện thực

Dùng pdftotext với layout và UTF-8; không OCR vì cả ba PDF có text layer.

### Tham chiếu bài báo

Toàn bộ ba PDF.

### Tiêu chí chấp nhận

- Có đúng ba TXT tương ứng 12, 6 và 27 trang.
- Title, abstract, heading, công thức và references không rỗng.
- PDF gốc không bị sửa.

### Phụ thuộc

Không.

## PB-02 - Xác định vai trò và metadata bài báo

### Mục tiêu

Ánh xạ chính xác sSFCM, sSMC-FCM và evaluation. Trạng thái: Hoàn thành.

### Lý do

Không suy đoán nội dung chỉ từ tên tệp.

### Đầu vào

Title, abstract, keywords và section headings.

### Đầu ra

Bảng ánh xạ trong docs/ptyc.md.

### Hiện thực

Đọc nội dung thật của từng bài báo và đối chiếu phần phương pháp.

### Tham chiếu bài báo

Trang đầu của mỗi PDF.

### Tiêu chí chấp nhận

- Mỗi tệp có đúng title và một vai trò.
- Vai trò phù hợp abstract và nội dung phương pháp.

### Phụ thuộc

PB-01.

## PB-03 - Chuẩn hóa ký hiệu và shape

### Mục tiêu

Chuyển notation của hai bài thuật toán sang quy ước NumPy theo chiều mẫu. Trạng thái: Hoàn thành.

### Lý do

Bài sSFCM và sSMC-FCM dùng chỉ số theo thứ tự khác nhau.

### Đầu vào

Các hàm mục tiêu, công thức cập nhật và ràng buộc.

### Đầu ra

Bảng ký hiệu, ý nghĩa và shape.

### Hiện thực

Chuẩn hóa X:(N,D), U:(N,C), V:(C,D) và ghi rõ ánh xạ chỉ số.

### Tham chiếu bài báo

sSFCM Section II; sSMC-FCM Sections 2-3.

### Tiêu chí chấp nhận

- Mọi biến trong sSFCM Eqs. (2),(4),(6) và sSMC-FCM Eqs. (7)-(20),(23) có shape.
- Không còn chỉ số i/k mơ hồ.

### Phụ thuộc

PB-02.

## PB-04 - Kiểm tra trực quan các công thức quan trọng

### Mục tiêu

Xác minh những công thức bị hỏng định dạng khi trích xuất TXT. Trạng thái: Hoàn thành.

### Lý do

PDF hai cột có thể làm sai số mũ, dấu phẩy trên và ngoặc.

### Đầu vào

TXT và PDF gốc.

### Đầu ra

Các công thức đã được đối chiếu trong docs/ptyc.md.

### Hiện thực

Kiểm tra sSFCM trang 2-3; sSMC-FCM trang 5,6,8,9; validity trang 4-13.

### Tham chiếu bài báo

sSFCM Eqs. (1)-(8); sSMC-FCM Eqs. (7)-(20),(23); validity Eqs. (1)-(53).

### Tiêu chí chấp nhận

- Eq. (19) có số mũ đúng $(M'-M)/(M'-1)$.
- Eq. (23) có $M'\alpha^{M'-1}$ ở vế trái.
- Mỗi metric giữ đúng chiều tối ưu.

### Phụ thuộc

PB-01, PB-03.

## PB-05 - Ghi nhận các điểm chưa rõ và quyết định kỹ thuật

### Mục tiêu

Tách dữ kiện từ bài báo khỏi lựa chọn hiện thực. Trạng thái: Danh sách hoàn thành, quyết định còn mở.

### Lý do

Bài báo thiếu initialization, norm dừng, xử lý khoảng cách 0 và chi tiết solver Eq. (19).

### Đầu vào

Section 12 của docs/ptyc.md.

### Đầu ra

Decision log khi bắt đầu viết mã.

### Hiện thực

Mỗi quyết định ghi default, phương án khác, ảnh hưởng tái lập và test tương ứng.

### Tham chiếu bài báo

sSMC-FCM Sections 3.1-3.2; sSFCM Algorithm 1.

### Tiêu chí chấp nhận

- Mười hai điểm chưa rõ có quyết định hoặc trạng thái mở.
- Không mô tả quyết định kỹ thuật như công thức gốc.

### Phụ thuộc

PB-04.

## Milestone 1 - FCM baseline

## PB-06 - Khởi tạo package, kiểu dữ liệu và validation

### Mục tiêu

Tạo skeleton src/, tests/ và validation chung. Ưu tiên: P0.

### Lý do

Mọi baseline cần cùng hợp đồng shape và lỗi.

### Đầu vào

X, C, fuzzifier, tolerance, tâm hoặc seed tùy chọn.

### Đầu ra

Dữ liệu và cấu hình đã kiểm tra.

### Hiện thực

Kiểm tra dữ liệu 2-D, hữu hạn, không rỗng; C hợp lệ; fuzzifier và tolerance dương.

### Tham chiếu bài báo

sSMC-FCM Section 2.1 và ràng buộc sau Eq. (1).

### Tiêu chí chấp nhận

- Từ chối NaN/Inf, dữ liệu rỗng, C sai và m không hợp lệ.
- Không thay đổi X đầu vào.
- Có unit test cho mọi nhánh lỗi.

### Phụ thuộc

PB-03, PB-05.

## PB-07 - Khoảng cách Euclid theo cặp

### Mục tiêu

Tính D và D bình phương ổn định. Ưu tiên: P0.

### Lý do

Mọi công thức cập nhật và nhiều metric đều cần khoảng cách.

### Đầu vào

X:(N,D), V:(C,D).

### Đầu ra

dist và dist_sq, shape (N,C).

### Hiện thực

Vector hóa bằng NumPy; chặn sai số âm rất nhỏ của bình phương khoảng cách về 0.

### Tham chiếu bài báo

FCM Eq. (1); sSMC-FCM Eq. (7).

### Tiêu chí chấp nhận

- Trùng vòng lặp tham chiếu với rtol/atol đã công bố.
- Shape đúng, không NaN/Inf với đầu vào hợp lệ.
- Không tính căn bậc hai lặp lại không cần thiết.

### Phụ thuộc

PB-06.

## PB-08 - Khởi tạo FCM

### Mục tiêu

Tạo U0 hợp lệ hoặc nhận V0 cố định. Ưu tiên: P0.

### Lý do

Cần tính tái lập và kiểm soát thí nghiệm.

### Đầu vào

N, C, random_state hoặc V0.

### Đầu ra

U0:(N,C) hoặc V0:(C,D).

### Hiện thực

Hỗ trợ seed và tâm do người gọi cung cấp; ghi rõ chiến lược.

### Tham chiếu bài báo

FCM Step 1; sSMC-FCM Step 1.

### Tiêu chí chấp nhận

- U0 không âm, tổng hàng bằng 1 nếu khởi tạo U.
- Cùng seed cho cùng kết quả.
- Không xáo trộn tâm được cung cấp.

### Phụ thuộc

PB-06.

## PB-09 - Cập nhật độ thuộc FCM

### Mục tiêu

Hiện thực công thức tỷ số khoảng cách. Ưu tiên: P0.

### Lý do

Đây là baseline và chính là Eq. (15) cho mẫu không giám sát.

### Đầu vào

dist:(N,C), m>1.

### Đầu ra

U:(N,C).

### Hiện thực

Dùng FCM Eq. (2) / sSMC-FCM Eq. (15); tách riêng policy khoảng cách 0.

### Tham chiếu bài báo

sSMC-FCM Eqs. (2),(15), PDF trang 3 và 6.

### Tiêu chí chấp nhận

- Tổng mỗi hàng xấp xỉ 1.
- Không âm, hữu hạn.
- Trùng ví dụ thủ công không có khoảng cách 0.
- Không NaN/Inf trong test zero-distance.

### Phụ thuộc

PB-07, PB-08.

## PB-10 - Cập nhật tâm và objective FCM

### Mục tiêu

Hiện thực FCM Eqs. (1),(3). Ưu tiên: P0.

### Lý do

Cần cho alternating optimization và baseline.

### Đầu vào

X, U, m, dist_sq.

### Đầu ra

V:(C,D) và objective scalar.

### Hiện thực

Tính weights = U**m, weighted mean và tổng weights*dist_sq.

### Tham chiếu bài báo

sSMC-FCM Section 2.1, Eqs. (1),(3).

### Tiêu chí chấp nhận

- Trùng vòng lặp tham chiếu.
- Objective hữu hạn, không âm.
- Mẫu số bằng 0 có lỗi/policy rõ ràng.

### Phụ thuộc

PB-07, PB-09.

## PB-11 - Vòng fit FCM và regression test

### Mục tiêu

Hoàn chỉnh FCM có tính xác định. Ưu tiên: P0.

### Lý do

sSMC-FCM tái sử dụng vòng lặp và cập nhật cho mẫu không nhãn.

### Đầu vào

Các component PB-07 đến PB-10.

### Đầu ra

membership_, cluster_centers_, labels_, histories, converged_.

### Hiện thực

Lặp cập nhật U/V, dừng theo delta tâm, giới hạn max_iter và ghi objective.

### Tham chiếu bài báo

sSMC-FCM Section 2.1, Steps 1-5.

### Tiêu chí chấp nhận

- Hội tụ trên synthetic blobs tách biệt.
- Cùng seed cho cùng kết quả.
- Objective không tăng quá tolerance trên test chuẩn.
- Mọi invariant shape/simplex đúng.

### Phụ thuộc

PB-08, PB-09, PB-10.

## Milestone 2 - sSFCM baseline

## PB-12 - Biểu diễn và kiểm tra U_bar

### Mục tiêu

Định nghĩa hợp đồng supervision của sSFCM. Ưu tiên: P0.

### Lý do

U_bar khác hoàn toàn Y của sSMC-FCM.

### Đầu vào

U_bar:(N,C).

### Đầu ra

Supervision hợp lệ và residual r:(N,).

### Hiện thực

Kiểm tra hữu hạn, trong [0,1], tổng hàng không quá 1.

### Tham chiếu bài báo

sSFCM Eq. (1), PDF trang 2.

### Tiêu chí chấp nhận

- Từ chối shape/giá trị/tổng hàng sai.
- Ma trận 0 hợp lệ và tương ứng không giám sát.
- Residual nằm trong [0,1].

### Phụ thuộc

PB-06.

## PB-13 - Cập nhật độ thuộc sSFCM khi m>1

### Mục tiêu

Hiện thực Eq. (6). Ưu tiên: P0.

### Lý do

Cần baseline bán giám sát để đối chiếu tiến trình.

### Đầu vào

dist_sq, U_bar, m.

### Đầu ra

U:(N,C).

### Hiện thực

Phân bổ residual theo nghịch đảo khoảng cách bình phương đã chuẩn hóa.

### Tham chiếu bài báo

sSFCM Eqs. (5)-(7), PDF trang 2.

### Tiêu chí chấp nhận

- U không nhỏ hơn U_bar ngoài tolerance.
- Tổng hàng bằng 1.
- U_bar=0 cho kết quả trùng FCM.
- Xử lý khoảng cách 0 theo decision log.

### Phụ thuộc

PB-09, PB-12.

## PB-14 - Nhánh sSFCM khi m=1

### Mục tiêu

Hiện thực Eq. (8). Ưu tiên: P1.

### Lý do

Bài gốc trình bày đây là một nhánh đầy đủ.

### Đầu vào

dist_sq, U_bar.

### Đầu ra

U:(N,C).

### Hiện thực

Gán residual cho cụm gần nhất; ghi rõ cách phá hòa.

### Tham chiếu bài báo

sSFCM Eq. (8), Algorithm 1, PDF trang 3.

### Tiêu chí chấp nhận

- Phần tử không phải target bằng U_bar.
- Target gần nhất nhận toàn bộ residual.
- Tổng hàng bằng 1; xử lý hòa có tính xác định.

### Phụ thuộc

PB-12, PB-07.

## PB-15 - Tâm, objective và vòng fit sSFCM

### Mục tiêu

Hoàn chỉnh sSFCM baseline. Ưu tiên: P0.

### Lý do

Cần so sánh trực tiếp với sSMC-FCM.

### Đầu vào

X, U_bar, m, V0, tol, max_iter.

### Đầu ra

Trạng thái model và histories.

### Hiện thực

Objective Eq. (2), tâm Eq. (4), membership PB-13/PB-14.

### Tham chiếu bài báo

sSFCM Eqs. (2),(4),(6),(8), Algorithm 1.

### Tiêu chí chấp nhận

- Objective hữu hạn, không âm.
- U_bar=0, m>1 trùng FCM với cùng initialization.
- Stop/max_iter có semantics rõ.

### Phụ thuộc

PB-13, PB-14, PB-10.

## PB-16 - Tái lập sSFCM Table II

### Mục tiêu

Kiểm tra baseline bằng số liệu bài báo. Ưu tiên: P1.

### Lý do

Giảm rủi ro sai notation trước khi viết sSMC-FCM.

### Đầu vào

Bộ 20 điểm, m=2; supervision 0, 0.3 và 0.6 cho mẫu 9,10 vào cụm 1.

### Đầu ra

Fixture và báo cáo so sánh.

### Hiện thực

Căn chỉnh hoán vị nhãn; so độ thuộc làm tròn hai chữ số.

### Tham chiếu bài báo

sSFCM Section III, Tables I-II.

### Tiêu chí chấp nhận

- Membership khớp Table II trong tolerance do làm tròn nếu có thể.
- Nếu không khớp do thiếu V0, ghi sai lệch; không sửa công thức.
- Mẫu 9,10 có xu hướng 0.19 -> 0.45 -> 0.69 tại cụm 1.

### Phụ thuộc

PB-15, PB-30.

## Milestone 3 - Lõi sSMC-FCM

## PB-17 - Biểu diễn và kiểm tra Y

### Mục tiêu

Mã hóa mẫu có/không có giám sát. Ưu tiên: P0.

### Lý do

Suy dẫn chỉ xử lý một cụm đích cho mỗi mẫu.

### Đầu vào

target_cluster:(N,), -1 nếu không nhãn.

### Đầu ra

Mask và chỉ số target.

### Hiện thực

Kiểm tra kiểu số nguyên, miền giá trị và từ chối nhiều target trong baseline.

### Tham chiếu bài báo

sSMC-FCM Eq. (8), Case 2 Eqs. (16)-(20).

### Tiêu chí chấp nhận

- Chỉ nhận -1 hoặc [0,C).
- Giữ nguyên thứ tự mẫu.
- Trường hợp toàn bộ không nhãn hợp lệ.

### Phụ thuộc

PB-06, PB-05.

## PB-18 - Tạo ma trận số mũ

### Mục tiêu

Hiện thực Eq. (8). Ưu tiên: P0.

### Lý do

Đây là cơ chế giám sát cốt lõi của sSMC-FCM.

### Đầu vào

targets, C, M, M_prime.

### Đầu ra

exponents:(N,C).

### Hiện thực

Điền M rồi đặt ô target thành M_prime.

### Tham chiếu bài báo

sSMC-FCM Eq. (8), PDF trang 5.

### Tiêu chí chấp nhận

- Kiểm tra M_prime > M > 1.
- Mỗi hàng giám sát có đúng một ô M_prime.
- Hàng không nhãn chứa toàn M.

### Phụ thuộc

PB-17.

## PB-19 - Chuẩn hóa khoảng cách và tính mu ngoài target

### Mục tiêu

Hiện thực Eqs. (17)-(18). Ưu tiên: P0.

### Lý do

Đây là nửa đầu cập nhật độ thuộc có giám sát.

### Đầu vào

dist_row, target, M.

### Đầu ra

d_row, mu_non_target và A.

### Hiện thực

Tính d_min, tỷ số và số mũ; xử lý khoảng cách 0 theo decision log.

### Tham chiếu bài báo

sSMC-FCM Eqs. (17)-(18), PDF trang 6.

### Tiêu chí chấp nhận

- min(d_row)=1 khi d_min>0.
- mu ngoài target dương và hữu hạn.
- Trùng phép tính thủ công.
- Có test riêng cho zero-distance.

### Phụ thuộc

PB-07, PB-17.

## PB-20 - Solver scalar cho Eq. (19)

### Mục tiêu

Giải mu_target với residual được kiểm soát. Ưu tiên: P0.

### Lý do

Đây là thành phần khó nhất và bài báo không cho closed form.

### Đầu vào

A, d_target, M, M_prime, solver_tol, max_iter.

### Đầu ra

mu_target dương, residual và số vòng.

### Hiện thực

Dùng chia đôi với cận mở rộng động trên hàm tăng của bài báo.

### Tham chiếu bài báo

sSMC-FCM Eq. (19), PDF trang 6 và 9.

### Tiêu chí chấp nhận

- Residual tuyệt đối hoặc đã scale không quá solver_tol.
- Có tính xác định và giới hạn vòng lặp.
- Test nhiều bộ tham số, kể cả gần biên.
- Khi thất bại phải có diagnostic, không trả NaN.

### Phụ thuộc

PB-19, PB-05.

## PB-21 - Tạo hàng membership có giám sát

### Mục tiêu

Kết hợp Eqs. (17)-(20). Ưu tiên: P0.

### Lý do

Tạo một hàng U thỏa hệ Eq. (16).

### Đầu vào

dist_row, target, M, M_prime.

### Đầu ra

U_row:(C,) và solver diagnostics.

### Hiện thực

Gọi PB-19/PB-20 rồi chuẩn hóa mu bằng Eq. (20).

### Tham chiếu bài báo

sSMC-FCM Eqs. (16)-(20), Proposition 1.

### Tiêu chí chấp nhận

- U_row không âm, hữu hạn, tổng bằng 1.
- Các vế $M'U_k^{M'-1}D_k^2$ và $MU_j^{M-1}D_j^2$ xấp xỉ bằng nhau.
- Residual Eq. (19) đạt tolerance.

### Phụ thuộc

PB-19, PB-20.

## PB-22 - Cập nhật membership hỗn hợp

### Mục tiêu

Cập nhật toàn bộ U cho mẫu có và không có giám sát. Ưu tiên: P0.

### Lý do

Step 2 cần hai công thức khác nhau.

### Đầu vào

dist:(N,C), targets, M, M_prime.

### Đầu ra

U:(N,C) và diagnostics cho các hàng giám sát.

### Hiện thực

Batch các hàng không nhãn bằng Eq. (15); xử lý S hàng giám sát bằng Eq. (19).

### Tham chiếu bài báo

sSMC-FCM Step 2, Eqs. (15),(17)-(20).

### Tiêu chí chấp nhận

- Toàn bộ U đúng shape/simplex.
- Hàng không nhãn trùng PB-09.
- Hàng giám sát thỏa PB-21.
- Không thay đổi thứ tự đầu vào.

### Phụ thuộc

PB-09, PB-17, PB-21.

## PB-23 - Tâm và objective sSMC-FCM

### Mục tiêu

Hiện thực Eqs. (10),(7). Ưu tiên: P0.

### Lý do

Số mũ thay đổi theo ô nên không thể dùng nguyên mã FCM scalar.

### Đầu vào

X, U, exponents, dist_sq.

### Đầu ra

V:(C,D) và objective scalar.

### Hiện thực

Tính weights=U**exponents, weighted centers và tổng weights*dist_sq.

### Tham chiếu bài báo

sSMC-FCM Eqs. (7),(10), PDF trang 5.

### Tiêu chí chấp nhận

- Trùng vòng lặp tham chiếu.
- Objective hữu hạn, không âm.
- Khi toàn bộ exponent là M thì trùng FCM.
- Mẫu số 0 có diagnostic rõ.

### Phụ thuộc

PB-18, PB-22, PB-07.

## PB-24 - Vòng fit và API SSMCFCM

### Mục tiêu

Hoàn chỉnh thuật toán đích. Ưu tiên: P0.

### Lý do

Kết nối các phương trình thành alternating optimization có thể dùng và kiểm thử.

### Đầu vào

X, targets, C, M, M_prime, tol, max_iter, V0/seed và cấu hình solver.

### Đầu ra

Model đã fit với U, V, labels, histories và converged_.

### Hiện thực

Theo Steps 1-5; ghi objective, delta tâm và residual solver.

### Tham chiếu bài báo

sSMC-FCM phần tóm tắt thuật toán, PDF trang 6-7.

### Tiêu chí chấp nhận

- API và attributes đúng đặc tả.
- Dừng đúng norm/tol hoặc converged_=False khi hết max_iter.
- Không NaN/Inf trên dữ liệu chuẩn.
- Cùng seed/cấu hình cho cùng kết quả.
- Default path không chứa biến thể ngoài bài báo.

### Phụ thuộc

PB-18, PB-22, PB-23.

## PB-25 - Bộ chọn M_prime theo Eq. (23)

### Mục tiêu

Hỗ trợ chọn M_prime để đạt U_target >= alpha. Ưu tiên: P2.

### Lý do

Proposition 3 có ích nhưng mô tả tìm kiếm còn chưa rõ.

### Đầu vào

M, alpha, U_unsup_target, cận và tolerance.

### Đầu ra

M_prime ứng viên và residual bất đẳng thức.

### Hiện thực

Tìm trên miền đã kiểm tra và đánh giá trực tiếp Eq. (23), không giả định đơn điệu toàn cục.

### Tham chiếu bài báo

sSMC-FCM Eq. (23), Proposition 3, PDF trang 8-9.

### Tiêu chí chấp nhận

- Tái lập ví dụ M_prime=5.582 trong tolerance.
- Giá trị trả về lớn hơn M và thỏa Eq. (23).
- Có test cho alpha nơi khẳng định đơn điệu không áp dụng toàn cục.

### Phụ thuộc

PB-24, PB-05.

## Milestone 4 - Chỉ số đánh giá

## PB-26 - Chuyển nhãn cứng và kernel đếm cặp

### Mục tiêu

Chuẩn hóa labels và tính a,b,c,d. Ưu tiên: P1.

### Lý do

Ba chỉ số ngoại tại dùng cùng pair counts; sSMC-FCM trả U mờ.

### Đầu vào

U hoặc nhãn dự đoán, nhãn ground truth.

### Đầu ra

Nhãn cứng và bốn số đếm.

### Hiện thực

Argmax có quy tắc hòa xác định; pair counts không phụ thuộc tên nhãn.

### Tham chiếu bài báo

Validity Section 3, định nghĩa trước Eq. (51).

### Tiêu chí chấp nhận

- a+b+c+d = N(N-1)/2.
- Hoán vị nhãn không đổi counts.
- Quy tắc hòa được ghi rõ.

### Phụ thuộc

PB-24.

## PB-27 - RI, ARI và Jaccard

### Mục tiêu

Hiện thực các chỉ số ngoại tại từ bài báo. Ưu tiên: P1.

### Lý do

Survey dùng ARI và Jaccard trong thí nghiệm; RI là định nghĩa cơ sở.

### Đầu vào

y_true, y_pred.

### Đầu ra

Ba score.

### Hiện thực

Eqs. (51)-(53), có policy cho mẫu số biên.

### Tham chiếu bài báo

Validity Sections 3.1-3.3.

### Tiêu chí chấp nhận

- Phân hoạch hoàn hảo cho score 1.
- Bất biến với hoán vị nhãn.
- Ví dụ Fig. 5 cho RI xấp xỉ 0.6786.
- Cross-check thư viện tin cậy trên trường hợp ngẫu nhiên.

### Phụ thuộc

PB-26.

## PB-28 - Bộ chỉ số nội tại cốt lõi

### Mục tiêu

Hiện thực SWC, SSWC, VRC và PBM. Ưu tiên: P1.

### Lý do

Survey kết luận silhouettes, PBM và VRC có kết quả tổng thể tốt; SSWC rẻ hơn SWC.

### Đầu vào

X và hard labels.

### Đầu ra

Các score và lỗi rõ cho trường hợp không xác định.

### Hiện thực

Dùng validity Eqs. (1)-(8),(18)-(21); singleton có silhouette 0.

### Tham chiếu bài báo

Validity Sections 2.1.1, 2.1.5, 2.1.7, 2.1.9 và Section 7.

### Tiêu chí chấp nhận

- SWC trong [-1,1], đúng quy ước singleton.
- VRC/PBM hữu hạn khi hợp lệ.
- Trùng ví dụ thủ công và thư viện tin cậy.
- Từ chối k<2, cụm rỗng và mẫu số 0.

### Phụ thuộc

PB-07.

## PB-29 - Danh mục đầy đủ 40 tiêu chuẩn

### Mục tiêu

Hiện thực phần còn lại của survey nếu cần nghiên cứu đầy đủ. Ưu tiên: P2.

### Lý do

Bài báo khảo sát 40 tiêu chuẩn nhưng không phải tất cả đều cần cho MVP.

### Đầu vào

X, labels và chuỗi phân hoạch cho chỉ số dạng sai khác.

### Đầu ra

13 họ tối ưu không-Dunn, 18 biến thể Dunn và 9 chỉ số dạng sai khác.

### Hiện thực

Tái sử dụng kernel khoảng cách/scatter; dùng slogdet; Eq. (37) cần k-1,k,k+1.

### Tham chiếu bài báo

Validity Section 2, Eqs. (1)-(50), Table 1.

### Tiêu chí chấp nhận

- Registry đếm đúng 40 tiêu chuẩn.
- Mỗi metric có chiều tối ưu, miền và điều kiện không xác định.
- Covariance/determinant suy biến có diagnostic.
- Transform dạng sai khác xử lý mẫu số 0.

### Phụ thuộc

PB-28.

## Milestone 5 - Thí nghiệm

## PB-30 - Fixture bộ dữ liệu 20 điểm

### Mục tiêu

Mã hóa chính xác dữ liệu trong hai bài thuật toán. Ưu tiên: P0.

### Lý do

Dùng chung cho tái lập sSFCM và sSMC-FCM.

### Đầu vào

sSFCM Table I / sSMC-FCM Table 1.

### Đầu ra

X:(20,2), supervision fixtures và kết quả làm tròn mong đợi.

### Hiện thực

Nhập tọa độ theo bảng; mã dùng index 0-based, bài báo dùng 1-based.

### Tham chiếu bài báo

sSFCM Table I; sSMC-FCM Table 1.

### Tiêu chí chấp nhận

- Đủ 20 tọa độ đúng bài báo.
- Mẫu 9,10 ánh xạ thành index 8,9.
- Fixture không bị mutation trong test.

### Phụ thuộc

PB-04.

## PB-31 - Tái lập sSMC-FCM Table 3

### Mục tiêu

Tái lập ba trường hợp trong bài báo. Ưu tiên: P1.

### Lý do

Đây là acceptance test khoa học quan trọng nhất.

### Đầu vào

PB-30; C=2, M=2, M'=2/4/8, mẫu 9,10 vào cụm 1, epsilon=1e-3.

### Đầu ra

Báo cáo membership, tâm và số vòng.

### Hiện thực

Chạy với initialization cố định, căn chỉnh hoán vị cụm và so số làm tròn.

### Tham chiếu bài báo

sSMC-FCM Section 4, Table 3.

### Tiêu chí chấp nhận

- Độ thuộc target có xu hướng 0.19 -> 0.43 -> 0.60.
- Tâm khớp ba chữ số nếu tìm được initialization phù hợp; nếu không phải báo ambiguity.
- Ghi nhận “khoảng 10 vòng”, không ép chính xác.
- Không tinh chỉnh công thức để khớp bảng.

### Phụ thuộc

PB-24, PB-30.

## PB-32 - Experiment runner và logging có cấu trúc

### Mục tiêu

Chạy FCM, sSFCM và sSMC-FCM trên cùng dữ liệu/cấu hình. Ưu tiên: P1.

### Lý do

Bảo đảm so sánh công bằng và tái lập được.

### Đầu vào

Dataset, supervision split, seeds và parameter grid.

### Đầu ra

Cấu hình/kết quả máy đọc được và bảng tóm tắt.

### Hiện thực

Ghi seed, initialization, runtime, iterations, objective, delta tâm, residual và metrics.

### Tham chiếu bài báo

sSMC-FCM Section 4; validity Sections 4-6.

### Tiêu chí chấp nhận

- Mỗi run có đủ cấu hình để chạy lại.
- Baseline dùng cùng tâm ban đầu khi phù hợp.
- Không ghi đè kết quả im lặng.
- Run không hội tụ có trạng thái riêng.

### Phụ thuộc

PB-11, PB-15, PB-24, PB-27, PB-28.

## PB-33 - Bộ sinh split có nhãn/không nhãn

### Mục tiêu

Tạo supervision có seed và không làm rò nhãn đánh giá. Ưu tiên: P1.

### Lý do

Cần đo ảnh hưởng tỷ lệ mẫu có nhãn một cách lặp lại.

### Đầu vào

y_true, tỷ lệ/số lượng có nhãn, seed, tùy chọn stratify.

### Đầu ra

target_cluster, mask và U_bar riêng cho sSFCM.

### Hiện thực

Tách nhãn dùng để supervise khỏi nhãn chỉ dùng evaluation.

### Tham chiếu bài báo

Không có protocol split trong bài sSMC-FCM; đây là hạ tầng thí nghiệm.

### Tiêu chí chấp nhận

- Cùng seed cho cùng split.
- Đúng số mẫu có nhãn, không trùng.
- Model không nhận truth của mẫu unlabeled.
- Stratified mode có test cho lớp nhỏ.

### Phụ thuộc

PB-17.

## Milestone 6 - Kiểm chứng

## PB-34 - Unit test theo từng phương trình

### Mục tiêu

Kiểm thử riêng từng thành phần toán học. Ưu tiên: P0.

### Lý do

Lỗi công thức có thể bị che bởi vòng fit.

### Đầu vào

Mảng nhỏ tính tay.

### Đầu ra

Test cho Eqs. (7),(8),(10),(15),(17)-(20),(23).

### Hiện thực

So vectorized implementation với scalar reference và các đồng nhất thức residual.

### Tham chiếu bài báo

sSMC-FCM Section 3.

### Tiêu chí chấp nhận

- Mỗi phương trình có test chuẩn và test biên.
- Kiểm tra Eq. (16) sau khi chạy Eqs. (17)-(20).
- Thông báo lỗi nêu rõ phương trình.

### Phụ thuộc

PB-18 đến PB-25.

## PB-35 - Test bất biến và ổn định số

### Mục tiêu

Bảo vệ simplex, finite values và edge cases. Ưu tiên: P0.

### Lý do

Tỷ số khoảng cách và số mũ nhạy với zero, scale và M gần 1.

### Đầu vào

Mảng ngẫu nhiên và trường hợp bất lợi.

### Đầu ra

Parameterized tests.

### Hiện thực

Test điểm trùng, zero distance, scale lớn/nhỏ, cụm gần rỗng, M gần 1 và M' lớn.

### Tham chiếu bài báo

Ràng buộc sau Eq. (7); docs/ptyc.md Section 12.

### Tiêu chí chấp nhận

- Không NaN/Inf im lặng.
- Tổng hàng membership đúng tolerance.
- Luôn báo residual solver.
- Đầu vào sai phát sinh lỗi có ý nghĩa.

### Phụ thuộc

PB-34.

## PB-36 - Test hội tụ và tính xác định

### Mục tiêu

Kiểm tra hành vi của vòng lặp. Ưu tiên: P0.

### Lý do

Bài báo dùng delta tâm và báo khoảng 10 vòng trong ví dụ.

### Đầu vào

Bộ 20 điểm, synthetic blobs và seed cố định.

### Đầu ra

Regression tests cho histories và trạng thái dừng.

### Hiện thực

Kiểm tra criterion, max_iter, deterministic history và objective.

### Tham chiếu bài báo

sSMC-FCM Step 4 và Section 4.

### Tiêu chí chấp nhận

- converged_ phù hợp delta tâm cuối.
- Cùng seed/cấu hình cho cùng trạng thái.
- Objective tăng quá tolerance làm test fail để điều tra, không bị clip.
- Hết max_iter có warning/trạng thái rõ.

### Phụ thuộc

PB-24, PB-35.

## PB-37 - Cổng tái lập end-to-end

### Mục tiêu

Đặt cổng chất lượng trước khi công bố hiện thực. Ưu tiên: P0.

### Lý do

Unit test không thay thế tái lập khoa học.

### Đầu vào

Báo cáo PB-16 và PB-31, metrics và cấu hình đầy đủ.

### Đầu ra

Báo cáo kiểm chứng có phiên bản.

### Hiện thực

Chạy FCM, sSFCM, sSMC-FCM; so bảng, tâm, xu hướng và ghi ambiguity.

### Tham chiếu bài báo

sSFCM Tables I-II; sSMC-FCM Tables 1-3 và Section 4.

### Tiêu chí chấp nhận

- Lưu dữ liệu và tham số cùng báo cáo.
- Tách tolerance do làm tròn khỏi tolerance số học.
- Xử lý hoán vị nhãn.
- Mọi sai lệch có nguyên nhân hoặc nhãn [CẦN XÁC MINH].

### Phụ thuộc

PB-16, PB-27, PB-28, PB-31, PB-32, PB-36.

## Thứ tự lập trình khuyến nghị

Điểm bắt đầu tốt nhất là PB-06. Đường găng:

    PB-06 -> PB-07 -> PB-08 -> PB-09 -> PB-10 -> PB-11
          -> PB-12 -> PB-13 -> PB-15
          -> PB-17 -> PB-18 -> PB-19 -> PB-20 -> PB-21
          -> PB-22 -> PB-23 -> PB-24
          -> PB-34 -> PB-35 -> PB-36 -> PB-31 -> PB-37

PB-20, solver Eq. (19), là thành phần có rủi ro kỹ thuật cao nhất. PB-25 và PB-29 chỉ nên làm sau khi phần lõi và tái lập đã đạt.

