# -*- utf-8 -*-
import requests
import json

APP_ID = 'cli_a92024d097381cc5'
APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'
DOC_TOKEN = 'DUkcdNjeqordlzxXK84cslYPneb'

# 获取 Token
resp = requests.post('https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal', 
                     json={'app_id': APP_ID, 'app_secret': APP_SECRET}, timeout=30)
token_result = resp.json()
app_token = token_result.get('app_access_token')
print(f'✅ Token: {app_token[:30]}...')

# 飞书文档 V2 API - 获取文档结构
print('\n📖 获取文档结构...')
url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}'
headers = {'Authorization': f'Bearer {app_token}'}
resp = requests.get(url, headers=headers, timeout=30)
print(f'获取文档状态：{resp.status_code}')

# 创建块
print('\n✏️  创建内容块...')
url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks'
headers = {'Authorization': f'Bearer {app_token}', 'Content-Type': 'application/json'}

# 简单文本块
data = {
    'parent_block_id': DOC_TOKEN,
    'block_type': 'text',
    'text': {
        'elements': [{
            'text_run': {
                'content': '# OA 邮件分析报表\n\n分析时间：2026-04-19\n邮件总数：15 封'
            }
        }]
    }
}

resp = requests.post(url, headers=headers, json=data, timeout=30)
print(f'创建块状态：{resp.status_code}')
print(f'响应：{resp.text[:500]}')

if resp.status_code == 200:
    result = resp.json()
    print(f'\n✅ 块创建成功!')
    print(f'块 ID: {result.get("data", {}).get("block_id")}')
else:
    print(f'\n❌ 块创建失败')
    # 尝试直接导入 Markdown
    print('\n🔄 尝试导入 Markdown...')
    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/import_markdown'
    with open('D:/openclaw-workspace/oa_mail_for_upload_20260419_161246.md', 'r', encoding='utf-8') as f:
        md_content = f.read()
    data = {'markdown': md_content}
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    print(f'导入状态：{resp.status_code}')
    print(f'导入响应：{resp.text[:300]}')
