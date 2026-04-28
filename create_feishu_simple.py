# -*- utf-8 -*-
import requests
import json

APP_ID = 'cli_a92024d097381cc5'
APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'

print('🔑 获取飞书应用 Token...')
token_url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
resp = requests.post(token_url, json={'app_id': APP_ID, 'app_secret': APP_SECRET}, timeout=30)
token_result = resp.json()
app_token = token_result.get('app_access_token')
print(f'✅ Token: {app_token[:30]}...')

print('\n📄 创建飞书文档...')
create_url = 'https://open.feishu.cn/open-apis/docx/v1/documents'
headers = {'Authorization': f'Bearer {app_token}', 'Content-Type': 'application/json'}
create_resp = requests.post(create_url, headers=headers, json={'title': 'OA 邮件分析报表 - 2026-04-19'}, timeout=30)
create_result = create_resp.json()
doc_token = create_result.get('data', {}).get('document', {}).get('document_id')
doc_url = f'https://bytedance.feishu.cn/docx/{doc_token}'

print(f'\n✅ 文档创建成功!')
print(f'📄 文档 ID: {doc_token}')
print(f'🔗 在线查看：{doc_url}')
print(f'\n📝 内容请手动复制：D:\\openclaw-workspace\\oa_mail_for_upload_20260419_161246.md')
