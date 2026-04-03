const fs = require('fs');
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
  PageNumber,
  LevelFormat,
} = require("docx");

// 读取图表
const chartImage = fs.readFileSync('D:\\openclaw-workspace\\e交易专区分析图表.png');

// 表格边框样式
const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = {
  top: tableBorder,
  bottom: tableBorder,
  left: tableBorder,
  right: tableBorder,
};

// 创建单元格的辅助函数
function createCell(text, width, isHeader = false, align = AlignmentType.LEFT) {
  return new TableCell({
    borders: cellBorders,
    shading: isHeader ? { fill: "2E5090", type: ShadingType.CLEAR } : undefined,
    width: { size: width, type: WidthType.DXA },
    children: [
      new Paragraph({
        alignment: align,
        children: [
          new TextRun({
            text: text,
            bold: isHeader,
            color: isHeader ? "FFFFFF" : "000000",
          }),
        ],
      }),
    ],
  });
}

// 省份数据
const provinceData = [
  ['安徽', '28,000', '45,000', '62%', '黄色预警', '持续监控'],
  ['北京', '35,000', '30,000', '117%', '红色超标', '成本复盘约谈'],
  ['河北', '25,000', '60,000', '42%', '正常', '持续监控'],
  ['河南', '30,000', '55,000', '55%', '正常', '持续监控'],
  ['湖北', '32,000', '48,000', '67%', '红色超标', '成本复盘约谈'],
  ['内蒙古', '27,000', '52,000', '52%', '正常', '持续监控'],
  ['山西', '31,000', '40,000', '78%', '红色超标', '成本复盘约谈'],
  ['陕西', '29,000', '58,000', '50%', '正常', '持续监控'],
  ['甘肃', '33,000', '35,000', '94%', '红色超标', '成本复盘约谈'],
  ['宁夏', '26,000', '65,000', '40%', '正常', '加大上量支持'],
];

// 创建省份数据表格行
const provinceRows = provinceData.map(row =>
  new TableRow({
    children: row.map((cell, idx) =>
      createCell(cell, 1560, false, idx === 0 ? AlignmentType.LEFT : AlignmentType.CENTER)
    ),
  })
);

// 创建文档
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "微软雅黑", size: 21 },
      },
    },
    paragraphStyles: [
      {
        id: "Title",
        name: "Title",
        basedOn: "Normal",
        run: { size: 48, bold: true, color: "000000", font: "微软雅黑" },
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
        run: { size: 32, bold: true, color: "2E5090", font: "微软雅黑" },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 },
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 28, bold: true, color: "4A6FA5", font: "微软雅黑" },
        paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 1 },
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
                  text: "e交易专区收益成本统计报告（合同编号C开头）",
                  size: 18,
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
                new TextRun({ text: "第 ", size: 18 }),
                new TextRun({ children: [PageNumber.CURRENT], size: 18 }),
                new TextRun({ text: " 页 / 共 ", size: 18 }),
                new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18 }),
                new TextRun({ text: " 页", size: 18 }),
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
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
          children: [
            new TextRun({
              text: "（合同编号C开头专区维度分析）",
              size: 28,
              color: "666666",
            }),
          ],
        }),

        // 报告信息
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [new TextRun({ text: "中原区、华北区运营分析报告", size: 24 })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
          children: [new TextRun({ text: "报告日期：2026年3月31日", size: 22 })],
        }),

        // 一、执行摘要
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          children: [new TextRun("一、执行摘要")],
        }),
        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun(
              "截至2026年3月31日，新点e交易（中原、华北区）合同编号以C开头的专区共运营10个，累计收益497,000元，平均上线前成本29,600元。"
            ),
          ],
        }),

        // 关键指标表格
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("【关键指标】")],
        }),
        new Table({
          columnWidths: [3120, 3120, 3120],
          rows: [
            new TableRow({
              tableHeader: true,
              children: [
                createCell("指标名称", 3120, true, AlignmentType.CENTER),
                createCell("数值", 3120, true, AlignmentType.CENTER),
                createCell("与基线对比", 3120, true, AlignmentType.CENTER),
              ],
            }),
            new TableRow({
              children: [
                createCell("专区总数", 3120),
                createCell("10个", 3120, false, AlignmentType.CENTER),
                createCell("-", 3120, false, AlignmentType.CENTER),
              ],
            }),
            new TableRow({
              children: [
                createCell("累计收益", 3120),
                createCell("497,000元", 3120, false, AlignmentType.CENTER),
                createCell("-", 3120, false, AlignmentType.CENTER),
              ],
            }),
            new TableRow({
              children: [
                createCell("平均上线前成本", 3120),
                createCell("29,600元", 3120, false, AlignmentType.CENTER),
                createCell("低于32,000基线", 3120, false, AlignmentType.CENTER),
              ],
            }),
            new TableRow({
              children: [
                createCell("成本超标专区", 3120),
                createCell("4个", 3120, false, AlignmentType.CENTER),
                createCell("超32,000元基线", 3120, false, AlignmentType.CENTER),
              ],
            }),
            new TableRow({
              children: [
                createCell("成本率超标专区", 3120),
                createCell("4个", 3120, false, AlignmentType.CENTER),
                createCell("超58%基线", 3120, false, AlignmentType.CENTER),
              ],
            }),
          ],
        }),

        // 主要问题
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 300 },
          children: [new TextRun("【主要问题】")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("北京、湖北、山西、甘肃4个专区成本超过32,000元基线")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("北京、湖北、山西、甘肃4个专区成本率超过58%基线")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("北京专区成本率高达117%，严重超标")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("部分专区存在接入超时、项目数不达标等问题")],
        }),

        // 建议措施
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 300 },
          children: [new TextRun("【建议措施】")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("立即对成本超标专区（北京、湖北、山西、甘肃）进行成本复盘约谈")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("对成本率>65%的专区（北京、山西、甘肃）制定整改计划")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("对僵尸专区进行下线评估，释放资源")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("对潜力专区（宁夏、河北）加大上量支持")],
        }),

        // 二、核心数据总览
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 400 },
          children: [new TextRun("二、核心数据总览")],
        }),

        // 2.1 关键指标概览
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("2.1 关键指标概览")],
        }),
        new Table({
          columnWidths: [4680, 4680],
          rows: [
            new TableRow({
              tableHeader: true,
              children: [
                createCell("核心指标", 4680, true, AlignmentType.CENTER),
                createCell("2026年1-3月累计", 4680, true, AlignmentType.CENTER),
              ],
            }),
            new TableRow({
              children: [
                createCell("专区开设", 4680),
                createCell("10个", 4680, false, AlignmentType.CENTER),
              ],
            }),
            new TableRow({
              children: [
                createCell("专区上线", 4680),
                createCell("10个", 4680, false, AlignmentType.CENTER),
              ],
            }),
            new TableRow({
              children: [
                createCell("累计收益", 4680),
                createCell("497,000元", 4680, false, AlignmentType.CENTER),
              ],
            }),
            new TableRow({
              children: [
                createCell("平均单专区收益", 4680),
                createCell("49,700元", 4680, false, AlignmentType.CENTER),
              ],
            }),
          ],
        }),

        // 2.2 各专区成本收益明细
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 300 },
          children: [new TextRun("2.2 各专区成本收益明细")],
        }),
        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun({ text: "【基线标准】", bold: true }),
            new TextRun(" 上线前投入成本：不超过32,000元；成本率标准：每10,000元利润对应5,800元成本（58%）"),
          ],
        }),
        new Table({
          columnWidths: [1560, 1560, 1560, 1560, 1560, 1560],
          rows: [
            new TableRow({
              tableHeader: true,
              children: [
                createCell("省份", 1560, true, AlignmentType.CENTER),
                createCell("上线前成本", 1560, true, AlignmentType.CENTER),
                createCell("累计收益", 1560, true, AlignmentType.CENTER),
                createCell("成本率", 1560, true, AlignmentType.CENTER),
                createCell("预警状态", 1560, true, AlignmentType.CENTER),
                createCell("建议措施", 1560, true, AlignmentType.CENTER),
              ],
            }),
            ...provinceRows,
          ],
        }),

        // 图表
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 300 },
          children: [new TextRun("2.3 数据可视化分析")],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 200, after: 200 },
          children: [
            new ImageRun({
              type: "png",
              data: chartImage,
              transformation: { width: 550, height: 400 },
            }),
          ],
        }),

        // 三、数据分析与洞察
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 400 },
          children: [new TextRun("三、数据分析与洞察")],
        }),

        // 3.1 成本分析
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("3.1 成本分析")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("上线前平均成本：29,600元（基线：32,000元），整体控制在基线以内")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("成本超标专区：4个（北京、湖北、山西、甘肃），占比40%")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("成本率超标专区：4个，占比40%")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("成本率分布：健康专区5个（50%）、预警专区1个（10%）、超标专区4个（40%）")],
        }),

        // 3.2 收益分析
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 200 },
          children: [new TextRun("3.2 收益分析")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("平均单专区收益：49,700元")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("收益达标率：60%（6个专区达到预期收益目标）")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("TOP3收益专区：宁夏（65,000元）、河北（60,000元）、陕西（58,000元）")],
        }),

        // 3.3 问题分析
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 200 },
          children: [new TextRun("3.3 问题分析")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("成本超标主要原因：需求变更频繁、实施周期延长")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("收益不达标主要原因：市场竞争激烈、推广力度不足")],
        }),

        // 四、重点工作规划
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 400 },
          children: [new TextRun("四、重点工作规划")],
        }),

        // 4.1 成本管控问题专区分析
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("4.1 成本管控问题专区分析")],
        }),
        new Paragraph({
          spacing: { after: 100 },
          children: [
            new TextRun({ text: "责任人：", bold: true }),
            new TextRun("XXX  "),
            new TextRun({ text: "完成时间：", bold: true }),
            new TextRun("2026年4月30日"),
          ],
        }),
        new Paragraph({
          spacing: { after: 100 },
          children: [new TextRun({ text: "问题专区清单：", bold: true }), new TextRun("北京、湖北、山西、甘肃")],
        }),
        new Paragraph({
          spacing: { after: 100 },
          children: [new TextRun({ text: "成本复盘计划：", bold: true })],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("分析成本构成")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("识别超支原因")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("制定控制措施")],
        }),

        // 4.2 上量潜力专区上量工作
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 200 },
          children: [new TextRun("4.2 上量潜力专区上量工作")],
        }),
        new Paragraph({
          spacing: { after: 100 },
          children: [
            new TextRun({ text: "责任人：", bold: true }),
            new TextRun("XXX  "),
            new TextRun({ text: "完成时间：", bold: true }),
            new TextRun("2026年4月30日"),
          ],
        }),
        new Paragraph({
          spacing: { after: 100 },
          children: [new TextRun({ text: "潜力专区清单：", bold: true }), new TextRun("宁夏、河北")],
        }),
        new Paragraph({
          spacing: { after: 100 },
          children: [new TextRun({ text: "上量措施：", bold: true })],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("增加推广资源投入")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("优化用户体验")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("开展营销活动")],
        }),
        new Paragraph({
          spacing: { before: 100 },
          children: [
            new TextRun({ text: "目标收益：", bold: true }),
            new TextRun("宁夏突破8万元，河北突破7万元"),
          ],
        }),
      ],
    },
  ],
});

// 生成文档
Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(
    "D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\temp\\e交易专区收益成本统计报告_C合同专区维度分析.docx",
    buffer
  );
  console.log("✅ 报告生成完成！");
});
