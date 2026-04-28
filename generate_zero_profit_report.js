const docx = require('docx');
const fs = require('fs');
const { Document, Paragraph, TextRun, Table, TableCell, TableRow, WidthType, AlignmentType, HeadingLevel } = docx;

// 创建文档
const doc = new Document({
    sections: [{
        properties: {},
        children: [
            // 标题
            new Paragraph({
                text: '零收益专区成本分析报告',
                heading: HeadingLevel.TITLE,
                alignment: AlignmentType.CENTER,
                spacing: { after: 200 }
            }),
            
            // 报告日期
            new Paragraph({
                text: '中原华北区 | 报告日期：2026年4月10日',
                alignment: AlignmentType.CENTER,
                spacing: { after: 400 }
            }),
            
            // 一、整体概况
            new Paragraph({
                text: '一、整体概况',
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 300, after: 200 }
            }),
            new Table({
                width: { size: 100, type: WidthType.PERCENTAGE },
                rows: [
                    new TableRow({
                        children: [
                            new TableCell({ children: [new Paragraph({ text: '指标', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '数值', bold: true })] })
                        ]
                    }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('零收益专区数量')] }), new TableCell({ children: [new Paragraph('40个')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('占总专区比例')] }), new TableCell({ children: [new Paragraph('35.1%')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('零收益专区总成本')] }), new TableCell({ children: [new Paragraph('510,622.39元')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('平均成本')] }), new TableCell({ children: [new Paragraph('12,765.56元')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('成本中位数')] }), new TableCell({ children: [new Paragraph('10,060.85元')] })] })
                ]
            }),
            
            // 二、成本额度对比
            new Paragraph({
                text: '二、成本额度对比（基线30,000元）',
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Table({
                width: { size: 100, type: WidthType.PERCENTAGE },
                rows: [
                    new TableRow({
                        children: [
                            new TableCell({ children: [new Paragraph({ text: '指标', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '金额', bold: true })] })
                        ]
                    }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('成本额度总计')] }), new TableCell({ children: [new Paragraph('1,200,000元')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('实际成本总计')] }), new TableCell({ children: [new Paragraph('510,622.39元')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('成本结余')] }), new TableCell({ children: [new Paragraph({ text: '689,377.61元', bold: true })] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('整体成本使用率')] }), new TableCell({ children: [new Paragraph({ text: '42.6%', bold: true })] })] })
                ]
            }),
            
            // 三、成本使用率分布
            new Paragraph({
                text: '三、成本使用率分布',
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Table({
                width: { size: 100, type: WidthType.PERCENTAGE },
                rows: [
                    new TableRow({
                        children: [
                            new TableCell({ children: [new Paragraph({ text: '区间', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '数量', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '占比', bold: true })] })
                        ]
                    }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('零成本')] }), new TableCell({ children: [new Paragraph('4个')] }), new TableCell({ children: [new Paragraph('10%')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('低成本（0-25%）')] }), new TableCell({ children: [new Paragraph('11个')] }), new TableCell({ children: [new Paragraph('27.5%')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('中低成本（25-50%）')] }), new TableCell({ children: [new Paragraph('9个')] }), new TableCell({ children: [new Paragraph('22.5%')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('中成本（50-75%）')] }), new TableCell({ children: [new Paragraph('11个')] }), new TableCell({ children: [new Paragraph('27.5%')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('接近上限（75-100%）')] }), new TableCell({ children: [new Paragraph('1个')] }), new TableCell({ children: [new Paragraph('2.5%')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph({ text: '超支（>100%）', bold: true })] }), new TableCell({ children: [new Paragraph({ text: '4个', bold: true })] }), new TableCell({ children: [new Paragraph({ text: '10%', bold: true })] })] })
                ]
            }),
            
            // 四、超支专区清单
            new Paragraph({
                text: '四、超支专区清单（需重点关注）',
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: '共4个专区成本超支，超支总额39,727.14元',
                spacing: { after: 200 }
            }),
            new Table({
                width: { size: 100, type: WidthType.PERCENTAGE },
                rows: [
                    new TableRow({
                        children: [
                            new TableCell({ children: [new Paragraph({ text: '专区名称', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '实际成本', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '超支金额', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '使用率', bold: true })] })
                        ]
                    }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('焦作市全要素阳光交易平台')] }), new TableCell({ children: [new Paragraph('52,197.73元')] }), new TableCell({ children: [new Paragraph({ text: '+22,197.73元', bold: true })] }), new TableCell({ children: [new Paragraph({ text: '174.0%', bold: true })] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('本溪阳光数字化招标采购平台')] }), new TableCell({ children: [new Paragraph('44,794.02元')] }), new TableCell({ children: [new Paragraph({ text: '+14,794.02元', bold: true })] }), new TableCell({ children: [new Paragraph({ text: '149.3%', bold: true })] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('内蒙古招采专区')] }), new TableCell({ children: [new Paragraph('32,449.52元')] }), new TableCell({ children: [new Paragraph('+2,449.52元')] }), new TableCell({ children: [new Paragraph('108.2%')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('庭州嘉泽工程招投标平台')] }), new TableCell({ children: [new Paragraph('30,285.87元')] }), new TableCell({ children: [new Paragraph('+285.87元')] }), new TableCell({ children: [new Paragraph('101.0%')] })] })
                ]
            }),
            
            // 五、按接入时间分析
            new Paragraph({
                text: '五、按接入时间分析',
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Table({
                width: { size: 100, type: WidthType.PERCENTAGE },
                rows: [
                    new TableRow({
                        children: [
                            new TableCell({ children: [new Paragraph({ text: '接入时长', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '数量', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '平均成本', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '总成本', bold: true })] })
                        ]
                    }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('新接入（3个月内）')] }), new TableCell({ children: [new Paragraph('7个')] }), new TableCell({ children: [new Paragraph('10,914.24元')] }), new TableCell({ children: [new Paragraph('76,399.65元')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('中期（3个月-1年）')] }), new TableCell({ children: [new Paragraph('20个')] }), new TableCell({ children: [new Paragraph('15,314.34元')] }), new TableCell({ children: [new Paragraph('306,286.89元')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('长期（1年以上）')] }), new TableCell({ children: [new Paragraph('13个')] }), new TableCell({ children: [new Paragraph('9,841.22元')] }), new TableCell({ children: [new Paragraph('127,935.85元')] })] })
                ]
            }),
            
            // 六、重点关注专区
            new Paragraph({
                text: '六、重点关注：长期零收益且高成本专区',
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: '共3个专区接入超过1年、成本超过2万、收益为0，需重点评估是否继续投入：',
                spacing: { after: 200 }
            }),
            new Table({
                width: { size: 100, type: WidthType.PERCENTAGE },
                rows: [
                    new TableRow({
                        children: [
                            new TableCell({ children: [new Paragraph({ text: '专区名称', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '实际成本', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '接入天数', bold: true })] }),
                            new TableCell({ children: [new Paragraph({ text: '使用率', bold: true })] })
                        ]
                    }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('本溪阳光数字化招标采购平台')] }), new TableCell({ children: [new Paragraph('44,794.02元')] }), new TableCell({ children: [new Paragraph('549天')] }), new TableCell({ children: [new Paragraph({ text: '149.3%', bold: true })] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('湖北省小额工程电子招标采购交易平台')] }), new TableCell({ children: [new Paragraph('20,790.52元')] }), new TableCell({ children: [new Paragraph('800天')] }), new TableCell({ children: [new Paragraph('69.3%')] })] }),
                    new TableRow({ children: [new TableCell({ children: [new Paragraph('鑫安胜通专区')] }), new TableCell({ children: [new Paragraph('20,150.09元')] }), new TableCell({ children: [new Paragraph('759天')] }), new TableCell({ children: [new Paragraph('67.2%')] })] })
                ]
            }),
            
            // 七、结论与建议
            new Paragraph({
                text: '七、结论与建议',
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: '1. 整体情况',
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 100 }
            }),
            new Paragraph({
                text: '• 40个零收益专区中，36个（90%）成本控制在30,000元基线内',
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: '• 整体成本使用率42.6%，控制良好，成本结余689,377.61元',
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: '• 平均成本12,765元，远低于30,000元基线',
                spacing: { after: 200 }
            }),
            new Paragraph({
                text: '2. 需重点关注',
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 100 }
            }),
            new Paragraph({
                text: '• 4个超支专区：焦作全要素、本溪阳光、内蒙古招采、庭州嘉泽',
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: '• 3个长期零收益高成本专区：本溪阳光、湖北省小额工程、鑫安胜通',
                spacing: { after: 200 }
            }),
            new Paragraph({
                text: '3. 建议措施',
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 100 }
            }),
            new Paragraph({
                text: '（1）对4个超支专区：制定成本压降计划，控制在30,000元基线内',
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: '（2）对3个长期零收益专区：进行ROI评估，考虑下线或转型',
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: '（3）对中期专区（20个）：加强运营支持，争取在1年内实现收益',
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: '（4）对新接入专区（7个）：正常投入，观察3个月后的收益情况',
                spacing: { after: 200 }
            }),
            
            // 八、附件：零收益专区成本明细
            new Paragraph({
                text: '八、附件：零收益专区成本明细（按使用率排序）',
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            })
        ]
    }]
});

// 保存文档
docx.Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync('D:\\openclaw-workspace\\零收益专区成本分析报告.docx', buffer);
    console.log('文档已生成：零收益专区成本分析报告.docx');
}).catch(err => {
    console.error('生成文档失败:', err);
});