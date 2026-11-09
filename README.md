# Phân cụm mờ bán giám sát

Demo đồ án tiếng Việt chạy local bằng Streamlit: tái hiện bộ **20 điểm, 2 cụm**
của hai bài thuật toán; xem độ thuộc U, tâm cụm, từng vòng lặp, metrics và tải
kết quả để kiểm tra lại. Chạy offline sau khi cài đủ dependencies.

## Cài đặt và chạy trên Windows

Để lấy phiên bản này trên laptop, mở PowerShell và chạy (cần Git và Python):

```powershell
git clone --branch alternate-version --single-branch https://github.com/DrGamingScience/Fuzzy-Supervised-Learning.git
cd Fuzzy-Supervised-Learning
```

Mở PowerShell tại thư mục gốc repo. Môi trường đã có đủ dependencies thì dùng
ngay Python đó; không cần cài lại mỗi phiên. Môi trường riêng mới:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Mở **http://127.0.0.1:8501**. Dừng server bằng **Ctrl+C**. Nếu dùng môi trường
có sẵn, chạy `python -m streamlit run app.py`. Cấu hình `.streamlit/config.toml`
giới hạn server ở localhost, tắt thu thập thống kê; không cần tài khoản/hosting.
Phiên bản đã kiểm tra: Python 3.13.9; dependencies được pin trong
[requirements.txt](requirements.txt) và [requirements-dev.txt](requirements-dev.txt).
Chi tiết môi trường: [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md).

## Kịch bản demo

1. Mở phần **Dữ liệu và nhóm tham chiếu** để xem 20 điểm. Nhóm tham chiếu chỉ
   dùng đánh giá, không nằm trong hai tọa độ đưa vào fit. ID điểm/cụm từ 1.
2. Chọn **FCM**, giữ tâm demo `(2.7,5), (9.1,5)` rồi **Chạy thuật toán**.
   U của điểm 9 và 10 vào cụm 1 khoảng **0.188663**: hai điểm thuộc cụm cứng 2.
3. Chọn **sSFCM (m > 1)**, m=2. Preset B=0.3/0.6 áp vào ID 9,10 → cụm 1.
   Chạy lại: U tương ứng khoảng **0.451669/0.693818**. Có thể sửa B, ID, cụm
   đích, thêm/xóa hoặc bật/tắt dòng. **Khôi phục preset** bỏ các sửa bảng hiện tại.
   Đổi preset B cũng khôi phục hai dòng mặc định. Dòng tắt được bỏ qua.
4. Chọn **sSMC-FCM**, M=2, preset M′=4 hoặc 8, giữ hai dòng chỉ dẫn bật:
   U khoảng **0.428699/0.604491**. B không áp dụng cho thuật toán này; M′ là
   số mũ, không có quy đổi mặc định với B. M′ nhập tay phải ≥ M.
5. Kéo **Vòng lặp** về 0 rồi đến cuối. Biểu đồ, bảng U và tâm cùng lấy từ một
   snapshot; đổi vòng không fit lại. Các bảng metrics đánh giá **vòng cuối**.
6. Chọn **So sánh cả năm**, cấu hình m/M, M′, lambda và bảng giám sát chung,
   rồi chạy. Mọi thuật toán nhận cùng X và tâm đầu; FCM bỏ qua giám sát,
   sS/eS nhận B, sSMC nhận cụm đích. Bảng không xếp hạng bằng J chéo thuật toán.
7. Chọn kết quả cần xem, đọc cảnh báo và tải **ZIP của lần chạy đang hiển thị**.
   Nếu chỉnh cấu hình sau khi chạy, ứng dụng giữ kết quả cũ và đánh dấu rõ;
   chạy thành công mới thay kết quả/ZIP. Input sai không thay kết quả đã có.

Khởi tạo có hai lựa chọn: tâm demo cố định của dự án (không phải tâm đầu do
bài báo cung cấp), hoặc lấy mẫu điểm theo seed. Không chuẩn hóa dữ liệu demo.

## Công thức và quy ước

Trong mã, X: N×D; U: N×C; V: C×D. Chỉ số nội bộ từ 0, ID hiển thị/xuất từ 1.
Mỗi hàng U không âm, tổng 1; nhãn cứng = argmax U, hòa chọn cụm ID nhỏ nhất.

| Lựa chọn | Cập nhật U | Trọng số cập nhật tâm | Nguồn |
| --- | --- | --- | --- |
| FCM | Chuẩn hóa d²^(-1/(m−1)), m>1 | U^m | Khang 2021 (2),(3) |
| sSFCM m>1 | B + (1−tổng hàng B) × U_FCM | \|U−B\|^m | Endo 2009 (4),(6) |
| sSFCM m=1 | B + phần dư vào cụm gần nhất; hòa chọn ID nhỏ nhất | \|U−B\| | Endo 2009 (4),(8) |
| eSFCM | B + phần dư × softmax(−lambda d²) | U | Endo 2009 (10),(14) |
| sSMC-FCM | Giải (17)–(20), Brent trong tọa độ logit, kiểm tra residual | U^(m_ik) | Khang 2021 (7)–(20) |

B thuộc [0,1], tổng hàng ≤1; B là cận dưới, không phải U cuối bắt buộc bằng B.
Nếu tổng hàng B=1, U hàng đó cố định và trọng số phần dư của sSFCM bằng 0.
Hàm mục tiêu FCM/sSMC là tổng U^(m_ik)d²; sSFCM là tổng |U−B|^m d²;
eSFCM là tổng U d² + lambda^(-1) tổng (U−B)log|U−B|, quy ước 0 log 0=0.

sSMC chỉ nhận tối đa một cụm đích mỗi điểm; M′ cố định trong một lần fit,
không ép nhãn sau FCM. Root tolerance mặc định 1e-12 trong `Config`.
Softmax và trọng số tâm tính ổn định trong log. Nếu có nhiều tâm trùng điểm,
FCM/sSMC chia đều phần thuộc cho các tâm có khoảng cách 0; sSFCM m=1 vẫn
theo quy tắc hòa ở trên. Cụm mất trọng số giữ tâm trước và có cảnh báo.
Khoảng cách vượt miền số hoặc underflow không phân biệt được với 0 sẽ báo lỗi
yêu cầu đổi thang dữ liệu; không âm thầm trả NaN/Inf.

Vòng 0 lưu U tính từ tâm khởi tạo. Mỗi vòng cập nhật tâm từ U trước đó rồi
tính lại U tại tâm mới, J và snapshot. Dừng khi `max_k ||V_k mới−V_k cũ||₂`
≤ epsilon, hoặc hết max_iter; trạng thái xuất là `epsilon` / `max_iter`.
Snapshot là bản sao chỉ đọc; số vòng không bắt buộc giống bài báo.

## Metrics và giới hạn diễn giải

| Metric | Chiều tốt | Quy ước |
| --- | --- | --- |
| Silhouette | Lớn | Khoảng cách Euclid; singleton có silhouette=0 |
| Calinski–Harabasz (CH) | Lớn | Tỷ số phân tán giữa/trong cụm |
| Davies–Bouldin (DB) | Nhỏ | Phân tán là khoảng cách trung bình đến tâm cứng |
| Dunn gốc | Lớn | Min khoảng cách điểm khác cụm / max đường kính nội cụm |
| PBM | Lớn | `((E1/Ek) × Dk/k)^2`; E là tổng khoảng cách Euclid, Dk là khoảng cách tâm lớn nhất |
| ARI | Lớn | Điều chỉnh ngẫu nhiên trên cặp điểm; có thể âm |
| Jaccard theo cặp | Lớn | a/(a+b+c) trên cặp điểm, không so trực tiếp mã nhãn |

Tâm metrics tính từ **nhãn cứng**, không dùng tâm mờ V. Metrics hình học cần
2 ≤ số cụm cứng thực tế < N. Mẫu số 0/tâm trùng có trạng thái không xác định
và lý do; không thay bằng 0. Silhouette và Dunn dùng khoảng cách theo cặp O(N²).

ARI/Jaccard bất biến khi đổi tên cụm, có hai phạm vi: toàn bộ và chưa giám sát.
FCM: mọi điểm chưa giám sát. sS/eS: hàng B có ô dương là đã giám sát.
sSMC: điểm có cụm đích là đã tiết lộ, kể cả khi M′=M. Ít hơn hai điểm hoặc
không có nhãn tham chiếu: không xác định. ARI=1 cho hai phân hoạch suy biến
tương đương; Jaccard=1 khi hai tập cặp cùng cụm đều rỗng.

Các chỉ số trên nhãn cứng không đánh giá đầy đủ thông tin mờ. Kết quả 20 điểm
không chứng minh ưu thế tổng quát; J của các thuật toán có định nghĩa khác nhau.

## Sai khác với bảng nguồn

- FCM tâm thứ hai tính được 9.017398, phù hợp 9.018 của bài 2021; bài 2009
  Table V ghi 9.08.
- eSFCM lambda=1: thay tâm Table V `(4.60,5),(8.33,5)` và X1=(0,4.5)
  vào (14) cho U1,2 khoảng 1.13e-21, khác 0.24 của Table IV. Mã theo công
  thức, UI/ZIP luôn giữ cảnh báo; nguyên nhân sai khác nguồn chưa xác định.
- Table 3 (2021), M′=4, ID 17/19 in 0.11. Tại chính tâm công bố, (15) cho
  0.10452027; hội tụ mã cho 0.10451687. Tests ghi nhận riêng hai hàng này,
  giữ nguyên fixture và dung sai 0.005 cho các hàng còn lại.

Chi tiết đối chiếu nguồn và dung sai: [docs/VALIDATION.md](docs/VALIDATION.md).

## Tệp xuất và API Python

ZIP gồm `result.json` strict (không NaN/Inf), `data.csv`, `supervision.csv`,
`comparison.csv`, hướng dẫn tiếng Việt, và thư mục mỗi thuật toán chứa U/nhãn,
tâm, lịch sử J/shift và metrics. CSV là UTF-8 BOM. JSON lưu cả seed, cấu hình,
tâm đầu, B/cụm đích, mặt nạ giám sát, thời gian/trạng thái dừng, cảnh báo và
**mọi snapshot**. Nhãn tham chiếu giữ mã gốc 0/1 của demo, tách khỏi X.

```python
from src.algorithms import Config, fit
from src.data import load_paper_data, demo_initial_centers, ssmc_preset

X, y = load_paper_data()  # y chỉ để đánh giá, không truyền vào fit
preset = ssmc_preset(8)
result = fit(X, Config(algorithm="ssmc", m_prime=8),
             initial_centers=demo_initial_centers(), targets=preset.targets)
print(result.membership[8])  # ID 9: khoảng [0.604491, 0.395509]
```

Điều phối/so sánh/xuất: `src.experiments.run_experiment`, `comparison_table`,
`export_zip`. Tham số `reference` chỉ phục vụ metrics sau fit.

## Kiểm thử

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m json.tool feature_list.json > $null
```

Hoặc thay đường dẫn venv bằng `python` của môi trường đang dùng.
Đã chạy **139 tests PASS**: công thức/bảng nguồn, tối ưu độc lập SLSQP, KKT,
baseline, biên số học, mọi snapshot, đối chiếu metrics với sklearn/đếm tay,
đọc lại ZIP/CSV/JSON, AppTest luồng demo và server localhost khởi động/dừng.
Không coi smoke dependency hoặc tính thử nghiên cứu là test thuật toán.
Giới hạn kiểm thử UI/editor: [docs/QA.md](docs/QA.md); chưa tuyên bố kiểm tra
trực quan mọi trình duyệt. Quy trình/checkpoint: [progress.md](progress.md),
[feature_list.json](feature_list.json), [docs/WORKFLOW.md](docs/WORKFLOW.md).

## Cấu trúc và tài liệu nguồn

- `src/data.py`: tọa độ, nhóm tham chiếu riêng, preset và tâm demo.
- `src/algorithms.py`: Config/validation, 5 thuật toán, snapshot và dừng.
- `src/metrics.py`: năm metrics hình học, ARI/Jaccard, báo cáo hai phạm vi.
- `src/experiments.py`: bảng chỉ dẫn, điều phối cùng điều kiện, xuất ZIP.
- `src/ui.py`, `app.py`: điều khiển, hiển thị và lưu kết quả phiên Streamlit.
- `tests/`: kiểm chứng mã mới, fixture chép từ bảng nguồn.
- Endo và cộng sự, *On Semi-Supervised Fuzzy c-Means Clustering* (2009):
  [PDF gốc](<docs/FCM Bán giám sát - yasunori2009.pdf>), công thức (2)–(14), Tables I–V.
- Khang, Tran, Fowler, *A Novel Semi-Supervised Fuzzy C-Means Clustering Algorithm
  Using Multiple Fuzzification Coefficients* (2021):
  [PDF gốc](docs/algorithms-14-00258-v2.pdf), công thức (2)–(20), Tables 1–3.
- Vendramin, Campello, Hruschka, *Relative Clustering Validity Criteria:
  A Comparative Overview* (2010):
  [PDF gốc](<docs/Relative Clustering Validity Criteria A Comparative Overview 2010.pdf>), metrics mục 2.

Phạm vi đã giao: hết DOC-002, dừng trước `LATER-001`. Notebook thuyết trình,
CSV/dữ liệu lớn, benchmark nhiều seed, chọn M′ theo alpha và metrics mở rộng
vẫn để phase sau; đây chưa phải tái hiện toàn bộ 40 tiêu chí/nghiên cứu metrics.
