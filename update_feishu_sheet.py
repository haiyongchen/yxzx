# -*- utf-8 -*-
import requests
import json

# 读取 OA 邮件数据
with open('D:/openclaw-workspace/oa_mails_full.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 准备表格数据
rows = []
for mail in data['mails']:
    # 简化内容总结（前 100 字）
    content_summary = mail['content'][:100].replace('\n', ' ') + '...' if len(mail['content']) > 100 else mail['content'].replace('\n', ' ')
    
    rows.append([
        str(mail['index']),
        mail['subject'],
        mail['sender'],
        mail['category'],
        mail['priority'],
        mail['link'],
        content_summary
    ])

# 飞书 API
APP_ID = 'cli_a92024d097381cc5'
APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'

# 获取 Token
resp = requests.post('https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal', 
                     json={'app_id': APP_ID, 'app_secret': APP_SECRET}, timeout=30)
app_token = resp.json().get('app_access_token')
print(f'✅ Token: {app_token[:50]}...')

# 飞书表格 Token
spreadsheet_token = 'SO2Xs2vlkh4XKNt0VfOclqWYn6g'

# 更新表格
print('\n📊 更新飞书表格...')
url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/Sheet1!A1:G16'
headers = {
    'Authorization': f'Bearer {app_token}',
    'Content-Type': 'application/json'
}

# 添加表头
values = [['序号', '邮件主题', '发件人', '分类', '优先级', '邮件地址', '内容总结']]
values.extend(rows)

data = {
    'values': values
}

resp = requests.put(url, headers=headers, json=data, timeout=30)
print(f'状态码：{resp.status_code}')
print(f'响应：{resp.text[:500]}')

if resp.status_code == 200:
    print('\n✅ 表格更新成功!')
    print(f'🔗 查看：https://www.feishu.cn/sheets/{spreadsheet_token}')
else:
    print(f'\n❌ 更新失败')
