# -*- coding: utf-8 -*-
"""
新点 OA 系统扫码登录 - 改进版（保持窗口打开）
"""
from playwright.sync_api import sync_playwright
import time
import sys
import os

# Windows UTF-8 支持
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
OA_HOME_URL = "https://oa.epoint.com.cn/wboa9/"

print("=" * 60)
print("新点 OA 系统扫码登录工具 v2.0 (窗口保持版)")
print("=" * 60)
print("\n👉 正在启动浏览器...")

try:
    playwright = sync_playwright().start()
    
    # 启动浏览器（持久化上下文）
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        channel="chrome",
        headless=False,
        args=[
            "--start-maximized",
            "--disable-blink-features=AutomationControlled"
        ]
    )
    
    page = context.new_page()
    
    print("👉 正在访问 OA 系统...")
    page.goto(OA_HOME_URL)
    time.sleep(3)
    
    # 检查是否已登录
    current_url = page.url
    if 'login' not in current_url.lower() and 'oauth2login' not in current_url.lower():
        print("\n✅ 登录状态有效！")
        print(f"   URL: {page.url}")
        print(f"   标题：{page.title()}")
        print("\n👉 浏览器窗口将保持打开 10 秒后关闭...")
        time.sleep(10)
    else:
        print("\n⚠️  需要登录")
        print("👉 浏览器窗口已打开，请在窗口中扫码登录")
        print("👉 重要：不要关闭浏览器窗口！")
        print("👉 扫码并确认登录后，脚本会自动检测...")
        print("\n⏳ 等待扫码中...（最多等待 3 分钟）\n")
        
        # 轮询检查登录状态
        max_attempts = 180
        logged_in = False
        
        for i in range(max_attempts):
            time.sleep(1)
            if i % 10 == 0:
                print(f"   等待中... ({i//10}秒)", end='\r')
            
            # 检查是否已登录
            current_url = page.url
            if 'login' not in current_url.lower() and 'oauth2login' not in current_url.lower():
                print("\n\n✅ 检测到登录成功！")
                logged_in = True
                break
        
        if logged_in:
            print("👉 正在保存登录状态...")
            # 等待 Cookie 保存到磁盘
            time.sleep(10)
            print("✅ 登录状态已保存！")
            print("\n👉 浏览器窗口将保持打开 10 秒后关闭...")
            time.sleep(10)
        else:
            print("\n\n❌ 等待超时，可能扫码未完成")
            print("👉 浏览器窗口将保持打开，请手动扫码后关闭...")
            time.sleep(60)  # 多等一会
    
    context.close()
    playwright.stop()
    print("\n✅ 完成！")
    
except Exception as e:
    print(f"\n❌ 错误：{e}")
    import traceback
    traceback.print_exc()
    input("\n按回车键退出...")
