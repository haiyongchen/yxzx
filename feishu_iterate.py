# -*- utf-8 -*-
import requests

APP_ID = 'cli_a92024d097381cc5'
APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'
DOC_TOKEN = 'DUkcdNjeqordlzxXK84cslYPneb'

# 获取 Token
resp = requests.post('https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal', 
                     json={'app_id': APP_ID, 'app_secret': APP_SECRET}, timeout=30)
app_token = resp.json().get('app_access_token')

# 飞书文档 API - 迭代所有块
print('📖 迭代文档块...')
url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/iterator'
headers = {'Authorization': f'Bearer {app_token}'}

# 获取迭代器
resp = requests.post(url, headers=headers, json={'document_id': DOC_TOKEN}, timeout=30)
print(f'迭代器状态：{resp.status_code}')
print(f'响应：{resp.text[:300]}')

if resp.status_code == 200:
    iterator_id = resp.json().get('data', {}).get('iterator_id')
    print(f'\n✅ 迭代器 ID: {iterator_id}')
    
    # 获取下一批块
    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/iterator/{iterator_id}/next_batch'
    resp = requests.get(url, headers=headers, timeout=30)
    print(f'\n块列表状态：{resp.status_code}')
    print(f'响应：{resp.text[:500]}')
