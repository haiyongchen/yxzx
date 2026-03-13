# -*- coding: utf-8 -*-
"""
从腾讯文档 HTML 中提取 JSON 数据
"""
import re
import json

def extract_json_from_html(html_file):
    """从 HTML 中提取 JSON 数据"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 查找所有可能的 JSON 数据
    patterns = [
        (r'window\.__INITIAL_STATE__\s*=\s*({.+?});\s*</script>', 'INITIAL_STATE'),
        (r'window\.__SSR_STATE__\s*=\s*({.+?});\s*</script>', 'SSR_STATE'),
        (r'({\s*"sheetConfig"[^}]+})', 'sheetConfig'),
        (r'({\s*"cellData"[^}]+})', 'cellData'),
        (r'(\\[{[^}]*"row"[^}]*}\\])', 'rows'),
    ]
    
    for pattern, name in patterns:
        matches = re.findall(pattern, html, re.DOTALL)
        if matches:
            print(f'\n找到 {name}: {len(matches)} 个匹配')
            for i, match in enumerate(matches[:3]):
                print(f'  匹配{i+1} 长度：{len(match)}')
                # 尝试解析 JSON
                try:
                    # 清理 JSON
                    json_str = match
                    if isinstance(json_str, bytes):
                        json_str = json_str.decode('utf-8')
                    data = json.loads(json_str)
                    
                    # 保存
                    out_file = f'D:\\openclaw-workspace\\{name}_{i}.json'
                    with open(out_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    print(f'  已保存到：{out_file}')
                except Exception as e:
                    print(f'  解析失败：{e}')
    
    # 查找所有 JSON 对象
    print('\n=== 查找大型 JSON 对象 ===')
    json_like = re.findall(r'{[^{}]{1000,}}', html)
    print(f'找到 {len(json_like)} 个大型 JSON 样式的对象')
    
    for i, j in enumerate(json_like[:5]):
        print(f'\nJSON 样本 {i+1} (前 500 字符):')
        print(j[:500])
        
        # 尝试解析
        try:
            data = json.loads(j)
            out_file = f'D:\\openclaw-workspace\\json_sample_{i}.json'
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'  解析成功，保存到：{out_file}')
        except Exception as e:
            print(f'  解析失败：{e}')

if __name__ == '__main__':
    extract_json_from_html('D:\\openclaw-workspace\\qq_doc_page.html')
