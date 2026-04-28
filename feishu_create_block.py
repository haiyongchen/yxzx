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

# 飞书 API - 创建块（在文档末尾添加）
print('✏️  添加内容块...')
url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks'
headers = {'Authorization': f'Bearer {app_token}', 'Content-Type': 'application/json'}

# 使用正确的块结构
data = {
    'parent_block_id': DOC_TOKEN,
    'block_type': 86,  # 文本块
    'text': {
        'elements': [{
            'text_run': {
                'content': content[:2000]  # 先写入前 2000 字符
            }
        }]
    }
}

resp = requests.post(url, headers=headers, json=data, timeout=30)
print(f'状态码：{resp.status_code}')
result = resp.json()
print(f'响应：{result}')

if resp.status_code == 200:
    block_id = result.get('data', {}).get('block_id')
    print(f'\n✅ 块创建成功!')
    print(f'块 ID: {block_id}')
    print(f'🔗 查看：https://bytedance.feishu.cn/docx/{DOC_TOKEN}')
else:
    print(f'\n❌ 失败：{result.get("msg", result)}')
