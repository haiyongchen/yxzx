# -*- coding: utf-8 -*-
"""
测试 OA 登录状态是否可以复用
"""
from playwright.sync_api import sync_playwright
import time

print("=" * 60)
print("测试 OA 登录状态复用")
print("=" * 60)

with sync_playwright() as p:
    # 使用持久化上下文（复用已保存的登录状态）
    context = p.chromium.launch_persistent_context(
        user_data_dir="oa_user_data",
        channel="msedge",
        headless=False,
        args=[
            "--start-maximized",
            "--disable-blink-features=AutomationControlled"
        ]
    )
    
    page = context.new_page()
    
    print("\n👉 正在访问 OA 系统...")
    page.goto("https://oa.epoint.com.cn/wboa9/")
    
    # 等待页面加载
    print("👉 等待页面加载...")
    time.sleep(5)
    
    current_url = page.url
    title = page.title()
    
    print(f"\n当前 URL: {current_url}")
    print(f"页面标题: {title}")
    
    # 判断是否已登录
    if "login" in current_url.lower() or "登录" in title or "oauth2login" in current_url.lower():
        print("\n❌ 未检测到登录状态，需要重新登录")
        print("\n可能的原因：")
        print("1. 登录状态已过期")
        print("2. OA 系统使用 SSO，session 有效期较短")
        print("3. 需要保持浏览器运行更长时间来保存状态")
    else:
        print("\n✅ 登录状态有效！无需重新登录")
    
    print("\n👉 保持浏览器运行 10 秒，请查看页面状态...")
    time.sleep(10)
    
    # 再次检查
    print(f"\n最终 URL: {page.url}")
    print(f"最终标题: {page.title()}")
    
    context.close()
    
print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
