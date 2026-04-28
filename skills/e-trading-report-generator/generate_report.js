#!/usr/bin/env node

/**
 * e交易专区收益成本统计报告生成器
 * 根据专区数据Excel文件自动生成Word统计报告
 */

const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  AlignmentType,
  HeadingLevel,
  BorderStyle,
  WidthType,
  ShadingType,
  VerticalAlign,
  LevelFormat,
} = require("docx");
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

// 获取命令行参数
const args = process.argv.slice(2);
const dataFilePath = args[0];
const outputPath = args[1];

if (!dataFilePath) {
  console.error("用法: node generate_report.js <数据文件路径> [输出文件路径]");
  console.error("示例: node generate_report.js D:/data/专区数据.xlsx D:/output/报告.docx");
  process.exit(1);
}

if (!fs.existsSync(dataFilePath)) {
  console.error(`错误: 数据文件不存在: ${dataFilePath}`);
  process.exit(1);
}

// 读取Excel数据并统计
function analyzeData(filePath) {
  const pythonScript = `
import pandas as pd
import sys
import json

df = pd.read_excel(r'${filePath.replace(/\\/g, '\\\\')}')

# 转换日期列
df['确认接入时间'] = pd.to_datetime(df['确认接入时间'], errors='coerce')

# 统计指标
stats = {
    'total': len(df),
    'indicator1': len(df[(df['确认接入时间'] < '2025-04-08') & (df['总收益情况'] == 0)]),
    'indicator2': len(df[(df['确认接入时间'] < '2025-04-08') & (df['总收益情况'] > 0) & (df['总收益情况'] < 100000)]),
    'indicator3': len(df[(df['确认接入时间'] < '2025-04-08') & (df['总收益情况'] > 0) & (df['总收益情况'] < 50000)]),
    'indicator4': len(df[(df['确认接入时间'] < '2025-01-01') & (df['25年收益情况'] > 0) & (df['25年收益情况'] < 100000)]),
    'indicator5': len(df[(df['确认接入时间'] < '2025-01-01') & (df['25年收益情况'] > 0) & (df['25年收益情况'] < 50000)]),
    'indicator6': len(df[df['26年收益情况'] > 0]),
    'indicator7': len(df[(df['25年收益情况'] > 0) & (df['26年收益情况'] == 0)]),
}

print(json.dumps(stats, ensure_ascii=False))
`;

  const tempPyFile = path.join(__dirname, '_temp_analyze.py');
  fs.writeFileSync(tempPyFile, pythonScript);
  
  try {
    const result = execSync(`python "${tempPyFile}"`, { encoding: 'utf-8' });
    fs.unlinkSync(tempPyFile);
    return JSON.parse(result.trim());
  } catch (error) {
    console.error("数据分析失败:", error.message);
    if (fs.existsSync(tempPyFile)) fs.unlinkSync(tempPyFile);
    process.exit(1);
  }
}

// 表格边框样式
const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "000000" };
const cellBorders = {
  top: tableBorder,
  bottom: tableBorder,
  left: tableBorder,
  right: tableBorder,
};

// 创建单元格的辅助函数
function createCell(text, options = {}) {
  const {
    bold = false,
    shading = null,
    width = 1500,
    alignment = AlignmentType.CENTER,
  } = options;

  return new TableCell({
    borders: cellBorders,
    width: { size: width, type: WidthType.DXA },
    shading: shading ? { fill: shading, type: ShadingType.CLEAR } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    children: [
      new Paragraph({
        alignment: alignment,
        children: [new TextRun({ text: String(text), bold: bold, size: 21 })],
      }),
    ],
  });
}

// 创建文档
function createDocument(stats) {
  return new Document({
    styles: {
      default: {
        document: {
          run: { font: "宋体", size: 24 },
        },
      },
      paragraphStyles: [
        {
          id: "Title",
          name: "Title",
          basedOn: "Normal",
          run: { size: 44, bold: true, color: "000000", font: "黑体" },
          paragraph: {
            spacing: { before: 240, after: 240 },
            alignment: AlignmentType.CENTER,
          },
        },
        {
          id: "Heading1",
          name: "Heading 1",
          basedOn: "Normal",
          next: "Normal",
          quickFormat: true,
          run: { size: 32, bold: true, color: "000000", font: "黑体" },
          paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 },
        },
        {
          id: "Heading2",
          name: "Heading 2",
          basedOn: "Normal",
          next: "Normal",
          quickFormat: true,
          run: { size: 28, bold: true, color: "000000", font: "黑体" },
          paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 1 },
        },
      ],
    },
    numbering: {
      config: [
        {
          reference: "bullet-list",
          levels: [
            {
              level: 0,
              format: LevelFormat.BULLET,
              text: "•",
              alignment: AlignmentType.LEFT,
              style: { paragraph: { indent: { left: 720, hanging: 360 } } },
            },
          ],
        },
      ],
    },
    sections: [
      {
        properties: {
          page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } },
        },
        children: [
          // 标题
          new Paragraph({
            heading: HeadingLevel.TITLE,
            children: [new TextRun("新点e交易专区（中原/华北）收益成本")],
          }),

          // 概述段落
          new Paragraph({
            spacing: { before: 200, after: 200 },
            children: [
              new TextRun({
                text: "近期基于新点e交易平台各专区的运营数据，从收益、成本、时间维度进行深度分析。通过部分指标的统计分析，我们发现当前平台存在一定数量的零收益、低收益专区，需要引起重点关注并采取针对性措施。",
                size: 24,
              }),
            ],
          }),

          new Paragraph({
            spacing: { before: 200, after: 200 },
            children: [
              new TextRun({
                text: `数据统计范围涵盖中原、华北等区域共${stats.total}个专区，重点分析确认接入时间、25年总收益、26年总收益、总成本等关键指标。通过建立风险分级体系（红色-重点关注、橙色-需改进、黄色-观察、灰色-流失风险）。`,
                size: 24,
              }),
            ],
          }),

          new Paragraph({
            spacing: { before: 200, after: 200 },
            children: [
              new TextRun({
                text: `本次统计识别出一批需重点关注的低收益专区，其中纳入红色等级预警的有 ${stats.indicator1 + stats.indicator2} 个、橙色等级预警的有 ${stats.indicator4} 个（两类等级存在部分专区重叠），另有灰色等级 ${stats.indicator7} 个。从数据趋势来看，部分早期接入的专区已出现运营效率低下、客户活跃度下降等问题。`,
                size: 24,
              }),
            ],
          }),

          new Paragraph({
            spacing: { before: 200, after: 200 },
            children: [
              new TextRun({
                text: "对于长期无收益且无可挽救价值的专区，建议果断下线以节约运营成本；对于有潜力的专区，加大资源投入和运营支持。",
                size: 24,
              }),
            ],
          }),

          // 一、核心数据概览
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("一、核心数据概览")],
          }),

          // 1.1 六大指标统计
          new Paragraph({
            heading: HeadingLevel.HEADING_2,
            children: [new TextRun("1.1 六大指标统计")],
          }),

          new Paragraph({
            spacing: { before: 200, after: 200 },
            children: [
              new TextRun({
                text: `从上表可以看出，接入超1年，但长期零收益专区为0的有${stats.indicator1}个，长期低收益专区（总收益10w以下）共计${stats.indicator2}个，占比较高，因收益10w以下的专区过多，故进一步分析收益5w以下的专区，数量为${stats.indicator3}个；25年前接入但收益不达标的专区（25年总收益在10w以下）共计${stats.indicator4}个，其中25年总收益在5w以下的有${stats.indicator5}个，反映出早期接入专区的运营效率问题；特别值得关注的是，有${stats.indicator7}个专区在25年产生收益但26年暂无收益，存在客户流失风险。`,
                size: 24,
              }),
            ],
          }),

          // 指标统计表格
          new Table({
            columnWidths: [1500, 3500, 1200, 1500, 2000],
            rows: [
              new TableRow({
                tableHeader: true,
                children: [
                  createCell("指标", { bold: true, shading: "D5E8F0", width: 1500 }),
                  createCell("条件", { bold: true, shading: "D5E8F0", width: 3500 }),
                  createCell("数量", { bold: true, shading: "D5E8F0", width: 1200 }),
                  createCell("风险等级", { bold: true, shading: "D5E8F0", width: 1500 }),
                  createCell("备注", { bold: true, shading: "D5E8F0", width: 2000 }),
                ],
              }),
              new TableRow({
                children: [
                  createCell("指标一", { width: 1500 }),
                  createCell("接入超过1年，总收益为0", { width: 3500, alignment: AlignmentType.LEFT }),
                  createCell(stats.indicator1, { width: 1200 }),
                  createCell("红色", { width: 1500 }),
                  createCell("重点关注", { width: 2000 }),
                ],
              }),
              new TableRow({
                children: [
                  createCell("指标二", { width: 1500 }),
                  createCell("接入超过1年，0<总收益<10w", { width: 3500, alignment: AlignmentType.LEFT }),
                  createCell(stats.indicator2, { width: 1200 }),
                  createCell("红色", { width: 1500 }),
                  createCell("重点关注", { width: 2000 }),
                ],
              }),
              new TableRow({
                children: [
                  createCell("指标三", { width: 1500 }),
                  createCell("接入超过1年，0<总收益<5w", { width: 3500, alignment: AlignmentType.LEFT }),
                  createCell(stats.indicator3, { width: 1200 }),
                  createCell("红色", { width: 1500 }),
                  createCell("重点关注", { width: 2000 }),
                ],
              }),
              new TableRow({
                children: [
                  createCell("指标四", { width: 1500 }),
                  createCell("25年前接入，0<25年收益<10w", { width: 3500, alignment: AlignmentType.LEFT }),
                  createCell(stats.indicator4, { width: 1200 }),
                  createCell("橙色", { width: 1500 }),
                  createCell("需改进", { width: 2000 }),
                ],
              }),
              new TableRow({
                children: [
                  createCell("指标五", { width: 1500 }),
                  createCell("25年前接入，0<25年收益<5w", { width: 3500, alignment: AlignmentType.LEFT }),
                  createCell(stats.indicator5, { width: 1200 }),
                  createCell("橙色", { width: 1500 }),
                  createCell("需改进", { width: 2000 }),
                ],
              }),
              new TableRow({
                children: [
                  createCell("指标六", { width: 1500 }),
                  createCell("26年产生收益", { width: 3500, alignment: AlignmentType.LEFT }),
                  createCell(stats.indicator6, { width: 1200 }),
                  createCell("黄色", { width: 1500 }),
                  createCell("观察", { width: 2000 }),
                ],
              }),
              new TableRow({
                children: [
                  createCell("指标七", { width: 1500 }),
                  createCell("25年有收益，26年无", { width: 3500, alignment: AlignmentType.LEFT }),
                  createCell(stats.indicator7, { width: 1200 }),
                  createCell("灰色", { width: 1500 }),
                  createCell("流失风险", { width: 2000 }),
                ],
              }),
            ],
          }),

          // 1.2 风险等级分布
          new Paragraph({
            heading: HeadingLevel.HEADING_2,
            children: [new TextRun("1.2 风险等级分布")],
          }),

          new Paragraph({
            spacing: { before: 200, after: 100 },
            children: [
              new TextRun({
                text: "根据收益水平、接入时长、趋势变化等维度，我们将专区划分为四个风险等级：",
                size: 24,
              }),
            ],
          }),

          // 红色等级
          new Paragraph({
            spacing: { before: 200, after: 100 },
            children: [
              new TextRun({ text: "【红色-重点关注】", bold: true, size: 24, color: "FF0000" }),
            ],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [
              new TextRun({ text: "处理对象：", bold: true, size: 24 }),
              new TextRun({ text: "接入超过一年，但长期零收益或者低收益专区", size: 24 }),
            ],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [new TextRun({ text: "处理措施：", bold: true, size: 24 })],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "逐一排查专区运营状态，确认是否仍在正常服务客户", size: 24 }),
            ],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "对于长期无交易的专区，评估是否继续投入运营成本", size: 24 }),
            ],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "制定专区下线计划，释放运维资源", size: 24 }),
            ],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "对于仍有潜力的专区，制定专项提升计划，明确责任人和时间节点", size: 24 }),
            ],
          }),

          // 橙色等级
          new Paragraph({
            spacing: { before: 200, after: 100 },
            children: [
              new TextRun({ text: "【橙色-需改进】", bold: true, size: 24, color: "FF8C00" }),
            ],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [
              new TextRun({ text: "处理对象：", bold: true, size: 24 }),
              new TextRun({ text: "25年前接入，25年存在收益但小于10w", size: 24 }),
            ],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [new TextRun({ text: "处理措施：", bold: true, size: 24 })],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "分析专区情况，找出收益低的原因，是否客户业务量上限，是否存在上量可能", size: 24 }),
            ],
          }),

          // 黄色等级
          new Paragraph({
            spacing: { before: 200, after: 100 },
            children: [
              new TextRun({ text: "【黄色-观察】", bold: true, size: 24, color: "FFD700" }),
            ],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [
              new TextRun({ text: "26年产生收益的专区，运营状态良好，继续保持观察。", size: 24 }),
            ],
          }),

          // 灰色等级
          new Paragraph({
            spacing: { before: 200, after: 100 },
            children: [
              new TextRun({ text: "【灰色-流失风险】", bold: true, size: 24, color: "808080" }),
            ],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [
              new TextRun({ text: "处理对象：", bold: true, size: 24 }),
              new TextRun({ text: "25年有收益但26年无收益专区", size: 24 }),
            ],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [new TextRun({ text: "处理措施：", bold: true, size: 24 })],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "优先安排人员对该部分专区进行情况了解", size: 24 }),
            ],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "了解客户流失原因", size: 24 }),
            ],
          }),

          // 图1占位符
          new Paragraph({
            spacing: { before: 300, after: 300 },
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "【图1：e交易专区风险等级分布】", italics: true, size: 22, color: "666666" })],
          }),

          // 二、收益分析
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("二、收益分析")],
          }),

          // 2.1 25年收益分布
          new Paragraph({
            heading: HeadingLevel.HEADING_2,
            children: [new TextRun("2.1 25年收益分布")],
          }),

          new Paragraph({
            spacing: { before: 200, after: 200 },
            children: [
              new TextRun({
                text: "针对25年前接入的低收益专区，我们进一步分析其25年总收益分布情况。从数据来看，收益分布呈现明显的两极分化特征：大部分专区集中在0-3万元区间，而收益在7-10万元区间的专区数量相对较少。这一分布特征表明，当前低收益专区普遍存在运营效率不高的问题，需要系统性分析原因并制定提升策略。",
                size: 24,
              }),
            ],
          }),

          // 图2占位符
          new Paragraph({
            spacing: { before: 300, after: 300 },
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "【图2：25年前接入专区收益分布（25年总收益<10万）】", italics: true, size: 22, color: "666666" })],
          }),

          // 2.2 流失风险专区TOP10
          new Paragraph({
            heading: HeadingLevel.HEADING_2,
            children: [new TextRun("2.2 流失风险专区TOP10")],
          }),

          new Paragraph({
            spacing: { before: 200, after: 200 },
            children: [
              new TextRun({
                text: "以下10个专区在2025年产生较高收益，但2026年至今暂无收益记录，存在较高的客户流失或业务停滞风险，建议优先安排客户经理进行回访和原因排查。",
                size: 24,
              }),
            ],
          }),

          // 图3占位符
          new Paragraph({
            spacing: { before: 300, after: 300 },
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "【图3：TOP10 流失风险专区（25年有收益但26年无）】", italics: true, size: 22, color: "666666" })],
          }),

          // 三、后续处理建议
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("三、后续处理建议")],
          }),

          new Paragraph({
            spacing: { before: 200, after: 200 },
            children: [
              new TextRun({
                text: "基于以上数据分析，针对不同类型的低收益专区，我们提出以下分类处理建议：",
                size: 24,
              }),
            ],
          }),

          // 3.1 红色等级专区
          new Paragraph({
            heading: HeadingLevel.HEADING_2,
            children: [new TextRun("3.1 红色等级专区（立即处理）")],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [
              new TextRun({ text: "处理对象：", bold: true, size: 24 }),
              new TextRun({ text: "接入超过一年，但长期零收益或者低收益专区", size: 24 }),
            ],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [new TextRun({ text: "处理措施：", bold: true, size: 24 })],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "逐一排查专区运营状态，确认是否仍在正常服务客户", size: 24 }),
            ],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "对于长期无交易的专区，评估是否继续投入运营成本", size: 24 }),
            ],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "制定专区下线计划，释放运维资源", size: 24 }),
            ],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "对于仍有潜力的专区，制定专项提升计划，明确责任人和时间节点", size: 24 }),
            ],
          }),

          // 3.2 灰色等级专区
          new Paragraph({
            heading: HeadingLevel.HEADING_2,
            children: [new TextRun("3.2 灰色等级专区（紧急跟进）")],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [
              new TextRun({ text: "处理对象：", bold: true, size: 24 }),
              new TextRun({ text: "25年有收益但26年无收益专区", size: 24 }),
            ],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [new TextRun({ text: "处理措施：", bold: true, size: 24 })],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "优先安排人员对该部分专区进行情况了解", size: 24 }),
            ],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "了解客户流失原因", size: 24 }),
            ],
          }),

          // 3.3 橙色等级专区
          new Paragraph({
            heading: HeadingLevel.HEADING_2,
            children: [new TextRun("3.3 橙色等级专区（持续优化）")],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [
              new TextRun({ text: "处理对象：", bold: true, size: 24 }),
              new TextRun({ text: "25年前接入，25年存在收益但小于10w", size: 24 }),
            ],
          }),

          new Paragraph({
            spacing: { before: 100, after: 100 },
            indent: { left: 360 },
            children: [new TextRun({ text: "处理措施：", bold: true, size: 24 })],
          }),

          new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [
              new TextRun({ text: "分析专区情况，找出收益低的原因，是否客户业务量上限，是否存在上量可能", size: 24 }),
            ],
          }),

          // 四、关键任务
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("四、关键任务")],
          }),

          // 关键任务表格
          new Table({
            columnWidths: [800, 4500, 1500, 2000, 1200],
            rows: [
              new TableRow({
                tableHeader: true,
                children: [
                  createCell("序号", { bold: true, shading: "D5E8F0", width: 800 }),
                  createCell("实施工作", { bold: true, shading: "D5E8F0", width: 4500 }),
                  createCell("负责人", { bold: true, shading: "D5E8F0", width: 1500 }),
                  createCell("计划完成节点", { bold: true, shading: "D5E8F0", width: 2000 }),
                  createCell("备注", { bold: true, shading: "D5E8F0", width: 1200 }),
                ],
              }),
              new TableRow({
                children: [
                  createCell("1", { width: 800 }),
                  createCell("对25年有收益但26年未产生收益的大企业侧专区进行摸排", { width: 4500, alignment: AlignmentType.LEFT }),
                  createCell("陈海勇/钟明珠", { width: 1500 }),
                  createCell("2026年4月17日", { width: 2000 }),
                  createCell("", { width: 1200 }),
                ],
              }),
              new TableRow({
                children: [
                  createCell("2", { width: 800 }),
                  createCell("对于接入超一年的低收益的大企业侧专区逐一排查，看是否存在上量可能", { width: 4500, alignment: AlignmentType.LEFT }),
                  createCell("陈海勇/钟明珠", { width: 1500 }),
                  createCell("2026年4月30日", { width: 2000 }),
                  createCell("", { width: 1200 }),
                ],
              }),
              new TableRow({
                children: [
                  createCell("3", { width: 800 }),
                  createCell("对接入超一年的零收益专区摸排，看是否存在上量可能，确认是否需要执行下线操作", { width: 4500, alignment: AlignmentType.LEFT }),
                  createCell("陈海勇/钟明珠", { width: 1500 }),
                  createCell("2026年5月31日", { width: 2000 }),
                  createCell("", { width: 1200 }),
                ],
              }),
              new TableRow({
                children: [
                  createCell("4", { width: 800 }),
                  createCell("对于26年产生收益专区持续关注", { width: 4500, alignment: AlignmentType.LEFT }),
                  createCell("陈海勇/钟明珠", { width: 1500 }),
                  createCell("2026年5月31日", { width: 2000 }),
                  createCell("", { width: 1200 }),
                ],
              }),
            ],
          }),

          // 附录
          new Paragraph({
            spacing: { before: 400, after: 200 },
            children: [
              new TextRun({ text: "【附录】", bold: true, size: 24 }),
            ],
          }),

          new Paragraph({
            spacing: { before: 200, after: 200 },
            children: [
              new TextRun({ text: "详细数据请参见附件《中原华北区专区数据_成本更新.xlsx》", size: 24 }),
            ],
          }),
        ],
      },
    ],
  });
}

// 主程序
console.log("正在分析数据...");
const stats = analyzeData(dataFilePath);
console.log("数据统计结果:");
console.log(`  - 总专区数: ${stats.total}`);
console.log(`  - 红色预警: ${stats.indicator1 + stats.indicator2}个`);
console.log(`  - 橙色预警: ${stats.indicator4}个`);
console.log(`  - 灰色风险: ${stats.indicator7}个`);

console.log("\n正在生成报告...");
const doc = createDocument(stats);

// 确定输出路径
const finalOutputPath = outputPath || path.join(
  path.dirname(dataFilePath),
  "e交易专区收益成本统计报告_生成.docx"
);

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(finalOutputPath, buffer);
  console.log(`\n报告已生成: ${finalOutputPath}`);
}).catch(err => {
  console.error("生成报告失败:", err);
  process.exit(1);
});
