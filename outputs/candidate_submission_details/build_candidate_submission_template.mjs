import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = path.dirname(fileURLToPath(import.meta.url));
const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Candidate Details");

sheet.showGridLines = false;
sheet.freezePanes.freezeRows(4);

sheet.getRange("A1:B1").merge();
sheet.getRange("A1").values = [["Candidate Submission Details"]];
sheet.getRange("A2:B2").merge();
sheet.getRange("A2").values = [["Fill the Details column when candidate information is available."]];

const rows = [
  ["Full Name", ""],
  ["Current Organization", ""],
  ["Total Years of Experience", ""],
  ["Relevant Experience", ""],
  ["Current Location", ""],
  ["Willing to Relocate", ""],
  ["Notice Period", ""],
  ["Last Working Day", ""],
  ["Current CTC", ""],
  ["Expected CTC", ""],
  ["Date of Birth", ""],
  ["Mobile Number", ""],
  ["Alternate Contact Number", ""],
  ["E-mail", ""],
  ["LinkedIn", ""],
  ["Higher Qualification", ""],
  ["Previously Worked / Resume Submitted / Attend Interview With Mindteck, Yes / No", ""],
];

sheet.getRange("A4:B4").values = [["Field", "Details"]];
sheet.getRange(`A5:B${rows.length + 4}`).values = rows;

sheet.getRange("A1:B1").format = {
  fill: "#17324D",
  font: { bold: true, color: "#FFFFFF", size: 16 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
sheet.getRange("A1:B1").format.rowHeightPx = 36;

sheet.getRange("A2:B2").format = {
  fill: "#EAF2F8",
  font: { italic: true, color: "#36536B" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
sheet.getRange("A2:B2").format.rowHeightPx = 24;

sheet.getRange("A4:B4").format = {
  fill: "#2F855A",
  font: { bold: true, color: "#FFFFFF" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  borders: { preset: "all", style: "thin", color: "#B7C8B9" },
};

const tableRange = sheet.getRange(`A4:B${rows.length + 4}`);
tableRange.format.borders = { preset: "all", style: "thin", color: "#D9E2E7" };
tableRange.format.verticalAlignment = "center";
tableRange.format.wrapText = true;

sheet.getRange(`A5:A${rows.length + 4}`).format = {
  fill: "#F6F8FA",
  font: { bold: true, color: "#243B53" },
  horizontalAlignment: "left",
  verticalAlignment: "center",
  wrapText: true,
};
sheet.getRange(`B5:B${rows.length + 4}`).format = {
  fill: "#FFFFFF",
  font: { color: "#111827" },
  horizontalAlignment: "left",
  verticalAlignment: "center",
  wrapText: true,
};

sheet.getRange("A1:A21").format.columnWidthPx = 360;
sheet.getRange("B1:B21").format.columnWidthPx = 360;
sheet.getRange(`A5:B${rows.length + 4}`).format.rowHeightPx = 28;
sheet.getRange("A21:B21").format.rowHeightPx = 44;

sheet.getRange("B10").dataValidation = {
  rule: { type: "list", values: ["Yes", "No"] },
};
sheet.getRange("B21").dataValidation = {
  rule: { type: "list", values: ["Yes", "No"] },
};

sheet.getRange("B12").format.numberFormat = "yyyy-mm-dd";
sheet.getRange("B15").format.numberFormat = "yyyy-mm-dd";
sheet.getRange("B16:B19").format.numberFormat = "@";
sheet.getRange("B7:B8").format.numberFormat = "0.0";
sheet.getRange("B13:B14").format.numberFormat = "#,##0.00";

const table = sheet.tables.add(`A4:B${rows.length + 4}`, true, "CandidateSubmissionDetails");
table.style = "TableStyleMedium4";
table.showFilterButton = false;

const inspect = await workbook.inspect({
  kind: "table",
  range: `Candidate Details!A1:B${rows.length + 4}`,
  include: "values,formulas",
  tableMaxRows: 25,
  tableMaxCols: 2,
});
console.log(inspect.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

const preview = await workbook.render({
  sheetName: "Candidate Details",
  autoCrop: "all",
  scale: 1,
  format: "png",
});
await fs.writeFile(path.join(outputDir, "candidate_submission_details_preview.png"), new Uint8Array(await preview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(path.join(outputDir, "candidate_submission_details_final.xlsx"));
