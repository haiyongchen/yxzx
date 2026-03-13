# -*- coding: utf-8 -*-
"""
用 Playwright 打开博客 v2 - 等待动态内容
"""

from playwright.sync_api import sync_playwright
import time

URL = "https://post.smzdm.com/p/aqm9n22p/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    
    print(f"访问：{URL}")
    page.goto(URL, timeout=60000)
    
    # 等待页面加载
    print("等待页面加载...")
    time.sleep(10)
    
    # 尝试滚动页面触发加载
    print("滚动页面...")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(2)
    
    # 获取标题
    title = page.title()
    print(f"\n标题：{title}")
    
    # 获取文章内容
    print("\n查找文章内容...")
    
    # 尝试多种选择器
    selectors = [
        'article',
        '.article-content',
        '.content',
        '[class*="article"]',
        '[class*="content"]',
        '#content',
    ]
    
    content = ""
    for selector in selectors:
        elem = page.query_selector(selector)
        if elem:
            content = elem.inner_text()
            print(f"[OK] 找到内容：{selector} - {len(content)} 字符")
            break
    
    if not content:
        # 获取整个页面文本
        content = page.inner_text('body')
        print(f"[INFO] 获取整个页面：{len(content)} 字符")
    
    # 保存
    with open('output/blog_content_v2.txt', 'w', encoding='utf-8') as f:
        f.write(f"标题：{title}\n")
        f.write(f"URL: {URL}\n")
        f.write(f"获取时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        f.write(content[:10000])  # 限制长度
    
    print(f"\n已保存：output/blog_content_v2.txt")
    
    # 截图
    page.screenshot(path='output/blog_screenshot_v2.png', full_page=True)
    print(f"截图：output/blog_screenshot_v2.png")
    
    # 打印前 500 字符
    print("\n" + "=" * 80)
    print("[内容预览]")
    print("=" * 80)
    print(content[:1000])
    
    browser.close()
