# -*- utf-8 -*-
import requests

APP_ID = 'cli_a92024d097381cc5'
APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'

# 获取 Token
resp = requests.post('https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal', 
                     json={'app_id': APP_ID, 'app_secret': APP_SECRET}, timeout=30)
app_token = resp.json().get('app_access_token')
print(f'✅ Token: {app_token[:30]}...')

# 读取 Markdown
with open('D:/openclaw-workspace/oa_mail_for_upload_20260419_161246.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 使用飞书云文档创建 API（直接创建带内容的文档）
print('\n📄 创建带内容的飞书文档...')
url = 'https://open.feishu.cn/open-apis/docx/v1/documents'
headers = {'Authorization': f'Bearer {app_token}', 'Content-Type': 'application/json'}

# 直接创建并写入
data = {
    'title': 'OA 邮件分析报表 - 2026-04-19',
    'content': content
}

resp = requests.post(url, headers=headers, json=data, timeout=30)
print(f'状态码：{resp.status_code}')
print(f'响应：{resp.text[:800]}')

if resp.status_code == 200:
    result = resp.json()
    doc_id = result.get('data', {}).get('document', {}).get('document_id')
    print(f'\n✅ 创建成功!')
    print(f'📄 文档 ID: {doc_id}')
    print(f'🔗 查看：https://bytedance.feishu.cn/docx/{doc_id}')
else:
    print(f'\n❌ 失败')
