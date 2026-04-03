const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  ImageRun,
  Header,
  Footer,
  AlignmentType,
  HeadingLevel,
  BorderStyle,
  WidthType,
  ShadingType,
  VerticalAlign,
  LevelFormat,
  PageNumber,
} = require("docx");
const fs = require("fs");

// 创建文档
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "微软雅黑", size: 24 },
      },
    },
    paragraphStyles: [
      {
        id: "Title",
        name: "Title",
        basedOn: "Normal",
        run: { size: 56, bold: true, color: "1F4E79", font: "微软雅黑" },
        paragraph: {
          spacing: { before: 400, after: 200 },
          alignment: AlignmentType.CENTER,
        },
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
        page: {
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      headers: {
        default: new Header({
          children: [
            new Paragraph({
              alignment: AlignmentType.RIGHT,
              children: [
                new TextRun({
                  text: "e交易专区收益成本统计报告",
                  size: 20,
                  color: "666666",
                }),
              ],
            }),
          ],
        }),
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [
                new TextRun({ text: "第 ", size: 20 }),
                new TextRun({ children: [PageNumber.CURRENT], size: 20 }),
                new TextRun({ text: " 页 / 共 ", size: 20 }),
                new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 20 }),
                new TextRun({ text: " 页", size: 20 }),
              ],
            }),
          ],
        }),
      },
      children: [
        // 标题
        new Paragraph({
          heading: HeadingLevel.TITLE,
          children: [new TextRun("e交易专区收益成本统计报告")],
        }),

        // 报告日期
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
          children: [
            new TextRun({
              text: "报告日期：2026年4月2日",
              size: 24,
              color: "666666",
            }),
          ],
        }),

        // 一、报告概述
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          children: [new TextRun("一、报告概述")],
        }),

        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun(
              "本报告基于e交易平台各专区的运营数据，从收益、成本、时间维度进行深度分析，旨在识别低效运营专区，为管理层决策提供数据支撑。通过对六大核心指标的统计分析，我们发现当前平台存在一定数量的低收益专区，需要引起重点关注并采取针对性措施。"
            ),
          ],
        }),

        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun(
              "数据统计范围涵盖中原、华北等区域共147个专区，重点分析确认接入时间、25年总收益、26年总收益、总成本等关键指标。通过建立风险分级体系（红色-重点关注、橙色-需改进、黄色-观察、灰色-流失风险），为后续运营策略制定提供清晰指引。"
            ),
          ],
        }),

        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun({
              text: "【重要说明】",
              bold: true,
              color: "C00000",
            }),
            new TextRun(
              " 本报告中的指标存在包含关系：指标三（总收益<5w）是指标一（总收益<10w）的子集，指标四（25年收益<5w）是指标二（25年收益<10w）的子集。为避免重复统计，后续分析采用去重后的数据。"
            ),
          ],
        }),

        // 二、核心数据概览
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          children: [new TextRun("二、核心数据概览")],
        }),

        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("2.1 六大指标统计（原始数据）")],
        }),

        // 原始指标表格
        createOriginalMetricsTable(),

        new Paragraph({
          spacing: { before: 200, after: 200 },
          children: [
            new TextRun(
              "从上表可以看出，指标之间存在明显的包含关系：指标三（56个）全部包含在指标一（66个）中，指标四（60个）全部包含在指标二（64个）中。这意味着如果简单相加会导致重复统计，需要进行去重处理。"
            ),
          ],
        }),

        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("2.2 去重后的风险等级分布")],
        }),

        // 去重后表格
        createDedupedMetricsTable(),

        new Paragraph({
          spacing: { before: 200, after: 200 },
          children: [
            new TextRun(
              "经过去重处理，实际需要关注的专区总数为83个。其中红色等级（重点关注）66个，占比最高；橙色等级（需改进）6个；灰色等级（流失风险）4个；黄色等级（观察）7个。这一分布特征表明，平台存在大量长期低收益专区，需要系统性整改。"
            ),
          ],
        }),

        // 插入图表1
        new Paragraph({
          spacing: { before: 300, after: 100 },
          alignment: AlignmentType.CENTER,
          children: [
            new ImageRun({
              type: "png",
              data: fs.readFileSync(
                "D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\temp\\chart1_risk_distribution.png"
              ),
              transformation: { width: 500, height: 400 },
              altText: {
                title: "风险等级分布",
                description: "风险等级分布饼图",
                name: "风险等级分布",
              },
            }),
          ],
        }),

        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 300 },
          children: [
            new TextRun({
              text: "图1：e交易专区风险等级分布（去重后）",
              size: 20,
              italics: true,
            }),
          ],
        }),

        // 三、收益分析
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          children: [new TextRun("三、收益分析")],
        }),

        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("3.1 收益区间分布")],
        }),

        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun(
              "针对需要关注的专区，我们进一步分析其收益分布情况。从数据来看，收益分布呈现明显的两极分化特征：大部分专区集中在低收益区间，而收益接近10万元门槛的专区数量相对较少。这一分布特征表明，当前低收益专区普遍存在运营效率不高的问题，需要系统性分析原因并制定提升策略。"
            ),
          ],
        }),

        // 插入图表2
        new Paragraph({
          spacing: { before: 200, after: 100 },
          alignment: AlignmentType.CENTER,
          children: [
            new ImageRun({
              type: "png",
              data: fs.readFileSync(
                "D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\temp\\chart2_revenue_distribution.png"
              ),
              transformation: { width: 500, height: 300 },
              altText: {
                title: "收益分布",
                description: "25年收益分布柱状图",
                name: "收益分布",
              },
            }),
          ],
        }),

        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 300 },
          children: [
