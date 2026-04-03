const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, Header, Footer, AlignmentType, HeadingLevel,
  BorderStyle, WidthType, ShadingType, PageNumber, LevelFormat,
} = require("docx");

const chartImage = fs.readFileSync('D:\\openclaw-workspace\\e交易专区分析图表_110个专区.png');

const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

function createCell(text, width, isHeader = false, align = AlignmentType.LEFT, fontSize = 18) {
  return new TableCell({
    borders: cellBorders,
    shading: isHeader ? { fill: "2E5090", type: ShadingType.CLEAR } : undefined,
    width: { size: width, type: WidthType.DXA },
    children: [new Paragraph({ alignment: align, children: [new TextRun({ text: text, bold: isHeader, color: isHeader ? "FFFFFF" : "000000", size: fontSize })] })],
  });
}

const provinceData = [
  ['湖北', '21', '1,351,108', '284,150', '21.0%', '正常'],
  ['新疆', '15', '1,300,710', '285,636', '22.0%', '正常'],
  ['河南', '28', '975,792', '279,808', '28.7%', '正常'],
  ['山东', '20', '226,145', '150,528', '66.6%', '黄色预警'],
  ['内蒙古', '13', '116,240', '209,040', '179.8%', '红色超标'],
  ['辽宁', '6', '87,410', '115,007', '131.6%', '红色超标'],
  ['河北', '4', '36,042', '125,127', '347.2%', '红色超标'],
  ['天津', '1', '29,500', '7,264', '24.6%', '正常'],
  ['北京', '1', '20,585', '1,996', '9.7%', '正常'],
  ['吉林', '1', '1,700', '29,944', '1761.4%', '红色超标'],
];

const topRevenueData = [
  ['1', '昌吉城建市政招采平台', '新疆', '24,709', '767,865', '3.2%'],
  ['2', '湖北专区', '湖北', '40,041', '443,270', '9.0%'],
  ['3', '荆门城控专区', '湖北', '15,875', '281,650', '5.6%'],
  ['4', '中元专区', '湖北', '7,702', '217,515', '3.5%'],
  ['5', '正兴数字化交易服务平台', '新疆', '12,651', '215,390', '5.9%'],
  ['6', '恒信专区', '河南', '7,415', '206,410', '3.6%'],
  ['7', '济源专区', '河南', '23,793', '125,715', '18.9%'],
  ['8', '汉江集团专区', '湖北', '16,264', '110,270', '14.7%'],
  ['9', '正济专区', '河南', '1,793', '105,220', '1.7%'],
  ['10', '德e采专区', '山东', '20,266', '103,718', '19.5%'],
];

const provinceRows = provinceData.map(row => new TableRow({
  children: row.map((cell, idx) => createCell(cell, 1560, false, idx === 0 ? AlignmentType.LEFT : AlignmentType.CENTER, 16))
}));

const topRevenueRows = topRevenueData.map(row => new TableRow({
  children: row.map((cell, idx) => createCell(cell, 1560, false, idx === 0 ? AlignmentType.CENTER : AlignmentType.LEFT, 16))
}));

const doc = new Document({
  styles: {
    default: { document: { run: { font: "微软雅黑", size: 21 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", run: { size: 48, bold: true, color: "000000", font: "微软雅黑" }, paragraph: { spacing: { before: 240, after: 240 }, alignment: AlignmentType.CENTER } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 32, bold: true, color: "2E5090", font: "微软雅黑" }, paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 28, bold: true, color: "4A6FA5", font: "微软雅黑" }, paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: "bullet-list", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "e交易专区收益成本统计报告（C合同-110个专区）", size: 18, color: "666666" })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "第 ", size: 18 }), new TextRun({ children: [PageNumber.CURRENT], size: 18 }), new TextRun({ text: " 页 / 共 ", size: 18 }), new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18 }), new TextRun({ text: " 页", size: 18 })] })] }) },
    children: [
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("e交易专区收益成本统计报告")] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 }, children: [new TextRun({ text: "（合同编号C开头 - 110个专区维度分析）", size: 28, color: "666666" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: "中原区、华北区运营分析报告", size: 24 })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 }, children: [new TextRun({ text: "报告日期：2026年3月31日", size: 22 })] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("一、执行摘要")] }),
      new Paragraph({ spacing: { after: 200 }, children: [new TextRun("截至2026年3月31日，新点e交易（中原、华北区）合同编号以C开头的专区共运营110个，覆盖10个省份，累计收益4,145,231.71元，累计成本1,488,500.37元，平均单专区收益37,683.92元。")] }),
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("【关键指标】")] }),
      new Table({
        columnWidths: [3120, 3120, 3120],
        rows: [
          new TableRow({ tableHeader: true, children: [createCell("指标名称", 3120, true, AlignmentType.CENTER), createCell("数值", 3120, true, AlignmentType.CENTER), createCell("说明", 3120, true, AlignmentType.CENTER)] }),
          new TableRow({ children: [createCell("专区总数", 3120), createCell("110个", 3120, false, AlignmentType.CENTER), createCell("合同编号C开头", 3120, false, AlignmentType.CENTER)] }),
          new TableRow({ children: [createCell("覆盖省份", 3120), createCell("10个", 3120, false, AlignmentType.CENTER), createCell("湖北、新疆、河南等", 3120, false, AlignmentType.CENTER)] }),
          new TableRow({ children: [createCell("累计收益", 3120), createCell("4,145,231.71元", 3120, false, AlignmentType.CENTER), createCell("-", 3120, false, AlignmentType.CENTER)] }),
          new TableRow({ children: [createCell("累计成本", 3120), createCell("1,488,500.37元", 3120, false, AlignmentType.CENTER), createCell("-", 3120, false, AlignmentType.CENTER)] }),
          new TableRow({ children: [createCell("平均单专区收益", 3120), createCell("37,683.92元", 3120, false, AlignmentType.CENTER), createCell("-", 3120, false, AlignmentType.CENTER)] }),
          new TableRow({ children: [createCell("成本超标专区", 3120), createCell("10个", 3120, false, AlignmentType.CENTER), createCell("总成本>32,000元", 3120, false, AlignmentType.CENTER)] }),
        ],
      }),
      new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 300 }, children: [new TextRun("【主要问题】")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("河北、内蒙古、辽宁、吉林等省份成本率严重超标（>100%）")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("10个专区总成本超过32,000元基线")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("部分专区零收益，成本无法回收")] }),
      new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 300 }, children: [new TextRun("【建议措施】")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("对成本率超标省份（河北、内蒙古、辽宁、吉林）进行成本复盘")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("对零收益专区进行下线评估")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("对高收益专区（湖北、新疆）加大上量支持")] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 400 }, children: [new TextRun("二、核心数据总览")] }),
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2.1 各省份专区分布")] }),
      new Table({ columnWidths: [1560, 1560, 1560, 1560, 1560, 1560], rows: [