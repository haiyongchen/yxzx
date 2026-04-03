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

        // 二、核心数据概览
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          children: [new TextRun("二、核心数据概览")],
        }),

        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("2.1 六大指标统计")],
        }),

        // 指标表格
        createMetricsTable(),

        new Paragraph({
          spacing: { before: 200, after: 200 },
          children: [
            new TextRun(
              "从上表可以看出，平台存在124个专区需要不同程度的关注。其中，长期低收益专区（指标一+指标三）共计124个，占比较高；25年前接入但收益不达标的专区（指标二+指标四）共计124个，反映出早期接入专区的运营效率问题；特别值得关注的是，有20个专区在25年产生收益但26年暂无收益，存在客户流失风险。"
            ),
          ],
        }),

        // 2.2 风险等级分布
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("2.2 风险等级分布")],
        }),

        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun(
              "根据收益水平、接入时长、趋势变化等维度，我们将专区划分为四个风险等级："
            ),
          ],
        }),

        // 风险等级说明
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun({
              text: "【🔴 红色-重点关注】",
              bold: true,
              color: "C00000",
            }),
            new TextRun(
              " 长期低收益专区，接入超过1年但总收益低于10万或5万，需立即制定提升方案或考虑下线。"
            ),
          ],
        }),

        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun({
              text: "【🟠 橙色-需改进】",
              bold: true,
              color: "ED7D31",
            }),
            new TextRun(
              " 25年前接入但25年收益不达标的专区，需分析原因并优化运营策略。"
            ),
          ],
        }),

        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun({
              text: "【🟡 黄色-观察】",
              bold: true,
              color: "FFC000",
            }),
            new TextRun(" 26年产生收益的专区，运营状态良好，继续保持观察。"),
          ],
        }),

        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun({
              text: "【⚪ 灰色-流失风险】",
              bold: true,
              color: "7F7F7F",
            }),
            new TextRun(
              " 25年有收益但26年暂无收益的专区，存在客户流失或业务停滞风险，需紧急跟进。"
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
              text: "图1：e交易专区风险等级分布",
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
          children: [new TextRun("3.1 25年收益分布")],
        }),

        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun(
              "针对25年前接入的64个低收益专区，我们进一步分析其25年总收益分布情况。从数据来看，收益分布呈现明显的两极分化特征：大部分专区集中在0-3万元区间，而收益在7-10万元区间的专区数量相对较少。这一分布特征表明，当前低收益专区普遍存在运营效率不高的问题，需要系统性分析原因并制定提升策略。"
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
            new TextRun({
              text: "图2：25年前接入专区收益分布（25年总收益<10万）",
              size: 20,
              italics: true,
            }),
          ],
        }),

        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("3.2 流失风险专区TOP10")],
        }),

        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun(
              "以下10个专区在2025年产生较高收益，但2026年至今暂无收益记录，存在较高的客户流失或业务停滞风险，建议优先安排客户经理进行回访和原因排查。"
            ),
          ],
        }),

        // 插入图表3
        new Paragraph({
          spacing: { before: 200, after: 100 },
          alignment: AlignmentType.CENTER,
          children: [
            new ImageRun({
              type: "png",
              data: fs.readFileSync(
                "D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\temp\\chart3_top10_risk.png"
              ),
              transformation: { width: 550, height: 350 },
              altText: {
                title: "TOP10风险专区",
                description: "流失风险专区TOP10",
                name: "TOP10风险专区",
              },
            }),
          ],
        }),

        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 300 },
          children: [
            new TextRun({
              text: "图3：TOP10 流失风险专区（25年有收益但26年无）",
              size: 20,
              italics: true,
            }),
          ],
        }),

        // 四、后续处理建议
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          children: [new TextRun("四、后续处理建议")],
        }),

        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun(
              "基于以上数据分析，针对不同类型的低收益专区，我们提出以下分类处理建议："
            ),
          ],
        }),

        // 建议1
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("4.1 红色等级专区（立即处理）")],
        }),

        new Paragraph({
          spacing: { after: 150 },
          children: [
            new TextRun({
              text: "处理对象：",
              bold: true,
            }),
            new TextRun(
              "指标一（67个）+ 指标三（57个）= 124个长期低收益专区"
            ),
          ],
        }),

        new Paragraph({
          spacing: { after: 150 },
          children: [
            new TextRun({
              text: "处理措施：",
              bold: true,
            }),
          ],
        }),

        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun(
              "逐一排查专区运营状态，确认是否仍在正常服务客户"
            ),
          ],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun(
              "对于长期无交易的专区，评估是否继续投入运营成本"
            ),
          ],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun(
              "制定专区下线或合并方案，释放服务器和运维资源"
            ),
          ],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun(
              "对于仍有潜力的专区，制定专项提升计划，明确责任人和时间节点"
            ),
          ],
        }),

        // 建议2
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("4.2 灰色等级专区（紧急跟进）")],
        }),

        new Paragraph({
          spacing: { after: 150 },
          children: [
            new TextRun({
              text: "处理对象：",
              bold: true,
            }),
            new TextRun("指标六（20个）25年有收益但26年无收益专区"),
          ],
        }),

        new Paragraph({
          spacing: { after: 150 },
          children: [
            new TextRun({
              text: "处理措施：",
              bold: true,
            }),
          ],
        }),

        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun(
              "优先安排客户经理对TOP10风险专区进行电话或实地回访"
            ),
          ],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun(
              "了解客户流失原因：是业务暂停、平台迁移还是服务问题"
            ),
          ],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun(
              "针对可挽回客户，制定专属优惠政策或服务升级方案"
            ),
          ],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun(
              "建立客户流失预警机制，定期监控专区活跃度"
            ),
          ],
        }),

        // 建议3
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun("4.3 橙色等级专区（持续优化）")],
        }),

        new Paragraph({
          spacing: { after: 150 },
          children: [
            new TextRun({
              text: "处理对象：",
              bold: true,
            }),
            new TextRun("指标二（64个）+ 指标四（60个）= 124个25年前低收益专区"),
          ],
        }),

        new Paragraph({
          spacing: { after: 150 },
          children: [
            new TextRun({
              text: "处理措施：",
              bold: true,
            }),
          ],
        }),

        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun(
              "分析专区所在行业特点和区域市场环境，找出收益低的外部原因"
            ),
          ],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun(
              "对比同类高收益专区的运营模式，提炼可复制的成功经验"
            ),
          ],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun(
              "针对收益在5-10万的专区，制定冲刺方案争取突破10万门槛"
            ),
          ],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [
            new TextRun(
              "定期组织运营培训，提升专区管理员运营能力"
            ),
          ],
        }),

        // 五、总结
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          children: [new TextRun("五、总结")],
        }),

        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun(
              "本次统计共识别出124个需要关注的低收益专区，其中红色等级124个、橙色等级124个、灰色等级20个。从数据趋势来看，部分早期接入的专区存在运营效率低下、客户活跃度下降等问题，需要引起管理层高度重视。"
            ),
          ],
        }),

        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun(
              "建议成立专项工作组，由运营中心牵头，联合客服、技术、销售等部门，按照'先急后缓、先大后小'的原则，分批推进低收益专区的整改提升工作。对于长期无收益且无可挽救价值的专区，建议果断下线以节约运营成本；对于有潜力的专区，加大资源投入和运营支持，力争在2026年下半年实现收益显著提升。"
            ),
          ],
        }),

        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun(
              "后续将建立月度监控机制，持续跟踪各专区收益变化情况，及时发现问题并调整策略，确保e交易平台整体运营质量稳步提升。"
            ),
          ],
        }),

        // 附录说明
        new Paragraph({
          spacing: { before: 400, after: 100 },
          children: [
            new TextRun({
              text: "【附录】",
              bold: true,
              size: 22,
              color: "666666",
            }),
          ],
        }),

        new Paragraph({
          spacing: { after: 100 },
          children: [
            new TextRun({
              text: "详细数据请参见附件《专区低收益统计结果.xlsx》，包含六个指标的完整数据清单。",
              size: 20,
              color: "666666",
            }),
          ],
        }),
      ],
    },
  ],
});

// 创建指标统计表格
function createMetricsTable() {
  const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
  const cellBorders = {
    top: tableBorder,
    bottom: tableBorder,
    left: tableBorder,
    right: tableBorder,
  };

  return new Table({
    columnWidths: [1200, 3500, 1200, 1500, 1960],
    rows: [
      // 表头
      new TableRow({
        tableHeader: true,
        children: [
          createHeaderCell("指标", 1200),
          createHeaderCell("条件", 3500),
          createHeaderCell("数量", 1200),
          createHeaderCell("风险等级", 1500),
          createHeaderCell("备注", 1960),
        ],
      }),
      // 数据行
      createDataRow(
        "指标一",
        "接入超过1年，总收益<10w",
        "67",
        "🔴 红色",
        "重点关注",
        cellBorders
      ),
      createDataRow(
        "指标二",
        "25年前接入，25年收益<10w",
        "64",
        "🟠 橙色",
        "需改进",
        cellBorders
      ),
      createDataRow(
        "指标三",
        "接入超过1年，总收益<5w",
        "57",
        "🔴 红色",
        "重点关注",
        cellBorders
      ),
      createDataRow(
        "指标四",
        "25年前接入，25年收益<5w",
        "60",
        "🟠 橙色",
        "需改进",
        cellBorders
      ),
      createDataRow(
        "指标五",
        "26年产生收益",
        "35",
        "🟡 黄色",
        "观察",
        cellBorders
      ),
      createDataRow(
        "指标六",
        "25年有收益，26年无",
        "20",
        "⚪ 灰色",
        "流失风险",
        cellBorders
      ),
    ],
  });
}

function createHeaderCell(text, width) {
  return new TableCell({
    borders: {
      top: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
      bottom: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
      left: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
      right: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" },
    },
    width: { size: width, type: WidthType.DXA },
    shading: { fill: "1F4E79", type: ShadingType.CLEAR },
    verticalAlign: VerticalAlign.CENTER,
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({
            text: text,
            bold: true,
            color: "FFFFFF",
            size: 22,
          }),
        ],
      }),
    ],
  });
}

function createDataRow(
  index,
  condition,
  count,
  riskLevel,
  remark,
  cellBorders
) {
  const riskColors = {
    "🔴 红色": "C00000",
    "🟠 橙色": "ED7D31",
    "🟡 黄色": "FFC000",
    "⚪ 灰色": "7F7F7F",
  };

  return new TableRow({
    children: [
      new TableCell({
        borders: cellBorders,
        width: { size: 1200, type: WidthType.DXA },
        verticalAlign: VerticalAlign.CENTER,
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: index, size: 22 })],
          }),
        ],
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: 3500, type: WidthType.DXA },
        verticalAlign: VerticalAlign.CENTER,
        children: [
          new Paragraph({
            children: [new TextRun({ text: condition, size: 22 })],
          }),
        ],
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: 1200, type: WidthType.DXA },
        verticalAlign: VerticalAlign.CENTER,
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: count, size: 22, bold: true }),
            ],
          }),
        ],
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: 1500, type: WidthType.DXA },
        verticalAlign: VerticalAlign.CENTER,
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({
                text: riskLevel,
                size: 22,
                color: riskColors[riskLevel] || "000000",
                bold: true,
              }),
            ],
          }),
        ],
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: 1960, type: WidthType.DXA },
        verticalAlign: VerticalAlign.CENTER,
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: remark, size: 22 })],
          }),
        ],
      }),
    ],
  });
}

// 保存文档
Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(
    "D:\\work\\运营中心\\yxzx\\新点e交易相关材料\\日常数据运维工具\\temp\\e交易专区收益成本统计报告.docx",
    buffer
  );
  console.log("文档生成成功！");
});
