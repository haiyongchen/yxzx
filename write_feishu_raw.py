# -*- utf-8 -*-
import requests
import base64

APP_ID = 'cli_a92024d097381cc5'
APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'
DOC_TOKEN = 'DUkcdNjeqordlzxXK84cslYPneb'

# 获取 Token
resp = requests.post('https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal', 
                     json={'app_id': APP_ID, 'app_secret': APP_SECRET}, timeout=30)
app_token = resp.json().get('app_access_token')

# 尝试飞书云文档 API
print('✏️  使用云文档 API 写入...')

# 读取 Markdown 文件
with open('D:/openclaw-workspace/oa_mail_for_upload_20260419_161246.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 飞书文档 API v2 - 更新文档
url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/raw_content'
headers = {
    'Authorization': f'Bearer {app_token}',
    'Content-Type': 'application/json'
}
data = {
    'content_type': 'markdown',
    'content': content
}

resp = requests.put(url, headers=headers, json=data, timeout=30)
print(f'状态码：{resp.status_code}')
print(f'响应：{resp.text[:500]}')

if resp.status_code == 200:
    print('\n✅ 内容写入成功!')
    print(f'🔗 查看：https://bytedance.feishu.cn/docx/{DOC_TOKEN}')
else:
    # 尝试另一个端点
    print('\n🔄 尝试分块追加...')
    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/append'
    data = {'content': content[:1000]}  # 先测试前 1000 字符
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    print(f'追加状态：{resp.status_code}')
    print(f'追加响应：{resp.text[:300]}')
