# -*- coding: utf-8 -*-
"""
直接请求腾讯文档 API
"""
import requests
import json
import re

def fetch_qq_doc_direct(url):
    """直接请求腾讯文档"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        print(f"访问：{url}")
        response = session.get(url, timeout=30, allow_redirects=True)
        print(f"状态码：{response.status_code}")
        print(f"响应长度：{len(response.text)}")
        
        # 保存 HTML
        html_file = 'D:\\openclaw-workspace\\qq_doc_page.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"HTML 已保存到：{html_file}")
        
        # 检查是否需要登录
        if '登录' in response.text or 'login' in response.text.lower():
            print("⚠️ 页面需要登录")
        else:
            print("✓ 页面可能无需登录")
        
        # 尝试提取表格数据
        content = response.text
        
        # 查找 JSON 数据（腾讯文档可能将数据嵌入 JSON）
        json_matches = re.findall(r'window\.__INITIAL_STATE__\s*=\s*({.+?});', content, re.DOTALL)
        if json_matches:
            print(f"\n找到初始状态 JSON，长度：{len(json_matches[0])}")
            try:
                data = json.loads(json_matches[0])
                json_file = 'D:\\openclaw-workspace\\qq_doc_data.json'
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"JSON 数据已保存到：{json_file}")
            except Exception as e:
                print(f"解析 JSON 失败：{e}")
        
        # 查找表格相关数据
        table_matches = re.findall(r'"cells":\s*(\[[^\]]+\])', content)
        if table_matches:
            print(f"\n找到 {len(table_matches)} 个单元格数据")
            for i, match in enumerate(table_matches[:3]):
                print(f"数据{i+1}: {match[:200]}...")
        
        return response.text
        
    except Exception as e:
        print(f"请求失败：{e}")
        return None

if __name__ == '__main__':
    urls = [
        'https://docs.qq.com/sheet/DTFdkY3NqamJJVEJl?tab=1sweh3',
        'https://docs.qq.com/sheet/DQnZoWXpYQU5HVEpz?tab=BB08J2'
    ]
    
    for url in urls:
        print(f"\n{'='*60}")
        fetch_qq_doc_direct(url)
