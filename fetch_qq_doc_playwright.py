# -*- coding: utf-8 -*-
"""
使用 Playwright 访问腾讯文档并抓取表格数据
"""
import json
import time
from playwright.sync_api import sync_playwright

def fetch_qq_sheet(url, output_file=None):
    """使用 Playwright 访问腾讯文档并提取表格数据"""
    
    all_data = []
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        try:
            print(f"正在访问：{url}")
            page.goto(url, wait_until='networkidle', timeout=60000)
            
            # 等待表格加载
            page.wait_for_selector('table, .sheet-cell, [class*="sheet"]', timeout=30000)
            time.sleep(3)  # 额外等待数据加载
            
            # 尝试获取页面内容
            html = page.content()
            print(f"页面长度：{len(html)}")
            
            # 尝试提取表格数据 - 方法 1: 查找 table 元素
            tables = page.query_selector_all('table')
            print(f"找到 {len(tables)} 个 table 元素")
            
            for i, table in enumerate(tables[:3]):
                print(f"\n=== 表格 {i+1} ===")
                rows = table.query_selector_all('tr')
                for j, row in enumerate(rows[:20]):
                    cells = row.query_selector_all('td, th')
                    row_data = [cell.inner_text() for cell in cells]
                    if any(row_data):  # 跳过空行
                        print(f"行{j+1}: {row_data}")
                        all_data.append(row_data)
            
            # 方法 2: 尝试查找腾讯文档特定的单元格
            cells = page.query_selector_all('.sheet-cell, [class*="cell"]')
            print(f"\n找到 {len(cells)} 个单元格元素")
            
            if cells and len(cells) > 0:
                # 尝试按行组织
                grid_data = []
                for cell in cells[:100]:  # 限制前 100 个
                    text = cell.inner_text()
                    if text:
                        grid_data.append(text)
                print(f"前 100 个单元格内容：{grid_data[:30]}")
            
            # 方法 3: 尝试获取整个工作区
            sheet_area = page.query_selector('[class*="sheet"], [id*="sheet"]')
            if sheet_area:
                print(f"\n找到 sheet 区域：{sheet_area.inner_text()[:500]}")
            
            # 保存 HTML 用于分析
            if output_file:
                html_file = output_file.replace('.json', '.html')
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f"HTML 已保存到：{html_file}")
            
            return all_data
            
        except Exception as e:
            print(f"错误：{e}")
            # 保存截图
            page.screenshot(path='qq_doc_error.png')
            print("已保存错误截图")
            return None
        finally:
            browser.close()

if __name__ == '__main__':
    urls = [
        'https://docs.qq.com/sheet/DTFdkY3NqamJJVEJl?tab=1sweh3',
        'https://docs.qq.com/sheet/DQnZoWXpYQU5HVEpz?tab=BB08J2'
    ]
    
    for i, url in enumerate(urls):
        print(f"\n{'='*60}")
        print(f"处理文档 {i+1}: {url}")
        print('='*60)
        data = fetch_qq_sheet(url, output_file=f'D:\\openclaw-workspace\\qq_doc_{i+1}.json')
        if data:
            with open(f'D:\\openclaw-workspace\\qq_doc_{i+1}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到：qq_doc_{i+1}.json")
