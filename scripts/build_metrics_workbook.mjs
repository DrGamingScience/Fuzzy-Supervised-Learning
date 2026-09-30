import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const workspaceRoot = path.resolve(scriptDir, "..");
const outputPath = path.join(workspaceRoot, "docs", "research", "clustering-validity-metrics-2010.xlsx");
const previewPath = path.join(workspaceRoot, "artifacts", "spreadsheets", "clustering-validity-metrics-2010.png");

const rows = [
  [1, "Optimization-like", "Calinski-Harabasz / VRC", 1, "Không", "So sánh độ phân tán giữa cụm với độ phân tán trong cụm.", "tr(B)/tr(W) × (N-k)/(k-1)", "[0, +∞)", "Cao hơn", "O(dN); cần 2 ≤ k < N.", "Có"],
  [2, "Optimization-like", "Davies-Bouldin", 1, "Không", "Trung bình trường hợp xấu nhất của tỷ lệ độ phân tán trong cụm trên độ tách giữa hai cụm.", "DB = (1/k) Σ max[(d_l+d_m)/d_lm]", "[0, +∞)", "Thấp hơn", "O(d(N+k²)).", "Không"],
  [3, "Optimization-like", "Dunn family", 18, "Không", "So sánh khoảng cách nhỏ nhất giữa các cụm với đường kính lớn nhất của một cụm.", "min δ(C_p,C_q) / max Δ(C_l)", "[0, +∞)", "Cao hơn", "18 cách kết hợp; thường O(dN²).", "Không"],
  [4, "Optimization-like", "SWC / SSWC", 2, "Không", "Đo độ chặt và độ tách của từng điểm. SSWC thay khoảng cách trung bình tới các điểm bằng khoảng cách tới tâm cụm.", "s(i)=(b(i)-a(i))/max(a(i),b(i)); lấy trung bình trên N điểm", "[-1, 1]", "Cao hơn", "SWC: O(dN²); SSWC: O(dkN).", "Có"],
  [5, "Optimization-like", "ASWC / ASSWC", 2, "Không", "Các biến thể silhouette dùng tỷ số phi tuyến; ASSWC sử dụng khoảng cách tới tâm cụm.", "s(i)=b(i)/(a(i)+ε); lấy trung bình", "[0, +∞)", "Cao hơn", "ASWC: O(dN²); ASSWC: O(dkN).", "Không"],
  [6, "Optimization-like", "PBM", 1, "Không", "Kết hợp độ phân tán toàn cục, độ phân tán trong cụm và khoảng cách lớn nhất giữa các tâm.", "[(E₁/E_K) × (D_K/k)]²", "[0, +∞)", "Cao hơn", "O(d(N+k²)).", "Không"],
  [7, "Optimization-like", "C-index", 1, "Không", "Chuẩn hóa tổng khoảng cách nội cụm theo các biên tốt nhất và xấu nhất có thể.", "(θ-θ_min)/(θ_max-θ_min)", "[0, 1]", "Thấp hơn", "O(N²(d+log N)).", "Không"],
  [8, "Optimization-like", "Gamma", 1, "Không", "So sánh số cặp khoảng cách đồng thuận và bất đồng giữa quan hệ cụm và khoảng cách.", "(S⁺-S⁻)/(S⁺+S⁻)", "[-1, 1]", "Cao hơn", "Chi phí rất lớn; có thành phần bậc bốn.", "Không"],
  [9, "Optimization-like", "G(+)", 1, "Không", "Đo tỷ lệ các cặp khoảng cách bất đồng với cấu trúc phân cụm.", "Chuẩn hóa số cặp bất đồng S⁻", "[0, 1]", "Thấp hơn", "Chi phí rất lớn; có thành phần bậc bốn.", "Không"],
  [10, "Optimization-like", "Tau", 1, "Không", "Chuẩn hóa chênh lệch giữa số cặp đồng thuận và bất đồng.", "Chuẩn hóa S⁺-S⁻ theo tổng số so sánh", "[-1, 1]", "Cao hơn", "Chi phí rất lớn; có thành phần bậc bốn.", "Không"],
  [11, "Optimization-like", "Point-biserial", 1, "Không", "Tương quan giữa khoảng cách cặp điểm và biến chỉ báo cùng hoặc khác cụm.", "Tương quan point-biserial", "Thường [-1, 1]", "Cao hơn", "O(dN²).", "Không"],
  [12, "Optimization-like", "C/√k", 1, "Không", "Kết hợp tỷ lệ phương sai theo từng thuộc tính và số cụm.", "C chia cho √k", "[0, 1] khi hợp lệ", "Cao hơn", "O(dN).", "Không"],
  [13, "Difference-like", "trace(W)", 1, "Không", "Tổng độ phân tán bên trong các cụm.", "trace(W)", "Phụ thuộc dữ liệu", "Tìm elbow", "Dùng chuỗi kết quả tại k-1, k và k+1.", "Không"],
  [14, "Difference-like", "trace(CovW)", 1, "Không", "Vết của ma trận hiệp phương sai gộp trong cụm.", "trace(CovW)", "Phụ thuộc dữ liệu", "Tìm elbow", "Dùng biến đổi Eq. (37) để tìm đỉnh.", "Không"],
  [15, "Difference-like", "trace(W⁻¹B)", 1, "Không", "So sánh phân tán giữa cụm với phân tán trong cụm qua ma trận nghịch đảo.", "trace(W⁻¹B)", "Phụ thuộc dữ liệu", "Tìm elbow", "Có rủi ro suy biến khi W không khả nghịch.", "Không"],
  [16, "Difference-like", "|T| / |W|", 1, "Không", "Tỷ số định thức của phân tán tổng thể và phân tán trong cụm.", "det(T)/det(W)", "Phụ thuộc dữ liệu", "Tìm elbow", "Có rủi ro định thức bằng 0 hoặc kém điều kiện.", "Không"],
  [17, "Difference-like", "N log(|T|/|W|)", 1, "Không", "Biến đổi log của tỷ số định thức, có nhân theo số mẫu.", "N × log(det(T)/det(W))", "Phụ thuộc dữ liệu", "Tìm elbow", "Cần kiểm tra định thức và ổn định số.", "Không"],
  [18, "Difference-like", "k²|W|", 1, "Không", "Điều chỉnh định thức phân tán trong cụm theo bình phương số cụm.", "k² × det(W)", "Phụ thuộc dữ liệu", "Tìm elbow", "Có rủi ro suy biến của W.", "Không"],
  [19, "Difference-like", "log(SSB/SSW)", 1, "Không", "Log tỷ lệ tổng bình phương giữa cụm và trong cụm.", "log(SSB/SSW)", "Phụ thuộc dữ liệu", "Tìm elbow", "Cần SSW > 0.", "Không"],
  [20, "Difference-like", "Ball-Hall", 1, "Không", "Trung bình độ phân tán trong cụm, có điều chỉnh theo số cụm.", "Tiêu chuẩn Ball-Hall", "Phụ thuộc dữ liệu", "Tìm elbow", "Đánh giá trên chuỗi số cụm.", "Không"],
  [21, "Difference-like", "McClain-Rao", 1, "Không", "So sánh khoảng cách trung bình trong cụm với khoảng cách trung bình giữa cụm.", "Khoảng cách nội cụm / khoảng cách liên cụm", "[0, +∞)", "Tìm elbow", "Đánh giá trên chuỗi số cụm.", "Không"],
  [22, "External", "Rand Index", 1, "Có", "Mức đồng thuận của mọi cặp điểm giữa nhãn thật và phân cụm.", "RI=(a+d)/(a+b+c+d)", "[0, 1]", "Cao hơn", "Không hiệu chỉnh đồng thuận ngẫu nhiên.", "Không"],
  [23, "External", "Adjusted Rand Index (ARI)", 1, "Có", "Mức đồng thuận theo cặp đã hiệu chỉnh phần đồng thuận kỳ vọng do ngẫu nhiên.", "[a-(a+b)(a+c)/M] / [((a+b)+(a+c))/2-(a+b)(a+c)/M]", "Có thể âm; 1 là hoàn hảo", "Cao hơn", "Kỳ vọng gần 0 đối với phân hoạch ngẫu nhiên.", "Có"],
  [24, "External", "Jaccard", 1, "Có", "Tỷ lệ các cặp được ghép cùng đúng trên tổng số cặp ghép cùng hoặc đáng lẽ phải ghép cùng.", "J=a/(a+b+c)", "[0, 1]", "Cao hơn", "Không dùng số cặp khác lớp và khác cụm d.", "Có"],
];

const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Metrics");
sheet.showGridLines = false;
sheet.tabColor = "#1F4E78";

sheet.getRange("A2").values = [["Các metrics trong bài Relative Clustering Validity Criteria (2010)"]];
sheet.getRange("A3").values = [["Nguồn: Vendramin, Campello và Hruschka (2010), Statistical Analysis and Data Mining 3, 209-235."]];
sheet.getRange("A4").values = [["Dòng chữ đậm và nền xanh nhạt là bốn metric/nhóm metric đề xuất dùng cho dự án."]];

const headers = [["STT", "Nhóm trong bài", "Metric / tiêu chuẩn", "Số tiêu chuẩn", "Cần nhãn thật", "Mô tả", "Công thức / logic", "Miền giá trị", "Chiều tốt", "Độ phức tạp / lưu ý", "Đề xuất dùng"]];
sheet.getRange("A6:K6").values = headers;
sheet.getRange(`A7:K${6 + rows.length}`).values = rows;

const fontName = "Arial";
const fullRange = sheet.getRange(`A2:K${6 + rows.length}`);
fullRange.format.font = { name: fontName, size: 10, color: "#1F2937" };
fullRange.format.verticalAlignment = "center";

sheet.getRange("A2:K2").format.font = { name: fontName, size: 14, bold: true, color: "#17365D" };
sheet.getRange("A3:K3").format.font = { name: fontName, size: 9, italic: true, color: "#5B6573" };
sheet.getRange("A4:K4").format.font = { name: fontName, size: 9, italic: true, color: "#355E3B" };

sheet.getRange("A6:K6").format = {
  fill: "#1F4E78",
  font: { name: fontName, size: 10, bold: true, color: "#FFFFFF" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  wrapText: true,
  borders: {
    bottom: { style: "medium", color: "#17365D" },
  },
};

const dataRange = sheet.getRange(`A7:K${6 + rows.length}`);
dataRange.format.wrapText = true;
dataRange.format.borders = {
  insideHorizontal: { style: "thin", color: "#D9E2F3" },
  bottom: { style: "thin", color: "#AAB7C4" },
};

sheet.getRange(`A7:E${6 + rows.length}`).format.horizontalAlignment = "center";
sheet.getRange(`H7:I${6 + rows.length}`).format.horizontalAlignment = "center";
sheet.getRange(`K7:K${6 + rows.length}`).format.horizontalAlignment = "center";
sheet.getRange(`F7:G${6 + rows.length}`).format.verticalAlignment = "top";
sheet.getRange(`J7:J${6 + rows.length}`).format.verticalAlignment = "top";

// Phân biệt nhóm mà không dùng màu làm nguồn thông tin duy nhất.
sheet.getRange("A19:K27").format.fill = "#F7F8FA";
sheet.getRange("A28:K30").format.fill = "#EEF4FB";

// Bốn metric/nhóm metric được đề xuất dùng: VRC, SWC/SSWC, ARI và Jaccard.
for (const excelRow of [7, 10, 29, 30]) {
  const rowRange = sheet.getRange(`A${excelRow}:K${excelRow}`);
  rowRange.format.fill = "#E2F0D9";
  rowRange.format.font = { name: fontName, size: 10, bold: true, color: "#1F2937" };
  sheet.getRange(`K${excelRow}`).format.fill = "#C6E0B4";
}

const widths = {
  A: 48,
  B: 112,
  C: 185,
  D: 82,
  E: 86,
  F: 290,
  G: 285,
  H: 115,
  I: 100,
  J: 210,
  K: 96,
};
for (const [col, widthPx] of Object.entries(widths)) {
  sheet.getRange(`${col}:${col}`).format.columnWidthPx = widthPx;
}

sheet.getRange("2:2").format.rowHeightPx = 24;
sheet.getRange("3:4").format.rowHeightPx = 20;
sheet.getRange("6:6").format.rowHeightPx = 34;
sheet.getRange(`7:${6 + rows.length}`).format.autofitRows();
sheet.getRange(`7:${6 + rows.length}`).format.rowHeightPx = 56;
sheet.freezePanes.freezeRows(6);
sheet.freezePanes.freezeColumns(3);

workbook.recalculate();

const inspection = await workbook.inspect({
  kind: "table",
  range: "Metrics!A2:K30",
  include: "values,formulas",
  tableMaxRows: 35,
  tableMaxCols: 11,
  tableMaxCellChars: 120,
  maxChars: 18000,
});
console.log(inspection.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

const preview = await workbook.render({
  sheetName: "Metrics",
  range: "A1:K30",
  scale: 1,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));

await fs.mkdir("D:/Fuzzy-Supervised-Learning/docs", { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(JSON.stringify({ outputPath, previewPath, rowCount: rows.length }));
