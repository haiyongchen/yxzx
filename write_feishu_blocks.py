# -*- utf-8 -*-
import requests

APP_ID = 'cli_a92024d097381cc5'
APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'
DOC_TOKEN = 'DUkcdNjeqordlzxXK84cslYPneb'

# 获取 Token
resp = requests.post('https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal', 
                     json={'app_id': APP_ID, 'app_secret': APP_SECRET}, timeout=30)
app_token = resp.json().get('app_access_token')

print('✏️  写入文档内容（使用块 API）...')

# 飞书文档块 API
url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks'
headers = {
    'Authorization': f'Bearer {app_token}',
    'Content-Type': 'application/json'
}

# 创建文本块（简单内容）
data = {
    'parent_block_id': DOC_TOKEN,
    'block_type': 1,
    'text': {
        'elements': [{
            'text_run': {
                'content': '# 📧 OA 邮件分析报表\n\n分析时间：2026-04-19\n时间范围：最近 7 天\n邮件总数：15 封\n\n## 📊 邮件列表\n\n|序号 | 邮件主题 | 发件人 | 分类 | 优先级|\n|-----|---------|--------|------|-------|\n| 1 | 【阳光优采】关于近期平台上量过程中的问题及工作建议总结梳理 | 李涛 (运营中心) | 电子商城 | ⭐⭐⭐ |\n| 2 | 【规范评审】服务器预规划流程增加 pinpoint 监控 | 包亚峰 | 系统通知 | ⭐⭐ |\n| 3 | 【商城专区开设】武汉光谷联合产权交易所黄石分公司 | 罗永健 | 招投标 | ⭐⭐⭐ |\n| 4 | AI 评标系统废标情况查询 | 沙宏宇 | 招投标 | ⭐⭐ |\n| 5 | 新疆阳光采购平台升级推广 | 庞丹枫 | 招投标 | ⭐⭐⭐ |\n| 6 | 山东兴多专区提取部署 | 庞鑫 | 电子商城 | ⭐⭐ |\n| 7 | 营销周报（4.7-4.10）| 徐志远 | 工作汇报 | ⭐ |\n| 8 | AI 沈阳试点私有模型部署 | 沙宏宇 | 电子商城 | ⭐⭐ |\n| 9 | 职业技能等级认定工作 | 耿李欢 | 培训学习 | ⭐ |\n| 10 | 中新建数字招采平台技术交流 | 王东 | 招投标 | ⭐⭐⭐ |\n| 11 | 阳光优采运营及产品工作 | 黄严宝 | 电子商城 | ⭐⭐ |\n| 12 | 【季报】新点 e 交易 Q1 季报 | 钟明珠 | 工作汇报 | ⭐⭐⭐ |\n| 13 | 阳光优采平台问题收集 | 马博林 | 电子商城 | ⭐⭐ |\n| 14 | E 招冀成数据推送备案 | 宋品桥 | 系统通知 | ⭐⭐ |\n| 15 | 新疆平台升级立项协调 | 庞丹枫 | 招投标 | ⭐⭐⭐ |\n\n## 📈 分类统计\n- 电子商城：5 封\n- 招投标：5 封\n- 系统通知：2 封\n- 工作汇报：2 封\n- 培训学习：1 封\n\n## 🎯 优先级\n- ⭐⭐⭐: 6 封\n- ⭐⭐: 7 封\n- ⭐: 2 封'
            }
        }]
    }
}

resp = requests.post(url, headers=headers, json=data, timeout=30)
print(f'状态码：{resp.status_code}')
print(f'响应：{resp.text[:500]}')

if resp.status_code == 200:
    print('\n✅ 内容写入成功!')
    print(f'🔗 查看文档：https://bytedance.feishu.cn/docx/{DOC_TOKEN}')
else:
    print('\n❌ 写入失败')
