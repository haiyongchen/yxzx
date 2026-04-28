# -*- utf-8 -*-
"""
直接调用腾讯文档 API
"""
import requests
import json

TOKEN = 'e23255dcdf51491cb208ecc9cc341e21'

# 读取内容
with open('D:/openclaw-workspace/oa_mail_for_upload_20260419_161246.md', 'r', encoding='utf-8') as f:
    content = f.read()

title = 'OA 邮件分析报表 -20260419'

print('🚀 调用腾讯文档 API...')
print(f'📄 标题：{title}')
print(f'📝 内容长度：{len(content)}')

# 腾讯文档 API
url = 'https://docs.qq.com/openapi/doc/create'
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}
data = {
    'title': title,
    'type': 'doc',
    'content': content
}

try:
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    print(f'\n状态码：{resp.status_code}')
    print(f'响应：{resp.text[:500]}')
    
    if resp.status_code == 200:
        result = resp.json()
        if result.get('code') == 0:
            doc_id = result.get('data', {}).get('doc_id')
            url = f'https://docs.qq.com/doc/{doc_id}'
            print(f'\n✅ 创建成功!')
            print(f'📄 文档 ID: {doc_id}')
            print(f'🔗 在线查看：{url}')
        else:
            print(f'\n❌ 失败：{result.get("message", result)}')
    else:
        print(f'\n❌ HTTP 错误：{resp.status_code}')
except Exception as e:
    print(f'\n❌ 错误：{e}')
