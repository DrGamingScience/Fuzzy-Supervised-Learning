# Nhật ký Tiến độ

## Trạng thái Đã xác minh Hiện tại

- Repo: `D:\Downloads\Semi-supervised-learning`; branch `main`; baseline task `4385c81635392a968749faaa91287f4ceaddc17d`; working tree sạch trước INIT.
- Khởi động: `python -m streamlit run app.py`; kiểm tra: `python -m pytest -q`.
- Task duy nhất: `UI-004` — INIT pass, EXE đang làm; phạm vi đã giao đến DOC-002, không làm LATER.
- Môi trường: Anaconda Python 3.13.9; imports NumPy/SciPy/pandas/sklearn/Streamlit/Plotly đã kiểm tra.
- Blocker: không có; không có thay đổi người dùng có sẵn.

## Nhật ký Phiên

### Phiên 028

- Ngày: 2026-11-09T23:23:35+07:00 (Asia/Saigon).
- Mục tiêu: UI-004 — Biểu đồ, bảng U và chọn vòng lặp. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: app.py, src/ui.py, tests/test_app.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Biểu đồ điểm/tâm và bảng U khớp snapshot đang chọn; Thanh chọn từ vòng 0 đến cuối và đường hội tụ; Đổi vòng không chạy lại fit và không làm mất kết quả.
- INIT: branch main, HEAD `4385c81635392a968749faaa91287f4ceaddc17d`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_app.py tests/test_history.py PASS: 10 tests. Chạy đơn, bảng U/tâm đúng vòng, Plotly/hội tụ và slider0..cuối; spy chứng minh đổi vòng không fit lại. Lỗi test tooling ban đầu: AppTest dataframe không callable theo key, sửa truy xuất theo schema cột; UI không lỗi. Diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: chờ acceptance tests và review diff.
- Tệp hoặc artifact đã cập nhật: app.py, src/ui.py, tests/test_app.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: hoàn tất EXE và COMMIT của UI-004.

### Phiên 027

- Ngày: 2026-11-09T23:22:42+07:00 (Asia/Saigon).
- Mục tiêu: UI-003 — Bảng sửa chỉ dẫn giám sát. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: app.py, tests/test_app.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Sửa/bật/tắt chỉ dẫn theo ID, cụm đích và độ thuộc khi áp dụng; Lỗi nhập có thông báo, không chạy với dữ liệu sai; M' và độ thuộc B không bị diễn giải là cùng tham số.
- INIT: branch main, HEAD `1a0a943011f0815e1b6c9898c4bc6ec365f69733`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_app.py tests/test_experiments.py PASS: 15 tests. AppTest sửa bảng gây trùng được báo lỗi, reset/preset0.6, dòng tắt bỏ qua, FCM bỏ qua bảng; validation EXE chặn dữ liệu sai. Diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `5517e0459d62a8686e2ee477244a94882e4e7494` (UI-003); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: app.py, tests/test_app.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: UI-004; working tree task sẽ sạch sau commit metadata.

### Phiên 026

- Ngày: 2026-11-09T23:22:00+07:00 (Asia/Saigon).
- Mục tiêu: UI-002 — Chọn thuật toán, tham số và preset. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: app.py, tests/test_app.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Chọn được năm thuật toán và tham số phù hợp; Preset 0 / 0.3 / 0.6, M' = 4 / 8; Seed/khởi tạo, epsilon và giới hạn vòng rõ ràng.
- INIT: branch main, HEAD `b3478a9ec394cb3798386bf377eabfed07d0b2bb`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_app.py PASS: 2 AppTests, chọn 5 thuật toán, preset B và Mprime8, tham số theo thuật toán, seed/tâm đầu/epsilon/max_iter rõ; diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `761c2cd413a9d59b1abc13588c97729b5f9229b8` (UI-002); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: app.py, tests/test_app.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: UI-003; working tree task sẽ sạch sau commit metadata.

### Phiên 025

- Ngày: 2026-11-09T23:21:17+07:00 (Asia/Saigon).
- Mục tiêu: UI-001 — Khung UI offline và dữ liệu demo. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: app.py, tests/test_app.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: UI tiếng Việt đơn giản, xem được 20 điểm và nhóm tham chiếu; Chạy trên localhost với assets cục bộ; Không lẫn nhãn tham chiếu vào dữ liệu fit.
- INIT: branch main, HEAD `825ae998d98bf1a0a971920d9008d8262d4f690e`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_app.py tests/test_server.py PASS: 2 tests. AppTest hiển thị 20 điểm/ID/nhóm tham chiếu, Plotly assets local; server localhost health/HTML/dừng pass. Nhãn không vào X đã kiểm tra EXP-001. Diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `2926add1ff82c333ed26af3d4a8c2def646bae56` (UI-001); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: app.py, tests/test_app.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: UI-002; working tree task sẽ sạch sau commit metadata.

### Phiên 024

- Ngày: 2026-11-09T23:20:38+07:00 (Asia/Saigon).
- Mục tiêu: EXP-002 — Xuất dữ liệu và kết quả tái lập. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/experiments.py, tests/test_export.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Xuất cấu hình, dữ liệu, U, tâm, nhãn, metrics, giám sát và mọi snapshot; Đọc lại ZIP/CSV/JSON và đối chiếu với kết quả gốc; JSON không có NaN/Inf, CSV đọc được tiếng Việt.
- INIT: branch main, HEAD `faf873cfa204d9b4664aa63dd1a8395b6e5e40d5`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_export.py tests/test_experiments.py PASS: 14 tests. Đọc lại ZIP JSON strict và CSV UTF-8 BOM, toàn bộ X/B/targets/U/V/nhãn/config/metrics/warnings/mọi snapshot; undefined là null; diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `8450c58a3e8845a7b0621b44d9d25e6f005f487d` (EXP-002); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/experiments.py, tests/test_export.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: UI-001; working tree task sẽ sạch sau commit metadata.

### Phiên 023

- Ngày: 2026-11-09T23:19:38+07:00 (Asia/Saigon).
- Mục tiêu: EXP-001 — Chuyển bảng giám sát và bảng so sánh. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/experiments.py, tests/test_experiments.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Kiểm tra ID, trùng điểm, miền độ thuộc và dòng tắt; So sánh cùng dữ liệu/khởi tạo, công bố tham số; Không dùng J để xếp hạng khác thuật toán.
- INIT: branch main, HEAD `049414b6f1862fdae533f101910229d5fb6eea83`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_experiments.py tests/test_metrics.py PASS: 31 tests. ID/cụm từ 1, trùng bật, dòng tắt, B độc lập targets; 5 thuật toán cùng X/tâm đầu/giám sát, sao chép input, công bố cấu hình, bảng không so J; diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `797c2d6823f318b73a4dab1560e4b98ee1684c63` (EXP-001); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/experiments.py, tests/test_experiments.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: EXP-002; working tree task sẽ sạch sau commit metadata.

### Phiên 022

- Ngày: 2026-11-09T23:18:36+07:00 (Asia/Saigon).
- Mục tiêu: MET-003 — Báo cáo toàn bộ và điểm chưa giám sát. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/metrics.py, tests/test_metrics.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Mặt nạ giám sát đúng theo từng thuật toán; Có ARI/Jaccard cho toàn bộ và chưa giám sát; Ít hơn hai điểm có trạng thái không xác định.
- INIT: branch main, HEAD `3fd263e80c45784630932f7befee62ddd61f922d`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_metrics.py PASS: 19 tests. Mask đúng 5 thuật toán, toàn bộ/chưa giám sát, thiếu nhãn, tập 0/1 điểm và mask sai; diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `abca92413ccf5eb2a64ba9d90aca5e8b5a363729` (MET-003); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/metrics.py, tests/test_metrics.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: EXP-001; working tree task sẽ sạch sau commit metadata.

### Phiên 021

- Ngày: 2026-11-09T23:17:57+07:00 (Asia/Saigon).
- Mục tiêu: MET-002 — ARI và Jaccard theo cặp. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/metrics.py, tests/test_metrics.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Đếm cặp đúng và bất biến theo hoán vị mã cụm; Đối chiếu số đếm tay và ARI thư viện; Quy ước phân hoạch suy biến được giải thích.
- INIT: branch main, HEAD `6d0f436d08bbc2e454cf3a0dd8868cc44c0b6e6d`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_metrics.py PASS: 13 tests. Đếm cặp tay và brute force, ARI sklearn 5 seed, hoán vị mã, Jaccard theo cặp và phân hoạch suy biến; diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `f0265de86a84d711d8852cdc487cae355e0b9792` (MET-002); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/metrics.py, tests/test_metrics.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: MET-003; working tree task sẽ sạch sau commit metadata.

### Phiên 020

- Ngày: 2026-11-09T23:16:22+07:00 (Asia/Saigon).
- Mục tiêu: MET-001 — Năm metrics hình học. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/metrics.py, tests/test_metrics.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Silhouette, CH, DB, Dunn gốc và PBM đúng định nghĩa; Tâm từ nhãn cứng và chiều tối ưu đúng; Có đối chiếu độc lập; báo giá trị không xác định và lý do.
- INIT: branch main, HEAD `8b70e382eed3275ea9f9a0022aa797473966cc76`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_metrics.py PASS: 6 tests. SWC/CH/DB đối chiếu sklearn 3 seed và tay; Dunn gốc min liên cụm/max đường kính, PBM E1=16 Ek=4 Dk=8 k=2 cho 256. Kỳ vọng PBM ban đầu tính nhầm 400, sửa biểu thức theo công thức, src giữ nguyên. Undefined/singleton có lý do. Diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `cc59b6db1e3abc5b4b0c2c2c95bac9f5738b0a89` (MET-001); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/metrics.py, tests/test_metrics.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: MET-002; working tree task sẽ sạch sau commit metadata.

### Phiên 019

- Ngày: 2026-11-09T23:14:40+07:00 (Asia/Saigon).
- Mục tiêu: TEST-001 — Bộ kiểm chứng toán và bảng bài báo. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: tests/test_paper.py, tests/fixtures/paper_memberships.csv, docs/VALIDATION.md. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Có tests kiểm chứng đúng công thức, ví dụ, baseline, KKT và trường hợp biên; Chạy pytest thành công và lưu lệnh/kết quả; Phân biệt tính thử nghiên cứu với kiểm thử trên mã src.
- INIT: branch main, HEAD `8a0dbcf02e5d27e0b3bf84978c315bef184ed5e0`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q PASS: 94 tests. Bảng nguồn 20 điểm, Table III, SLSQP độc lập cả 5 mục tiêu, KKT/biên/history. Phát hiện sai khác Table 3 Mprime=4 ID17/19: 0.11 in, 0.10452027 theo (15) tại tâm nguồn; giữ fixture và test sai khác riêng, không nới tolerance. Diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `15288fbcf92cc8b1e8e5d10c0900e4abbcb1ffb7` (TEST-001); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: tests/test_paper.py, tests/fixtures/paper_memberships.csv, docs/VALIDATION.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: MET-001; working tree task sẽ sạch sau commit metadata.

### Phiên 018

- Ngày: 2026-11-09T23:14:23+07:00 (Asia/Saigon).
- Mục tiêu: CORE-003 — Snapshot và trạng thái hội tụ. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/algorithms.py, tests/test_history.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Snapshot giữ U tính theo chính V được lưu; Công bố vòng 0 và chuẩn dừng; Lịch sử không bị sửa sau các vòng sau, có trạng thái đạt epsilon/max_iter.
- INIT: branch main, HEAD `7016448698800632909d0f46efb3c230164ac600`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_algorithms.py tests/test_numerics.py tests/test_history.py PASS: 55 tests. Mọi snapshot 0..cuối của 5 thuật toán có U(V), J đúng, J không tăng, shift và epsilon/max_iter rõ; bản sao chỉ đọc không bị vòng sau sửa; diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `64313e538d8429df3390c6e593aa99404d3008a4` (CORE-003); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/algorithms.py, tests/test_history.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: TEST-001; working tree task sẽ sạch sau commit metadata.

### Phiên 017

- Ngày: 2026-11-09T23:13:42+07:00 (Asia/Saigon).
- Mục tiêu: CORE-002 — Trường hợp suy biến và ổn định số. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/algorithms.py, tests/test_numerics.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Kiểm tra điểm trùng tâm, nhiều tâm trùng, điểm trùng và tổng B bằng 1; Mất trọng số có xử lý và cảnh báo rõ; Không âm thầm trả NaN/Inf hoặc phá ràng buộc U.
- INIT: branch main, HEAD `0491176e2a345c127bd3edaa8cd0551c9edd2ace`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_algorithms.py tests/test_numerics.py PASS: 49 tests. Trùng điểm/tâm, B tổng 1, cụm mất trọng số cảnh báo, exponent=10000/20000 tính log, scale overflow/underflow báo lỗi rõ. Test ban đầu bỏ sót entropy âm eSFCM khi khoảng cách=0; sửa kỳ vọng theo (9): -4 log 2, không đổi công thức. Diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `a026a1462d535d708ccbd599936bac8234870a2b` (CORE-002); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/algorithms.py, tests/test_numerics.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: CORE-003; working tree task sẽ sạch sau commit metadata.

### Phiên 016

- Ngày: 2026-11-09T23:12:52+07:00 (Asia/Saigon).
- Mục tiêu: ALG-005 — sSMC-FCM với M' thủ công. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/algorithms.py, tests/test_algorithms.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Giải (17)-(20), tâm dùng U^(m_ik); Kiểm tra residual/KKT tại các nghiệm cập nhật; M' = M thu về FCM, M' = 4 / 8 cho U9,1 gần 0.43 / 0.60.
- INIT: branch main, HEAD `8cf61344331ca17e6787baf08c8a9875ef1ebd1d`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_algorithms.py PASS: 36 tests. Giải (17)-(20) bằng logit/Brent có bracket và residual; KKT 2/3 cụm độc lập; Mprime=M trùng FCM, U9=0.428699/0.604491; tâm đúng số mũ; diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `446db53d2cf07d8e6664995a0e5f2f3cff03570d` (ALG-005); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/algorithms.py, tests/test_algorithms.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: CORE-002; working tree task sẽ sạch sau commit metadata.

### Phiên 015

- Ngày: 2026-11-09T23:11:35+07:00 (Asia/Saigon).
- Mục tiêu: ALG-004 — eSFCM entropy. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/algorithms.py, tests/test_algorithms.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Công thức (14), tâm trọng số U và entropy đúng bài 2009; Softmax ổn định và quy ước 0 log 0 rõ ràng; Kiểm tra trực tiếp công thức, báo sai khác bảng thay vì ép khớp bảng.
- INIT: branch main, HEAD `340a7a5dda30fe26655bead645c27ad7ccb6e06f`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_algorithms.py PASS: 32 tests. Công thức (14), tâm U, entropy độc lập, lambda lớn/0 log 0; thay tâm Table V cho U1,2=1.13e-21 thay vì 0.24, cảnh báo minh bạch; diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `6e1bbcb50e04528196f2776c9e22c984ab774084` (ALG-004); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/algorithms.py, tests/test_algorithms.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: ALG-005; working tree task sẽ sạch sau commit metadata.

### Phiên 014

- Ngày: 2026-11-09T23:11:25+07:00 (Asia/Saigon).
- Mục tiêu: ALG-003 — sSFCM m = 1. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/algorithms.py, tests/test_algorithms.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Nhánh riêng không chia cho m-1; Phần dư được gán theo cụm gần nhất, quy tắc hòa rõ ràng; Đối chiếu Table III 2009 và trường hợp B = 0.
- INIT: branch main, HEAD `40adc5f34a84cc0fc4b05c7a940f84eb166ba641`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_algorithms.py PASS: 30 tests. Toàn bộ Table III 2009 (20 điểm x 3 case) khớp; nhánh m=1/tie và tâm phần dư kiểm tra độc lập; diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `0f44e19ce8f123bac596e0f7d967973b2a02168a` (ALG-003); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/algorithms.py, tests/test_algorithms.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: ALG-004; working tree task sẽ sạch sau commit metadata.

### Phiên 013

- Ngày: 2026-11-09T23:11:01+07:00 (Asia/Saigon).
- Mục tiêu: ALG-002 — sSFCM m > 1. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/algorithms.py, tests/test_algorithms.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Cập nhật U có cận dưới B, tâm dùng trọng số |U-B|^m; B = 0 thu về FCM cùng điều kiện; U9,1 gần 0.45 / 0.69 với B = 0.3 / 0.6.
- INIT: branch main, HEAD `5f779651aa4c119f00d71ff63dc611e427509f89`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_algorithms.py PASS: 26 tests; U9=0.451669/0.693818, B=0 trùng FCM, đối chiếu độc lập tâm trọng số phần dư; diff review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `6e34ccade2f6bd7049aaeb47dd77456541959242` (ALG-002); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/algorithms.py, tests/test_algorithms.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: ALG-003; working tree task sẽ sạch sau commit metadata.

### Phiên 012

- Ngày: 2026-11-09T23:09:59+07:00 (Asia/Saigon).
- Mục tiêu: ALG-001 — FCM đối chứng. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/algorithms.py, tests/test_algorithms.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Cập nhật U và V đúng công thức; U9,1 gần 0.19 và tâm phù hợp ví dụ 2021; Hữu hạn, tổng hàng U bằng 1 và hành vi dừng rõ ràng.
- INIT: branch main, HEAD `e491dca934cf3e16b8fc453aa548daa2571f4eac`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q tests/test_algorithms.py PASS: 23 tests. FCM U9=0.188663, V theo 2021 trang 10; cập nhật độc lập, seed, zero và max_iter. Lỗi test ban đầu: nhập nhầm tâm kỳ vọng 2.684338; nguồn 2021 trang 10 ghi 2.719, đã render/đối chiếu rồi sửa test, không đổi src. git diff đã review/check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `258266456c75f7a04ba987a5cf64f446df0c6d18` (ALG-001); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/algorithms.py, tests/test_algorithms.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: ALG-002; working tree task sẽ sạch sau commit metadata.

### Phiên 011

- Ngày: 2026-11-09T23:08:25+07:00 (Asia/Saigon).
- Mục tiêu: CORE-001 — Cấu hình và validation đầu vào. Yêu cầu: thực hiện hết feature đến trước later. Scope/files: src/algorithms.py, tests/test_algorithms.py. Không mở task tiếp theo trước khi commit task này. Acceptance criteria giữ nguyên: Kiểm tra shape, số hữu hạn, miền tham số và tổng hàng B; Thông báo lỗi rõ cho cấu hình sai; Tham số không áp dụng không gây hạn chế vô lý cho thuật toán khác.
- INIT: branch main, HEAD `e8394943e24b1d6bf1d9537f583a94d180e687eb`, git status sạch; interpreter/dependencies kế thừa ENV-001 đã kiểm tra lại đầu đợt; baseline liên quan PASS ở checkpoint trước (đầu đợt 28 tests). Không có thay đổi người dùng có sẵn.
- Đã hoàn thành: EXE và acceptance checks PASS; diff đã review trong scope, chờ commit.
- Xác minh đã chạy: python -m pytest -q PASS: 49 tests; shape/finiteness/config/B/targets và tham số không áp dụng; git diff --check PASS.
- Bằng chứng đã ghi lại: chỉ tính tests chạy trên src mới; không dùng kết quả khảo sát cũ thay nghiệm thu.
- Commit: `10286ef9e60c09b6b68cc87750c5536280d9bdef` (CORE-001); hồ sơ hậu commit được commit riêng trước task tiếp theo.
- Tệp hoặc artifact đã cập nhật: src/algorithms.py, tests/test_algorithms.py.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi đang mở trong scope; giới hạn ngoài scope giữ nguyên.
- Bước tốt nhất tiếp theo: ALG-001; working tree task sẽ sạch sau commit metadata.

### Phiên 010

- Ngày: 09/11/2026 (Asia/Saigon); bắt đầu 2026-11-09T22:59:18+07:00.
- Mục tiêu: DATA-001 — Viết mới bộ 20 tọa độ, nhãn tham chiếu tách khỏi X, tâm đầu demo và preset đúng nguồn/quy ước ID; không viết thuật toán/UI dữ liệu. Phạm vi: src/__init__.py, src/data.py, tests/test_data.py, tests/fixtures/paper_20_points.csv, docs/DATA.md, AGENTS.md, feature_list.json, progress.md. Tiêu chí: giữ nguyên acceptance_criteria của task trong JSON.
- Đã hoàn thành: DATA-001: viết mới đủ 20 tọa độ nguồn; X (20,2) và nhãn tham chiếu (20,) tách riêng, hai nhóm 10 điểm; tâm đầu cố định của demo, preset B 0/0.3/0.6 và M' 2/4/8 với ID 9,10 → cụm 1; bản sao độc lập và tài liệu nguồn/ID. INIT baseline 9149f4f và 10 regression tests PASS trước EXE.
- Xác minh đã chạy: 09/11/2026: python -m pytest -q tests/test_data.py PASS exit 0 (18 tests); python -m pytest -q PASS exit 0 (28 tests). Hai PDF trang 4 đã render bằng pdftoppm và xem; python tmp/check_pdf_data.py PASS exit 0 sau khi giới hạn đúng vùng bảng, đối chiếu cả 20 tọa độ với fixture và src. python tmp/check_records.py; python -m json.tool feature_list.json; git diff --check PASS.
- Bằng chứng đã ghi lại: yêu cầu người dùng “Thực hiện đến hết data-001”; làm DOC → ENV → INIT → DATA tuần tự, không triển khai CORE/ALG/UI.
- Commit: `95c3b77ae2063b74d6f138ac22d6196739680f7e` (DATA-001); metadata hậu commit được lưu bằng commit riêng trước task tiếp theo/handoff. Working tree sau commit triển khai sạch.
- Tệp hoặc artifact đã cập nhật: src/__init__.py, src/data.py, tests/test_data.py, tests/fixtures/paper_20_points.csv, docs/DATA.md, AGENTS.md, feature_list.json, progress.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Lỗi tooling tái hiện bằng python tmp/check_pdf_data.py bản đầu: pypdf layout không bắt được tọa độ; PyMuPDF đọc được nhưng parser ban đầu lấy cả Table 2 (U). Phân loại environment/tooling, đã sửa reader/vùng trích xuất, không đổi dữ liệu/expected/test để né lỗi. Không có lỗi sản phẩm đang mở; chưa triển khai CORE/ALG/UI dữ liệu.
- Bước tốt nhất tiếp theo: Đã hoàn thành phạm vi đến DATA-001. CORE-001 planned, chưa được giao; không có task đang mở.

### Phiên 009

- Ngày: 09/11/2026 (Asia/Saigon); bắt đầu 2026-11-09T22:57:55+07:00.
- Mục tiêu: INIT-001 — Tạo smoke tests môi trường độc lập thuật toán và entry point Streamlit chỉ báo sẵn sàng; xác minh chạy/trả trang/dừng. Phạm vi: app.py, tests/test_environment.py, tests/test_app.py, tests/test_server.py, AGENTS.md, feature_list.json, progress.md. Tiêu chí: giữ nguyên acceptance_criteria của task trong JSON.
- Đã hoàn thành: INIT-001: entry point chỉ báo sẵn sàng; smoke dependency, AppTest chạy script thật; subprocess server localhost trả health và HTML, dừng và xác nhận port đã đóng. INIT baseline 7b08bcc/imports/config pass trước EXE.
- Xác minh đã chạy: 09/11/2026: python -m pytest -q PASS exit 0, 10 tests (7 imports, numeric/table/chart smoke, AppTest, HTTP server lifecycle). python tmp/check_records.py và git diff --check PASS. Server test dùng port local trống, luôn dừng tiến trình trong finally; không có thuật toán/metrics.
- Bằng chứng đã ghi lại: yêu cầu người dùng “Thực hiện đến hết data-001”; làm DOC → ENV → INIT → DATA tuần tự, không triển khai CORE/ALG/UI.
- Commit: `e00fba79674ee892f8b8a3858febacc377b9de56` (INIT-001); metadata hậu commit được lưu bằng commit riêng trước task tiếp theo/handoff. Working tree sau commit triển khai sạch.
- Tệp hoặc artifact đã cập nhật: app.py, tests/test_environment.py, tests/test_app.py, tests/test_server.py, AGENTS.md, feature_list.json, progress.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi trong scope; thuật toán/metrics/UI demo chưa triển khai.
- Bước tốt nhất tiếp theo: Tiếp tục DATA-001: dữ liệu 20 điểm và preset có nguồn.

### Phiên 008

- Ngày: 09/11/2026 (Asia/Saigon); bắt đầu 2026-11-09T22:56:57+07:00.
- Mục tiêu: ENV-001 — Xác minh interpreter/dependencies/config local, ghi setup lặp lại được; không chạy thuật toán. Phạm vi: requirements.txt, requirements-dev.txt, pyproject.toml, .streamlit/config.toml, .gitignore, docs/ENVIRONMENT.md, feature_list.json, progress.md. Tiêu chí: giữ nguyên acceptance_criteria của task trong JSON.
- Đã hoàn thành: ENV-001: tái sử dụng Anaconda Python 3.13.9, import đúng pin runtime; cấu hình localhost và pytest hợp lệ; docs/ENVIRONMENT.md có setup lặp lại được.
- Xác minh đã chạy: 09/11/2026: python tmp/check_environment.py PASS exit 0: NumPy 2.3.5, SciPy 1.16.3, pandas 2.3.3, sklearn 1.7.2, Streamlit 1.51.0, Plotly 6.3.0, pytest 8.4.2; python -m pip check PASS exit 0; python -m pip install --dry-run -r requirements-dev.txt PASS exit 0 (already satisfied); python tmp/check_records.py và git diff --check PASS.
- Bằng chứng đã ghi lại: yêu cầu người dùng “Thực hiện đến hết data-001”; làm DOC → ENV → INIT → DATA tuần tự, không triển khai CORE/ALG/UI.
- Commit: `bc404c2ed255c082b4e2e06af3db62c6d30ae270` (ENV-001); metadata hậu commit được lưu bằng commit riêng trước task tiếp theo/handoff. Working tree sau commit triển khai sạch.
- Tệp hoặc artifact đã cập nhật: requirements.txt, requirements-dev.txt, pyproject.toml, .streamlit/config.toml, .gitignore, docs/ENVIRONMENT.md, feature_list.json, progress.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không kiểm chứng cài đặt venv mới; chưa có entry point/tests ở task ENV. Không có lỗi môi trường đang mở.
- Bước tốt nhất tiếp theo: Tiếp tục INIT-001: smoke test và entry point tối thiểu.

### Phiên 007

- Ngày: 09/11/2026 (Asia/Saigon); bắt đầu 2026-11-09T22:55:55+07:00.
- Mục tiêu: DOC-001 — Đóng hồ sơ, dọn cache bản nháp và Git checkpoint; bootstrap Git là prerequisite được mở bởi yêu cầu đến DATA-001. Phạm vi: AGENTS.md, docs/WORKFLOW.md, feature_list.json, progress.md, src/__pycache__. Tiêu chí: giữ nguyên acceptance_criteria của task trong JSON.
- Đã hoàn thành: Git baseline 4f7fd34 giữ nguyên file có sẵn; xác nhận src rỗng và xóa thư mục bằng lệnh không đệ quy; mở scope đến DATA-001, giữ nguyên lịch sử.
- Xác minh đã chạy: 09/11/2026: python tmp/check_records.py PASS; git diff --check PASS; Test-Path src = False sau cleanup. Lệnh xóa đệ quy bị automatic policy chặn; xóa rỗng không đệ quy thành công. Nghiệm thu hồ sơ, không phải thuật toán.
- Bằng chứng đã ghi lại: yêu cầu người dùng “Thực hiện đến hết data-001”; làm DOC → ENV → INIT → DATA tuần tự, không triển khai CORE/ALG/UI.
- Commit: `1dcb6fd266a5f0b4a9860988a2599425aa9f20d4` (DOC-001); metadata hậu commit được lưu bằng commit riêng trước task tiếp theo/handoff. Working tree sau commit triển khai sạch.
- Tệp hoặc artifact đã cập nhật: AGENTS.md, docs/WORKFLOW.md, feature_list.json, progress.md, src/__pycache__.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Không có lỗi trong scope; thuật toán/metrics/UI demo chưa triển khai.
- Bước tốt nhất tiếp theo: Tiếp tục ENV-001 theo yêu cầu đến DATA-001.

### Phiên 006

- Ngày: 09/11/2026 (Asia/Saigon).
- Mục tiêu: sửa progress theo đúng mẫu Nhật ký Phiên; chỉ nhật ký mới nhất lên đầu, feature list giữ thứ tự kế hoạch từ đầu.
- Đã hoàn thành: chuyển 5 mốc cũ thành Phiên 001–005 và giữ nội dung nguyên văn; chèn phiên này đầu; bổ sung sequence 0–28 cho feature theo đúng thứ tự đang có; sửa quy ước sai trong AGENTS và WORKFLOW. Đây là thay đổi nội dung, DOC-001 chưa DONE theo điều kiện commit/checkpoint.
- Xác minh đã chạy: `python tmp/check_session_format.py` PASS (exit 0): đúng 2 phần của mẫu, 5 trường trạng thái, 9 trường mỗi phiên; thứ tự Phiên 006–001; bảo toàn 5 khối lịch sử; giữ nguyên 29 ID/thứ tự/trạng thái feature, sequence 0–28, JSON/dependency/WID=1; AGENTS 87 < 100 dòng. Script kiểm tra tạm đã được dọn sau khi chạy.
- Bằng chứng đã ghi lại: 29 feature giữ nguyên ID/trạng thái; 5 khối nhật ký cũ được giữ nguyên văn dưới Bằng chứng của từng phiên; không ghi giả kết quả chạy ứng dụng hoặc commit.
- Commit: chưa có; thư mục chưa là Git repo theo lần kiểm tra gần nhất.
- Tệp hoặc artifact đã cập nhật: progress.md, feature_list.json, AGENTS.md, docs/WORKFLOW.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: DOC-001 vẫn COMMIT/blocked do thiếu Git/checkpoint; src/__pycache__ còn 5 file .pyc do lệnh dọn trước bị policy chặn. Chưa có src/*.py, app.py, tests/ hoặc README.
- Bước tốt nhất tiếp theo: bàn giao đúng hồ sơ này; chưa tự triển khai tính năng. Chỉ xử lý phần dọn còn thiếu và bootstrap Git khi phạm vi được giao cho cùng task.

### Phiên 005

- Ngày: 09/11/2026 (Asia/Saigon); mốc gốc: 2026-11-09T22:42:32+07:00.
- Mục tiêu: Sắp xếp mới nhất trước và reset mã nguồn theo yêu cầu.
- Đã hoàn thành: Xóa 5 file src/*.py, đưa 14 feature về planned, sửa UTF-8 và đảo nhật ký. Quy tắc đảo feature của phiên này được sửa ở Phiên 006.
- Xác minh đã chạy: Python kiểm tra hồ sơ/UTF-8/WID/dependency/reset: PASS; lệnh xóa thư mục/cache bị policy từ chối.
- Bằng chứng đã ghi lại: bảo toàn nội dung nhật ký gốc bên dưới; các trạng thái cũ chỉ mô tả thời điểm ghi.

  > - Người dùng giao cập nhật feature list/progress, đặt feature hoàn thành mới nhất trên đầu và xóa src để bắt đầu lại.
  > - Đã xóa 5 file mã nguồn .py trong src bằng apply_patch; chưa xóa hết thư mục vì còn __pycache__.
  > - Hai lệnh xóa qua PowerShell bị policy từ chối; không có lý do chi tiết. Không dùng đường vòng để xóa cache/thư mục.
  > - Đưa 14 feature có mã bị xóa về planned; giữ expected_files để biết nơi dự kiến triển khai lại. ENV-001 còn cấu hình nên vẫn implemented_unverified.
  > - Thêm completed_at (null cho task chưa DONE), quy tắc verified mới nhất trước và nhật ký mới nhất trước. Không tự tạo timestamp hoàn thành hoặc commit.
  > - Sửa các chuỗi metadata JSON bị lỗi mã hóa tiếng Việt từ lần cập nhật trước; dùng script UTF-8 để ghi đúng.
  > - Không chạy lại thuật toán, không tạo src mới, không mở task khác. Git/checkpoint còn thiếu; DOC-001 vẫn COMMIT/blocked.
  > - Kiểm tra qua stdin lần đầu gặp lỗi mã hóa ở chuỗi đối chiếu tiêu đề; lần chạy lại dùng Unicode escape đã PASS (exit 0), không sửa dữ liệu chuẩn để bỏ qua kiểm tra.
  > - Kiểm tra cuối PASS: JSON/UTF-8, thứ tự feature/nhật ký, WID=1, dependency, trạng thái reset, AGENTS 87 dòng; xác nhận chưa dọn hết cache. Không coi kiểm tra hồ sơ là kiểm thử phần mềm.

- Commit: chưa có; không suy ra commit từ việc kiểm tra tài liệu pass.
- Tệp hoặc artifact đã cập nhật: src/*.py đã xóa; AGENTS.md, docs/WORKFLOW.md, feature_list.json, progress.md cập nhật.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: src/__pycache__ còn 5 file .pyc; chưa có Git/checkpoint; không có phần mềm đã nghiệm thu.
- Bước tốt nhất tiếp theo: Sửa cách tổ chức nhật ký và giữ thứ tự feature theo làm rõ của người dùng.

### Phiên 004

- Ngày: 09/11/2026 (Asia/Saigon); mốc gốc: 09/11/2026.
- Mục tiêu: WID=1, gate INIT/EXE/COMMIT và Definition of Done.
- Đã hoàn thành: Thêm WID=1, INIT → EXE → COMMIT, phase INIT và Definition of Done.
- Xác minh đã chạy: Kiểm tra hồ sơ: PASS; git rev-parse/status/log: not a git repository.
- Bằng chứng đã ghi lại: bảo toàn nội dung nhật ký gốc bên dưới; các trạng thái cũ chỉ mô tả thời điểm ghi.

  > - Người dùng yêu cầu chỉ làm task được giao, chưa đóng việc trước không làm việc sau, có kiểm thử/commit/checkpoint để đổi phiên sạch.
  > - Đã cập nhật AGENTS còn 86 dòng; quy trình chi tiết tách sang `docs/WORKFLOW.md`.
  > - Thêm INIT độc lập trước execute: ENV-001 chỉ kiểm tra interpreter/dependencies/config; INIT-001 tạo smoke test và entry point tối thiểu khi được giao, chưa làm thuật toán.
  > - Gate DATA-001 và UI-001 được nối qua INIT-001; không dùng kiểm thử môi trường làm bằng chứng thuật toán đúng.
  > - Definition of Done: acceptance checks pass, review diff đúng scope, hồ sơ đồng bộ, Git commit/checkpoint có thật, working tree sạch trong scope; giữ thay đổi của người dùng.
  > - Kiểm tra `git rev-parse --is-inside-work-tree`, `git status --short`, `git log -1` đều thất bại: `not a git repository`. Không tự git init/commit hoặc cài môi trường trong task chỉnh hồ sơ này.
  > - DOC-001 được chuyển từ verified cũ sang blocked/passes=false vì tiêu chuẩn mới yêu cầu commit/checkpoint chưa có; evidence kiểm tra tài liệu trước đây vẫn được bảo toàn.
  > - Python qua stdin kiểm tra AGENTS < 100 dòng/đủ 5 mục, JSON, WID=1, trạng thái/commit, file references và dependency không chu trình: **PASS, exit 0**.
  > - Không sửa src, không chạy thêm thuật toán, không mở task mới. Chưa có Git commit; chưa DONE theo quy trình mới.

- Commit: chưa có; không suy ra commit từ việc kiểm tra tài liệu pass.
- Tệp hoặc artifact đã cập nhật: AGENTS.md, docs/WORKFLOW.md, feature_list.json, progress.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: DOC-001 chuyển blocked vì chưa có Git/checkpoint.
- Bước tốt nhất tiếp theo: Giữ cùng task; chỉ bootstrap Git khi phạm vi được giao.

### Phiên 003

- Ngày: 09/11/2026 (Asia/Saigon); mốc gốc: 09/11/2026.
- Mục tiêu: Tối ưu bàn giao giữa các session.
- Đã hoàn thành: Rút AGENTS còn 76 dòng tại thời điểm đó và thêm lệnh khởi động/kiểm tra.
- Xác minh đã chạy: python -m compileall -q src: PASS, exit 0 trước khi src bị xóa; kiểm tra AGENTS: PASS.
- Bằng chứng đã ghi lại: bảo toàn nội dung nhật ký gốc bên dưới; các trạng thái cũ chỉ mô tả thời điểm ghi.

  > - Viết lại `AGENTS.md` thành 76 dòng, trả lời trực tiếp: mục tiêu, cấu trúc, khởi động, kiểm tra và tiến độ.
  > - Bổ sung lệnh tạo venv/cài dependencies/chạy Streamlit, check nhanh cú pháp, chạy toàn bộ test hoặc một file test.
  > - Ghi rõ `app.py` và `tests/` chưa tồn tại; lệnh UI/pytest là hướng dẫn cho khi các entry point đó được tạo, không tuyên bố đã chạy.
  > - Thêm **Bàn giao nhanh** đầu file này và quy định cập nhật sau mỗi feature/session.
  > - Đã chạy `python -m compileall -q src`: **PASS, exit 0**. Kết quả chỉ xác nhận cú pháp, không xác nhận công thức hay kết quả tính toán.
  > - Đã kiểm tra số dòng AGENTS (76 < 100), đủ 5 mục và các lệnh chính: **PASS**.
  > - Không sửa hay tiếp tục triển khai tính năng trong `src/`; trạng thái feature phần mềm giữ nguyên.

- Commit: chưa có; không suy ra commit từ việc kiểm tra tài liệu pass.
- Tệp hoặc artifact đã cập nhật: AGENTS.md, feature_list.json, progress.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Compile chỉ kiểm tra cú pháp; chưa có ứng dụng hoặc tests.
- Bước tốt nhất tiếp theo: Chốt WID và điều kiện đóng task.

### Phiên 002

- Ngày: 09/11/2026 (Asia/Saigon); mốc gốc: 09/11/2026.
- Mục tiêu: Chuẩn hóa hồ sơ quản lý triển khai.
- Đã hoàn thành: Tạo AGENTS, feature list và progress theo hiện trạng thời điểm đó.
- Xác minh đã chạy: Python kiểm tra JSON, ID, phase/status, dependency và file references: PASS.
- Bằng chứng đã ghi lại: bảo toàn nội dung nhật ký gốc bên dưới; các trạng thái cũ chỉ mô tả thời điểm ghi.

  > - Tạo `AGENTS.md`: phạm vi, workflow, trạng thái, yêu cầu khoa học, bằng chứng nghiệm thu và cách bàn giao.
  > - Tạo `feature_list.json`: công việc nhỏ theo P0–P4, dependency, acceptance criteria, files, evidence và passes.
  > - Tạo file tiến độ này; đánh dấu mã đang có là `implemented_unverified`, UI/tests là `planned`, phần mở rộng là `deferred`.
  > - Đã chạy kiểm tra bằng Python qua stdin: JSON hợp lệ, ID duy nhất, phase/status hợp lệ, `passes` đồng nhất với trạng thái, đường dẫn file tồn tại, dependency không có chu trình và tài liệu không rỗng. Kết quả: **PASS**.
  > - Đã đối chiếu preference với các câu trả lời phỏng vấn. Chỉ `DOC-001` được đánh dấu `verified` cho bộ hồ sơ; không có feature phần mềm nào được đánh dấu pass.

- Commit: chưa có; không suy ra commit từ việc kiểm tra tài liệu pass.
- Tệp hoặc artifact đã cập nhật: AGENTS.md, feature_list.json, progress.md.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Kết quả pass tài liệu cũ không đáp ứng Definition of Done có commit được bổ sung ở Phiên 004.
- Bước tốt nhất tiếp theo: Làm rõ quy trình bắt đầu và bàn giao phiên.

### Phiên 001

- Ngày: 09/11/2026 (Asia/Saigon); mốc gốc: 09/11/2026.
- Mục tiêu: Khảo sát, phỏng vấn và khởi tạo mã.
- Đã hoàn thành: Khảo sát tài liệu, phỏng vấn và tạo các bản nháp ban đầu; trạng thái này là lịch sử, mã đã bị xóa ở Phiên 005.
- Xác minh đã chạy: Phép tính khảo sát độc lập và đọc phiên bản môi trường; chưa có tests cho mã src.
- Bằng chứng đã ghi lại: bảo toàn nội dung nhật ký gốc bên dưới; các trạng thái cũ chỉ mô tả thời điểm ghi.

  > - Hoàn thành khảo sát và ghi preference như trên.
  > - Đã viết các bản nháp mã và cấu hình; chưa kiểm chứng thực thi chúng.
  > - Người dùng yêu cầu dừng để viết `AGENTS.md`, feature list JSON và progress, đồng thời báo cáo những gì đã làm.

- Commit: chưa có; không suy ra commit từ việc kiểm tra tài liệu pass.
- Tệp hoặc artifact đã cập nhật: docs/KE_HOACH_TRIEN_KHAI.md, docs/DAC_TA_BAN_DAU.md; các file src/cấu hình tại thời điểm đó.
- Rủi ro đã biết hoặc vấn đề chưa được giải quyết: Mã nháp chưa kiểm chứng; sai khác số liệu eSFCM cần phân tích.
- Bước tốt nhất tiếp theo: Chốt hồ sơ trước khi tiếp tục implementation.
