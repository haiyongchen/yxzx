# -*- utf-8 -*-
"""
OA 邮件阅读总结工具 - 简化版
"""
import sys
import os
import time
from datetime import datetime

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
OA_MAIL_URL = "https://oa.epoint.com.cn:8080/OA9/oa9/mail/mailframe"

print("=" * 60)
print("OA 邮件阅读工具")
print("=" * 60)

playwright = sync_playwright().start()

print("\n👉 启动浏览器...")
context = playwright.chromium.launch_persistent_context(
    user_data_dir=USER_DATA_DIR,
    channel="chrome",
    headless=False,
    args=["--disable-blink-features=AutomationControlled"]
)

page = context.new_page()

print(f"👉 访问：{OA_MAIL_URL}")
page.goto(OA_MAIL_URL, wait_until='networkidle', timeout=30000)
time.sleep(3)

# 检查登录
if 'login' in page.url.lower():
    print("\n⚠️  需要扫码，请在浏览器中扫码后按回车...")
    input()
    time.sleep(3)

print(f"\n✅ 当前页面：{page.title()}")
print(f"   URL: {page.url}")

# 截图
page.screenshot(path='mail_test.png')
print("\n📸 已保存截图：mail_test.png")

# 获取 iframe
print("\n👉 尝试获取邮件列表...")
time.sleep(2)

try:
    # 方法 1: frame_locator
    frame = page.frame_locator('#mail-rightframe')
    
    # 获取所有文本
    body = frame.locator('body').inner_text(timeout=5000)
    lines = [l.strip() for l in body.split('\n') if l.strip()]
    
    print(f"\n📄 iframe 内容 ({len(lines)} 行):")
    for i, line in enumerate(lines[:50]):
        print(f"  [{i}] {line[:100]}")
    
except Exception as e:
    print(f"❌ 失败：{e}")
    
    # 方法 2: 直接获取页面
    print("\n👉 尝试获取主页面内容...")
    try:
        body = page.locator('body').inner_text(timeout=5000)
        lines = [l.strip() for l in body.split('\n') if l.strip()]
        print(f"\n📄 主页面内容 ({len(lines)} 行):")
        for i, line in enumerate(lines[:50]):
            print(f"  [{i}] {line[:100]}")
    except Exception as e2:
        print(f"❌ 也失败了：{e2}")

print("\n✅ 完成，按回车退出...")
input()

context.close()
playwright.stop()
