const fs = require('fs');
const docx = require('docx');

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, Header, Footer, AlignmentType, HeadingLevel,
  BorderStyle, WidthType, ShadingType, VerticalAlign,
  LevelFormat, PageNumber
} = docx;

// 创建原始指标表格
function createOriginalTable() {
  const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
  const cellBorders = { top: border, bottom: border, left: border, right: border };
  
  return new Table({
    columnWidths: [1500, 4500, 1200, 1500, 1660],
    rows: [
      new TableRow({
        tableHeader: true,
        children: [
          createCell("指标", 1500, "1F4E79", true),
          createCell("条件", 4500, "1F4E79", true),
          createCell("数量", 1200, "1F4E79", true),
          createCell("包含关系", 1500, "1F4E79", true),
          createCell("备注", 1660, "1F4E79", true),
        ],
      }),
      createDataRow("指标一", "超1年且总收益<10w", "66", "包含指标三", "", cellBorders),
      createDataRow("指标二", "25年前且25年收益<10w", "64", "包含指标四", "", cellBorders),
      createDataRow("指标三", "超1年且总收益<5w", "56", "属于指标一", "子集", cellBorders),
      createDataRow("指标四", "25年前且25年收益<5w", "60", "属于指标二", "子集", cellBorders),
      createDataRow("指标五", "26年产生收益", "33", "-", "", cellBorders),
      createDataRow("指标六", "25年有收益但26年无", "20", "-", "", cellBorders),
    ],
  });
}

// 创建去重后表格
function createDedupedTable() {
  const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
  const cellBorders = { top: border, bottom: border, left: border, right: border };
  
  return new Table({
    columnWidths: [1800, 4200, 1200, 2200],
    rows: [
      new TableRow({
        tableHeader: true,
        children: [
          createCell("风险等级", 1800, "1F4E79", true),
          createCell("条件", 4200, "1F4E79", true),
          createCell("数量", 1200, "1F4E79", true),
          createCell("说明", 2200, "1F4E79", true),
        ],
      }),
      createDedupedRow("红色-重点关注", "超1年且总收益<10w", "66", "指标一全部", "C00000", cellBorders),
      createDedupedRow("橙色-需改进", "25年前且25年收益<10w（排除红色）", "6", "指标二独有", "ED7D31", cellBorders),
      createDedupedRow("灰色-流失风险", "25年有但26年无（排除红橙）", "4", "指标六排除重叠", "7F7F7F", cellBorders),
      createDedupedRow("黄色-观察", "26年有收益（排除红橙灰）", "7", "指标五排除重叠", "FFC000", cellBorders),
      createDedupedRow("合计", "不重复专区总数", "83", "去重后总数", "000000", cellBorders, true),
    ],
  });
}

function createCell(text, width, fillColor, isHeader) {
  return new TableCell({
    borders: {
      top: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
      bottom: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
      left: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
      right: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
    },
    width: { size: width, type: WidthType.DXA },
    shading: fillColor ? { fill: fillColor, type: ShadingType.CLEAR } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({
            text: text,
            bold: isHeader,
            color: isHeader ? "FFFFFF" : "000000",
            size: 22,
          }),
        ],
      }),
    ],
  });
}

function createDataRow(index, condition, count, relation, remark, cellBorders) {
  return new TableRow({
    children: [
      new TableCell({
        borders: cellBorders,
        width: { size: 1500, type: WidthType.DXA },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: index, size: 22 })] })],
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: 4500, type: WidthType.DXA },
        children: [new Paragraph({ children: [new TextRun({ text: condition, size: 22 })] })],
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: 1200, type: WidthType.DXA },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: count, size: 22, bold: true })] })],
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: 1500, type: WidthType.DXA },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: relation, size: 22 })] })],
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: 1660, type: WidthType.DXA },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: remark, size: 22 })] })],
      }),
    ],
  });
}

function createDedupedRow(level, condition, count, desc, color, cellBorders, isTotal) {
  return new TableRow({
    children: [
      new TableCell({
        borders: cellBorders,
        width: { size: 1800, type: WidthType.DXA },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: level, size: 22, bold: true, color: isTotal ? "000000" : color })] })],
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: 4200, type: WidthType.DXA },
        children: [new Paragraph({ children: [new TextRun({ text: condition, size: 22 })] })],
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: 1200, type: WidthType.DXA },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: count, size: 22, bold: true })] })],
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: 2200, type: WidthType.DXA },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: desc, size: 22 })] })],
      }),
    ],
  });
}

// 主文档内容
const doc = new Document({
  styles: {
    default: { document: { run: { font: "微软雅黑", size: 24 } } },
    paragraphStyles: [
      {
        id: "Title",
        name: "Title",
        basedOn: "Normal",
        run: { size: 56, bold: true, color: "1F4E79", font: "微软雅黑" },
        paragraph: { spacing: { before: 400, after: 200 }, alignment: AlignmentType.CENTER },
      },
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 36, bold: true, color: "1F4E79", font: "微软雅黑" },
        paragraph: { spacing: { before: 400, after: 200 }, outlineLevel: 0 },
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 28, bold: true, color: "2E75B6", font: "微软雅黑" },
        paragraph: { spacing: { before: 300, after: 150 }, outlineLevel: 1 },
      },
    ],
  },
  numbering: {
    config: [{
      reference: "bullet-list",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
    }],
  },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    headers: {
      default: new Header({
        children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "e交易专区收益成本统计报告", size: 20, color: "666666" })] })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "第 ", size: 20 }),
            new TextRun({ children: [PageNumber.CURRENT], size: 20 }),
            new TextRun({ text: " 页 / 共 ", size: 20 }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 20