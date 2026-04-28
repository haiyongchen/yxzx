# -*- utf-8 -*-
"""
飞书文档内容写入 - 使用多种 API 尝试
"""
import requests
import json

APP_ID = 'cli_a92024d097381cc5'
APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'
DOC_TOKEN = 'JTQwdmu85omOZlxJFdlckyWKnhf'

# 获取 Token
print('🔑 获取 Token...')
resp = requests.post('https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal', 
                     json={'app_id': APP_ID, 'app_secret': APP_SECRET}, timeout=30)
token_result = resp.json()
if token_result.get('code') != 0:
    print(f'❌ Token 获取失败：{token_result}')
    exit(1)
app_token = token_result.get('app_access_token')
print(f'✅ Token: {app_token[:50]}...')

# 读取 Markdown 内容
with open('D:/openclaw-workspace/oa_mail_for_upload_20260419_161246.md', 'r', encoding='utf-8') as f:
    content = f.read()
print(f'📝 内容长度：{len(content)} 字符')

# 尝试 1: 使用导入 Markdown API
print('\n📄 尝试 1: 导入 Markdown...')
url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/import_markdown'
headers = {'Authorization': f'Bearer {app_token}', 'Content-Type': 'application/json'}
data = {'markdown': content}
resp = requests.post(url, headers=headers, json=data, timeout=30)
print(f'状态码：{resp.status_code}')
if resp.status_code == 200:
    print('✅ 导入成功!')
    print(f'🔗 https://bytedance.feishu.cn/docx/{DOC_TOKEN}')
    exit(0)
else:
    print(f'❌ 导入失败：{resp.text[:200]}')

# 尝试 2: 使用批量创建块 API
print('\n📄 尝试 2: 批量创建块...')
url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks/batch_create'
data = {
    'parent_block_id': DOC_TOKEN,
    'blocks': [{
        'block_type': 1,
        'text': {'elements': [{'text_run': {'content': content[:3000]}}]}
    }]
}
resp = requests.post(url, headers=headers, json=data, timeout=30)
print(f'状态码：{resp.status_code}')
if resp.status_code == 200:
    print('✅ 块创建成功!')
    exit(0)
else:
    print(f'❌ 块创建失败：{resp.text[:200]}')

# 尝试 3: 使用文件上传 API
print('\n📄 尝试 3: 上传文件...')
# 先上传为临时文件
upload_url = 'https://open.feishu.cn/open-apis/drive/v1/medias/upload_all'
upload_headers = {'Authorization': f'Bearer {app_token}'}
files = {'media': ('report.md', content.encode('utf-8'), 'text/markdown')}
resp = requests.post(upload_url, headers=upload_headers, files=files, timeout=30)
print(f'上传状态：{resp.status_code}')
if resp.status_code == 200:
    upload_result = resp.json()
    file_token = upload_result.get('data', {}).get('file_token')
    print(f'✅ 文件上传成功：{file_token}')
else:
    print(f'❌ 上传失败：{resp.text[:200]}')

print(f'\n📄 文档链接：https://bytedance.feishu.cn/docx/{DOC_TOKEN}')
