# -*- utf-8 -*-
"""
使用飞书 API 创建文档
"""
import requests
import json

APP_ID = 'cli_a92024d097381cc5'
APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'

# 1. 获取应用级 Token
print('🔑 获取飞书应用 Token...')
token_url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
token_data = {
    'app_id': APP_ID,
    'app_secret': APP_SECRET
}

resp = requests.post(token_url, json=token_data, timeout=30)
print(f'状态码：{resp.status_code}')

if resp.status_code != 200:
    print(f'❌ 获取 Token 失败：{resp.text}')
    exit(1)

token_result = resp.json()
if token_result.get('code') != 0:
    print(f'❌ 错误：{token_result}')
    exit(1)

app_token = token_result.get('app_access_token')
print(f'✅ Token 获取成功：{app_token[:30]}...')

# 2. 创建文档
print('\n📄 创建飞书文档...')
create_url = 'https://open.feishu.cn/open-apis/docx/v1/documents'
headers = {
    'Authorization': f'Bearer {app_token}',
    'Content-Type': 'application/json'
}
create_data = {
    'title': 'OA 邮件分析报表 - 2026-04-19'
}

create_resp = requests.post(create_url, headers=headers, json=create_data, timeout=30)
print(f'创建状态码：{create_resp.status_code}')
print(f'创建响应：{create_resp.text[:500]}')

if create_resp.status_code == 200:
    create_result = create_resp.json()
    if create_result.get('code') == 0:
        doc_token = create_result.get('data', {}).get('document', {}).get('document_id')
        doc_url = f'https://bytedance.feishu.cn/docx/{doc_token}'
        print(f'\n✅ 文档创建成功!')
        print(f'📄 文档 ID: {doc_token}')
        print(f'🔗 在线查看：{doc_url}')
        
        # 3. 写入内容（飞书文档需要分块写入）
        print('\n✏️  写入文档内容...')
        # 使用 blocks API 创建内容
        blocks_url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks'
        headers['Content-Type'] = 'application/json'
        
        # 创建标题块
        block_data = {
            'parent_block_id': doc_token,
            'block_type': 1,  # 文本块
            'text': {
                'elements': [{
                    'text_run': {
                        'content': '📧 OA 邮件分析报表\n\n分析时间：2026-04-19\n时间范围：最近 7 天\n邮件总数：15 封\n\n详见：https://docs.qq.com/sheet/DWXBwWUJ1R0JhWUta'
                    }
                }]
            }
        }
        
        block_resp = requests.post(blocks_url, headers=headers, json=block_data, timeout=30)
        print(f'块创建状态码：{block_resp.status_code}')
        print(f'块创建响应：{block_resp.text[:300]}')

**分析时间**: 2026-04-19
**时间范围**: 最近 7 天
**邮件总数**: 15 封

## 📊 邮件列表

| 序号 | 邮件主题 | 发件人 | 分类 | 优先级 |
|------|----------|--------|------|--------|
| 1 | 【阳光优采】关于近期平台上量过程中的问题及工作建议总结梳理 | 李涛 (运营中心) | 电子商城 | ⭐⭐⭐ |
| 2 | 【规范评审】服务器预规划流程增加 pinpoint 监控 | 包亚峰 | 系统通知 | ⭐⭐ |
| 3 | 【商城专区开设】武汉光谷联合产权交易所黄石分公司 | 罗永健 | 招投标 | ⭐⭐⭐ |
| 4 | AI 评标系统废标情况查询 | 沙宏宇 | 招投标 | ⭐⭐ |
| 5 | 新疆阳光采购平台升级推广 | 庞丹枫 | 招投标 | ⭐⭐⭐ |
| 6 | 山东兴多专区提取部署 | 庞鑫 | 电子商城 | ⭐⭐ |
| 7 | 营销周报（4.7-4.10）| 徐志远 | 工作汇报 | ⭐ |
| 8 | AI 沈阳试点私有模型部署 | 沙宏宇 | 电子商城 | ⭐⭐ |
| 9 | 职业技能等级认定工作 | 耿李欢 | 培训学习 | ⭐ |
| 10 | 中新建数字招采平台技术交流 | 王东 | 招投标 | ⭐⭐⭐ |
| 11 | 阳光优采运营及产品工作 | 黄严宝 | 电子商城 | ⭐⭐ |
| 12 | 【季报】新点 e 交易 Q1 季报 | 钟明珠 | 工作汇报 | ⭐⭐⭐ |
| 13 | 阳光优采平台问题收集 | 马博林 | 电子商城 | ⭐⭐ |
| 14 | E 招冀成数据推送备案 | 宋品桥 | 系统通知 | ⭐⭐ |
| 15 | 新疆平台升级立项协调 | 庞丹枫 | 招投标 | ⭐⭐⭐ |

## 📈 分类统计
- 电子商城：5 封
- 招投标：5 封
- 系统通知：2 封
- 工作汇报：2 封
- 培训学习：1 封

## 🎯 优先级
- ⭐⭐⭐: 6 封
- ⭐⭐: 7 封
- ⭐: 2 封
'''
        }
        
        content_resp = requests.put(content_url, headers=headers, json=content_data, timeout=30)
        print(f'内容写入状态码：{content_resp.status_code}')
        print(f'内容写入响应：{content_resp.text[:300]}')
        
    else:
        print(f'❌ 创建失败：{create_result}')
else:
    print(f'❌ HTTP 错误：{create_resp.status_code}')
