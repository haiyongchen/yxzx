# -*- coding: utf-8 -*-
"""
获取腾讯文档内容 - 尝试多种方法
"""
import requests
import json
import re

def extract_doc_id(url):
    """从腾讯文档 URL 提取文档 ID"""
    # 格式：https://docs.qq.com/sheet/Dxxxxxxxx?tab=xxxx
    match = re.search(r'/sheet/(D[a-zA-Z0-9]+)', url)
    if match:
        return match.group(1)
    return None

def fetch_qq_doc_api(doc_id):
    """尝试使用腾讯文档 API 获取数据"""
    # 腾讯文档的 API 端点
    api_url = f"https://docs.qq.com/api/doc/{doc_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'https://docs.qq.com/sheet/{doc_id}',
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        print(f"API 响应状态码：{response.status_code}")
        print(f"API 响应内容：{response.text[:500]}")
        return response.text
    except Exception as e:
        print(f"API 请求失败：{e}")
        return None

def fetch_qq_doc_export(doc_id):
    """尝试导出为 Excel"""
    export_url = f"https://docs.qq.com/api/export/sheet/{doc_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    try:
        response = requests.get(export_url, headers=headers, timeout=30)
        print(f"导出响应状态码：{response.status_code}")
        if response.status_code == 200:
            # 保存为 Excel 文件
            output_file = f"D:\\openclaw-workspace\\{doc_id}.xlsx"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"已保存到：{output_file}")
            return output_file
        return None
    except Exception as e:
        print(f"导出失败：{e}")
        return None

if __name__ == '__main__':
    urls = [
        'https://docs.qq.com/sheet/DTFdkY3NqamJJVEJl?tab=1sweh3',
        'https://docs.qq.com/sheet/DQnZoWXpYQU5HVEpz?tab=BB08J2'
    ]
    
    for url in urls:
        print(f"\n{'='*60}")
        print(f"处理：{url}")
        print('='*60)
        
        doc_id = extract_doc_id(url)
        print(f"文档 ID: {doc_id}")
        
        if doc_id:
            # 尝试 API
            print("\n尝试 API 获取...")
            fetch_qq_doc_api(doc_id)
            
            # 尝试导出
            print("\n尝试导出 Excel...")
            fetch_qq_doc_export(doc_id)
