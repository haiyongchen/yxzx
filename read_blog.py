# -*- coding: utf-8 -*-
"""
用 Playwright 打开博客并获取内容
"""

from playwright.sync_api import sync_playwright
import time

URL = "https://post.smzdm.com/p/aqm9n22p/"

with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    
    # 访问页面
    print(f"访问：{URL}")
    page.goto(URL, timeout=60000, wait_until="networkidle")
    time.sleep(5)
    
    # 获取页面内容
    title = page.title()
    print(f"\n标题：{title}")
    
    # 获取正文内容
    content = page.inner_text('body')
    
    # 保存内容
    with open('output/blog_content.txt', 'w', encoding='utf-8') as f:
        f.write(f"标题：{title}\n")
        f.write(f"URL: {URL}\n")
        f.write(f"获取时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        f.write(content)
    
    print(f"\n内容长度：{len(content)} 字符")
    print(f"\n已保存：output/blog_content.txt")
    
    # 截图
    page.screenshot(path='output/blog_screenshot.png', full_page=True)
    print(f"截图：output/blog_screenshot.png")
    
    browser.close()
