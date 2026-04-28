# -*- utf-8 -*-
"""
使用飞书云盘 API 创建并导入文档
"""
import requests

APP_ID = 'cli_a92024d097381cc5'
APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'

# 获取 Token
resp = requests.post('https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal', 
                     json={'app_id': APP_ID, 'app_secret': APP_SECRET}, timeout=30)
app_token = resp.json().get('app_access_token')
print(f'✅ Token: {app_token[:50]}...')

# 读取 Markdown
with open('D:/openclaw-workspace/oa_mail_for_upload_20260419_161246.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 使用云盘 API 创建文档
print('\n📄 使用云盘 API 创建文档...')
url = 'https://open.feishu.cn/open-apis/drive/v1/files'
headers = {
    'Authorization': f'Bearer {app_token}',
    'Content-Type': 'application/json'
}

# 创建文档
data = {
    'name': 'OA 邮件分析报表 - 2026-04-19',
    'type': 'doc'
}
resp = requests.post(url, headers=headers, json=data, timeout=30)
print(f'创建状态：{resp.status_code}')
print(f'响应：{resp.text[:500]}')

if resp.status_code == 200:
    result = resp.json()
    file_token = result.get('data', {}).get('file_token')
    print(f'\n✅ 文档创建成功!')
    print(f'File Token: {file_token}')
    print(f'🔗 https://bytedance.feishu.cn/docx/{file_token}')
else:
    print(f'\n❌ 创建失败')
