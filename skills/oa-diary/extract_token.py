# -*- coding: utf-8 -*-
"""
从浏览器 Cookie 提取 OA Token 并保存
"""
from playwright.sync_api import sync_playwright
import time
import sys
import os

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
TOKEN_FILE = r"D:\openclaw-workspace\skills\oa-diary\oa\access_token.txt"

print("=" * 60)
print("从浏览器 Cookie 提取 OA Token")
print("=" * 60)

try:
    playwright = sync_playwright().start()
    
    print("\n1️⃣ 启动浏览器（使用已保存的 Cookie）...")
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        channel="chrome",
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    
    page = context.new_page()
    
    print("2️⃣ 访问 OA 系统...")
    page.goto("https://oa.epoint.com.cn/wboa9/", wait_until='networkidle', timeout=30000)
    time.sleep(5)
    
    # 提取 Cookie
    print("3️⃣ 提取 access_token Cookie...")
    cookies = context.cookies()
    access_token = None
    
    for cookie in cookies:
        if cookie.get('name') == 'access_token':
            access_token = cookie.get('value')
            break
    
    # 如果 Cookie 中没有，尝试从 localStorage 获取
    if not access_token:
        access_token = page.evaluate("localStorage.getItem('access_token')")
    
    context.close()
    playwright.stop()
    
    if not access_token:
        print("\n❌ 未找到 access_token")
        sys.exit(1)
    
    print(f"✅ 获取到 access_token: {access_token[:30]}...")
    
    # 保存 Token
    print(f"\n4️⃣ 保存 Token 到：{TOKEN_FILE}")
    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
    with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
        f.write(f"access_token={access_token}\n")
    
    print("✅ Token 已保存！")
    print("\n🎉 现在可以使用 oa_api.py 提交日志了！")
    
except Exception as e:
    print(f"\n❌ 错误：{e}")
    import traceback
    traceback.print_exc()
