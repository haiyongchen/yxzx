# -*- coding: utf-8 -*-
"""
尝试通过腾讯文档 CDN 获取表格数据
"""
import requests
import json

def fetch_sheet_data(doc_id, tab_id=None):
    """尝试从腾讯文档获取表格数据"""
    
    # 尝试多种 API 端点
    endpoints = [
        f"https://docs.qq.com/api/doc/{doc_id}",
        f"https://docs.qq.com/api/tabs/{doc_id}",
        f"https://docs.qq.com/api/sheet/{doc_id}/content",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Referer': f'https://docs.qq.com/sheet/{doc_id}',
    }
    
    for endpoint in endpoints:
        try:
            print(f"\n尝试：{endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"状态码：{response.status_code}")
            if response.status_code == 200:
                content = response.text[:1000]
                print(f"内容：{content}")
                return response.text
        except Exception as e:
            print(f"失败：{e}")
            continue
    
    return None

if __name__ == '__main__':
    docs = [
        ('DTFdkY3NqamJJVEJl', '1sweh3'),  # 01-新点电子交易专区&项目跟进表（重要）
        ('DQnZoWXpYQU5HVEpz', 'BB08J2'),  # 另一个文档
    ]
    
    for doc_id, tab_id in docs:
        print(f"\n{'='*60}")
        print(f"文档 ID: {doc_id}, Tab: {tab_id}")
        print('='*60)
        fetch_sheet_data(doc_id, tab_id)
