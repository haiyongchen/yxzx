# -*- coding: utf-8 -*-
"""
解析腾讯文档 HTML 提取表格数据
"""
import re
import json
from bs4 import BeautifulSoup

def parse_qq_doc_html(html_file):
    """解析腾讯文档 HTML"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    print(f'HTML 长度：{len(html)}')
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 查找表格
    tables = soup.find_all('table')
    print(f'找到 {len(tables)} 个表格')
    
    # 查找 script 标签中的数据
    scripts = soup.find_all('script')
    print(f'找到 {len(scripts)} 个 script 标签')
    
    all_sheet_data = []
    
    # 查找包含表格数据的 script
    for i, script in enumerate(scripts):
        if script.string:
            content = script.string
            if len(content) > 1000 and ('sheet' in content.lower() or 'cell' in content.lower()):
                print(f'\nScript {i}: 长度 {len(content)}')
                
                # 尝试提取 JSON
                json_patterns = [
                    r'window\.__INITIAL_STATE__\s*=\s*({.+?});',
                    r'({\s*"sheet"[^}]+})',
                    r'({\s*"cells"[^}]+})',
                ]
                
                for pattern in json_patterns:
                    match = re.search(pattern, content, re.DOTALL)
                    if match:
                        print(f'找到 JSON 数据 (模式：{pattern[:30]}...)')
                        try:
                            data = json.loads(match.group(1))
                            with open('D:\\openclaw-workspace\\sheet_json.json', 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=2)
                            print('已保存到 sheet_json.json')
                        except Exception as e:
                            print(f'解析失败：{e}')
                        break
    
    # 提取表格内容
    print('\n=== 表格内容 ===')
    for i, table in enumerate(tables[:5]):
        print(f'\n表格 {i+1}:')
        rows = table.find_all('tr')
        print(f'  行数：{len(rows)}')
        
        for j, row in enumerate(rows[:20]):
            cells = row.find_all(['td', 'th'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            if row_data and any(row_data):
                print(f'  行{j+1}: {row_data}')
                all_sheet_data.append(row_data)
    
    return all_sheet_data

if __name__ == '__main__':
    data = parse_qq_doc_html('D:\\openclaw-workspace\\qq_doc_page.html')
    print(f'\n总共提取 {len(data)} 行数据')
