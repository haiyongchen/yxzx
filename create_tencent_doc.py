# -*- utf-8 -*-
"""
使用腾讯文档 API 创建邮件分析表格
"""
import subprocess
import json
import os
from datetime import datetime

# 设置 Token
os.environ['TENCENT_DOCS_TOKEN'] = 'e23255dcdf51491cb208ecc9cc341e21'

# 邮件数据
mails = [
    ["1", "【阳光优采】关于近期平台上量过程中的问题及工作建议总结梳理", "李涛 (运营中心)", "星期六 08:33", "电子商城", "6 大问题 +5 项建议，涉及商品类型、流程优化、价格巡查等", "⭐⭐⭐"],
    ["2", "【规范评审】服务器预规划流程、正式部署流程增加 pinpoint 监控体系内容评审", "包亚峰", "星期五 16:26", "系统通知", "Pinpoint 监控体系评审，4 月 22 日前反馈", "⭐⭐"],
    ["3", "【商城专区开设】武汉光谷联合产权交易所黄石分公司", "罗永健", "星期五 08:35", "招投标", "五五分成协议，协调商城平台搭建", "⭐⭐⭐"],
    ["4", "AI 评标系统废标情况查询", "沙宏宇", "星期二 17:44", "招投标", "技术标废标异常，需排查复评", "⭐⭐"],
    ["5", "关于新疆阳光采购平台升级后市场推广上量相关事宜的沟通", "庞丹枫", "星期二 13:03", "招投标", "3 家国企入企推广讲座，PPT 优化需求", "⭐⭐⭐"],
    ["6", "山东兴多专区提取部署事宜", "庞鑫", "星期二 11:16", "电子商城", "年保底 130 个项目，申请提前开设专区", "⭐⭐"],
    ["7", "营销周报（4.7-4.10）-徐志远", "徐志远", "星期二 09:36", "工作汇报", "每周营销工作汇报", "⭐"],
    ["8", "AI 沈阳试点项目私有模型调试和切换工作协调备案", "沙宏宇", "星期一 18:54", "电子商城", "3 台物理机 24 张显卡，Qwen3.5 部署", "⭐⭐"],
    ["9", "2026 年度企业职业技能等级（高级）认定工作开展", "耿李欢", "星期一 14:52", "培训学习", "职业技能认定，培训 + 考核，补贴 500 元", "⭐"],
    ["10", "关于中新建数字发展有限责任公司建设兵团国有企业招采平台技术方案交流会事宜", "王东 (交易兵团分公司)", "星期一 14:51", "招投标", "技术方案交流，下周二 10 点半", "⭐⭐⭐"],
    ["11", "关于阳光优采运营及产品相关工作", "黄严宝", "星期一 13:39", "电子商城", "运营产品工作安排", "⭐⭐"],
    ["12", "【季报】新点e 交易平台第一季度季报 2026 年 1-3 月", "钟明珠", "2026-04-12", "工作汇报", "Q1 季度运营数据报告", "⭐⭐⭐"],
    ["13", "关于阳光优采平台常见问题收集的专项邮件", "马博林", "2026-04-10", "电子商城", "平台问题收集汇总", "⭐⭐"],
    ["14", "E 招冀成 - 对接客户数据中台数据推送工作说明备案", "宋品桥", "2026-04-10", "系统通知", "数据中台推送工作说明", "⭐⭐"],
    ["15", "关于新疆阳光采购平台升级建设工作立项事宜内部协调", "庞丹枫", "2026-04-10", "招投标", "项目立项内部协调", "⭐⭐⭐"],
]

# 创建 Markdown 表格
headers = ["序号", "邮件主题", "发件人", "日期", "分类", "内容摘要", "优先级"]

md_content = "# 📧 OA 邮件分析报表\n\n"
md_content += f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
md_content += f"**时间范围**: 最近 7 天\n"
md_content += f"**邮件总数**: {len(mails)} 封\n\n"

# 表格
md_content += "## 📊 邮件列表\n\n"
md_content += "| " + " | ".join(headers) + " |\n"
md_content += "| " + " | ".join(["---"] * len(headers)) + " |\n"

for row in mails:
    md_content += "| " + " | ".join([str(cell).replace('|', '\\|') for cell in row]) + " |\n"

# 统计
md_content += "\n## 📈 分类统计\n\n"
cat_count = {}
for row in mails:
    cat = row[4]
    cat_count[cat] = cat_count.get(cat, 0) + 1

for cat, count in sorted(cat_count.items(), key=lambda x: -x[1]):
    md_content += f"- **{cat}**: {count} 封\n"

md_content += "\n## 🎯 优先级统计\n\n"
pri_count = {}
for row in mails:
    pri = row[6]
    pri_count[pri] = pri_count.get(pri, 0) + 1

for pri in ['⭐⭐⭐', '⭐⭐', '⭐']:
    if pri in pri_count:
        md_content += f"- {pri}: {pri_count[pri]} 封\n"

md_content += "\n---\n\n**生成工具**: `skills/oa-mail-analyzer`\n"

# 保存本地备份
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
local_file = f'oa_mail_for_upload_{timestamp}.md'
with open(local_file, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"💾 本地文件已保存：{local_file}")
print(f"\n📄 文档内容预览 (前 500 字):\n{md_content[:500]}...")

# 调用腾讯文档 API
print("\n\n🚀 调用腾讯文档 API 创建文档...")

args = {
    'title': f'OA 邮件分析报表-{datetime.now().strftime("%Y%m%d")}',
    'content': md_content
}

result = subprocess.run(
    ['powershell', '-ExecutionPolicy', 'Bypass', '-File', 'D:\nvm4w\nodejs\mcporter.ps1', 'call', 'tencent-docs', 'create_smartcanvas_by_mdx', '--args', json.dumps(args, ensure_ascii=False)],
    capture_output=True,
    text=True,
    timeout=30,
    env=os.environ
)

print(f"\n返回码：{result.returncode}")
print(f"STDOUT: {result.stdout[:1000]}")
if result.stderr:
    print(f"STDERR: {result.stderr[:500]}")

if result.returncode == 0:
    try:
        response = json.loads(result.stdout.strip())
        print(f"\n解析响应：{json.dumps(response, indent=2, ensure_ascii=False)[:500]}")
        
        if 'error' in response and (not response['error'] or response['error'] == ''):
            file_id = response.get('file_id', response.get('node_id', ''))
            url = response.get('url', f'https://docs.qq.com/doc/{file_id}')
            print(f"\n✅ 创建成功！")
            print(f"   📄 文档 ID: {file_id}")
            print(f"   🔗 在线查看：{url}")
        else:
            print(f"\n❌ 创建失败：{response.get('error', '未知错误')}")
            if '400007' in str(response.get('error', '')):
                print("\n⚠️  VIP 权限不足，请升级腾讯文档 VIP")
    except Exception as e:
        print(f"\n❌ 响应解析失败：{e}")
else:
    print("\n❌ 调用失败")
