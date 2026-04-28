# -*- utf-8 -*-
import requests

APP_ID = 'cli_a92024d097381cc5'
APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'
DOC_TOKEN = 'JTQwdmu85omOZlxJFdlckyWKnhf'

# 获取 Token
resp = requests.post('https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal', 
                     json={'app_id': APP_ID, 'app_secret': APP_SECRET}, timeout=30)
app_token = resp.json().get('app_access_token')

# 读取 Markdown
with open('D:/openclaw-workspace/oa_mail_for_upload_20260419_161246.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 更新文档
print('✏️  更新文档内容...')
url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}'
headers = {'Authorization': f'Bearer {app_token}', 'Content-Type': 'application/json'}
data = {'content': content}

resp = requests.patch(url, headers=headers, json=data, timeout=30)
print(f'状态码：{resp.status_code}')
print(f'响应：{resp.text[:500]}')

if resp.status_code == 200:
    print('\n✅ 更新成功!')
    print(f'🔗 查看：https://bytedance.feishu.cn/docx/{DOC_TOKEN}')
else:
    print('\n❌ 更新失败')
    print('请查看文档：https://bytedance.feishu.cn/docx/JTQwdmu85omOZlxJFdlckyWKnhf')
