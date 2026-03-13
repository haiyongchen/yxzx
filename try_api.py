# -*- coding: utf-8 -*-
"""
尝试访问腾讯文档 API 获取表格数据
"""
import requests
import json
import re

def get_doc_info(doc_id):
    """获取文档信息"""
    
    # 尝试多种 API 端点
    endpoints = [
        f'https://docs.qq.com/api/doc/{doc_id}',
        f'https://docs.qq.com/api/tabs/{doc_id}',
        f'https://docs.qq.com/api/sheet/{doc_id}/info',
        f'https://docs.qq.com/api/sheet/{doc_id}/data',
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'https://docs.qq.com/sheet/{doc_id}',
        'Origin': 'https://docs.qq.com',
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    for endpoint in endpoints:
        try:
            print(f'\n尝试：{endpoint}')
            response = session.get(endpoint, timeout=10)
            print(f'状态码：{response.status_code}')
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f'响应：{json.dumps(data, ensure_ascii=False)[:500]}')
                    
                    # 保存
                    out_file = f'D:\\openclaw-workspace\\api_{doc_id}.json'
                    with open(out_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    print(f'已保存到：{out_file}')
                except:
                    print(f'文本响应：{response.text[:500]}')
        except Exception as e:
            print(f'失败：{e}')

def extract_doc_id(url):
    """从 URL 提取文档 ID"""
    match = re.search(r'/sheet/(D[a-zA-Z0-9]+)', url)
    return match.group(1) if match else None

if __name__ == '__main__':
    urls = [
        'https://docs.qq.com/sheet/DTFdkY3NqamJJVEJl?tab=1sweh3',
        'https://docs.qq.com/sheet/DQnZoWXpYQU5HVEpz?tab=BB08J2'
    ]
    
    for url in urls:
        doc_id = extract_doc_id(url)
        print(f'\n{"="*60}')
        print(f'文档 ID: {doc_id}')
        print(f'URL: {url}')
        print('='*60)
        if doc_id:
            get_doc_info(doc_id)
