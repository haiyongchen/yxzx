# -*- coding: utf-8 -*-
"""
用 Playwright 打开博客 v3 - 处理验证码
"""

from playwright.sync_api import sync_playwright
import time

URL = "https://post.smzdm.com/p/aqm9n22p/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    
    print(f"访问：{URL}")
    page.goto(URL, timeout=60000)
    
    # 等待页面加载
    print("\n等待页面加载（60 秒）...")
    print("[提示] 如果有拼图验证，请手动完成")
    
    # 等待 60 秒，给用户时间完成验证
    for i in range(60):
        try:
            # 检查是否有内容
            content_elem = page.query_selector('article, .article-content, .content')
            if content_elem:
                content = content_elem.inner_text()
                if len(content) > 500:
                    print(f"\n[OK] 检测到内容：{len(content)} 字符")
                    break
        except:
            pass
        
        # 每秒检查一次
        time.sleep(1)
        if (i + 1) % 10 == 0:
            print(f"  已等待 {i+1} 秒...")
    
    # 获取标题
    title = page.title()
    print(f"\n标题：{title}")
    
    # 获取内容
    content_elem = page.query_selector('article')
    if content_elem:
        content = content_elem.inner_text()
    else:
        # 尝试获取所有段落
        paragraphs = page.query_selector_all('p')
        content = '\n'.join([p.inner_text() for p in paragraphs[:50]])
    
    print(f"\n内容长度：{len(content)} 字符")
    
    # 保存
    with open('output/blog_content_v3.txt', 'w', encoding='utf-8') as f:
        f.write(f"标题：{title}\n")
        f.write(f"URL: {URL}\n")
        f.write(f"获取时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        f.write(content[:15000])
    
    print(f"\n已保存：output/blog_content_v3.txt")
    
    # 截图
    page.screenshot(path='output/blog_screenshot_v3.png', full_page=True)
    print(f"截图：output/blog_screenshot_v3.png")
    
    # 打印内容
    print("\n" + "=" * 80)
    print("[博客内容]")
    print("=" * 80)
    print(content[:2000])
    
    browser.close()
    print("\n[完成]")
