# -*- coding: utf-8 -*-
"""
从腾讯文档 HTML 中提取表格单元格数据
"""
import re
import json

def extract_cells(html_file):
    """提取单元格数据"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 查找包含 "cells" 或 "row" 的 script 标签
    script_pattern = r'<script[^>]*>(.+?)</script>'
    scripts = re.findall(script_pattern, html, re.DOTALL)
    
    print(f'找到 {len(scripts)} 个 script 标签')
    
    for i, script in enumerate(scripts):
        if len(script) < 500:
            continue
            
        # 查找单元格相关数据
        if 'cells' in script.lower() or '"row"' in script.lower() or 'sheetData' in script.lower():
            print(f'\n=== Script {i} (长度：{len(script)}) ===')
            
            # 提取包含 row/cell 的 JSON 数组
            # 模式 1: 查找数组格式的行数据
            row_pattern = r'\[\s*\[[^\]]+\][^\]]*\]'
            rows = re.findall(row_pattern, script)
            
            if rows:
                print(f'找到 {len(rows)} 个可能的行数据')
                for j, row in enumerate(rows[:20]):
                    # 清理并解析
                    try:
                        # 移除转义
                        clean_row = row.replace('\\', '')
                        data = json.loads(clean_row)
                        if isinstance(data, list) and len(data) > 0:
                            print(f'  行{j+1}: {data}')
                    except:
                        # 尝试直接提取文本
                        texts = re.findall(r'"([^"]+)"', row)
                        if texts and len(texts) > 1:
                            print(f'  行{j+1} 文本：{texts[:10]}')
            
            # 查找特定的数据结构
            # 腾讯文档可能使用 {r: row, c: col, v: value} 格式
            cell_pattern = r'\{[^}]*"r"[^}]*"c"[^}]*\}'
            cells = re.findall(cell_pattern, script)
            if cells:
                print(f'\n找到 {len(cells)} 个单元格对象')
                for cell in cells[:10]:
                    print(f'  {cell}')
    
    # 搜索整个 HTML 查找表格数据模式
    print('\n=== 搜索整个 HTML ===')
    
    # 查找类似 [[...],[...]] 的二维数组
    array_2d = re.findall(r'\[\s*\[\s*"[^"]+"\s*,', html)
    print(f'找到 {len(array_2d)} 个二维数组起始模式')
    
    # 查找包含中文的数组
    chinese_array = re.findall(r'\[[^\]]*[\u4e00-\u9fa5][^\]]*\]', html)
    print(f'找到 {len(chinese_array)} 个包含中文的数组')
    
    for arr in chinese_array[:20]:
        if len(arr) < 200:  # 短数组
            print(f'  {arr}')

if __name__ == '__main__':
    extract_cells('D:\\openclaw-workspace\\qq_doc_page.html')
