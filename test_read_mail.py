# -*- utf-8 -*-
"""
测试打开单封邮件阅读内容
"""
import sys
import os
import time

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
OA_MAIL_URL = "https://oa.epoint.com.cn:8080/OA9/oa9/mail/mailframe"

print("=" * 60)
print("测试打开邮件内容")
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
    print("\n⚠️  需要扫码")
    input()
    time.sleep(3)

print(f"\n✅ 登录成功：{page.title()}")

# 获取 iframe
print("\n👉 获取邮件列表...")
time.sleep(2)

frame = page.frame_locator('#mail-rightframe')
body_text = frame.locator('body').inner_text(timeout=5000)
lines = [l.strip() for l in body_text.split('\n') if l.strip()]

print(f"\n📄 邮件列表 ({len(lines)} 行):")
for i, line in enumerate(lines[:30]):
    print(f"  [{i}] {line}")

# 找到第一封有效邮件
print("\n👉 尝试打开第一封邮件...")

# 过滤出有效邮件行
mail_lines = []
for i, line in enumerate(lines):
    if len(line) > 5 and not any(kw in line for kw in ['全选', '转移', '签收', '删除', '本周', '更早', '每页', '条', '关键字', '搜索', '返回']):
        mail_lines.append((i, line))

print(f"\n找到 {len(mail_lines)} 个有效邮件行")
for idx, (line_num, text) in enumerate(mail_lines[:5]):
    print(f"  [{idx}] 行{line_num}: {text[:60]}")

# 点击第一封邮件的主题
if mail_lines:
    # 找到第一封邮件的主题行（通常是第 2 个有效行）
    target_line = mail_lines[1][1]  # 第二封（跳过"本周 XX 封"）
    print(f"\n👉 点击邮件：{target_line[:50]}...")
    
    try:
        # 在 iframe 中查找并点击
        mail_row = frame.get_by_text(target_line[:30], exact=False).first
        mail_row.click(timeout=5000)
        
        print("✅ 点击成功，等待加载...")
        time.sleep(3)
        
        # 获取邮件详情页面内容
        print("\n📖 获取邮件内容...")
        detail_text = frame.locator('body').inner_text(timeout=5000)
        detail_lines = [l.strip() for l in detail_text.split('\n') if l.strip()]
        
        print(f"\n📄 邮件详情页 ({len(detail_lines)} 行):")
        for i, line in enumerate(detail_lines[:80]):
            print(f"  [{i}] {line[:120]}")
        
        # 保存完整内容
        with open('mail_content_test.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(detail_lines))
        print("\n💾 已保存完整内容：mail_content_test.txt")
        
    except Exception as e:
        print(f"❌ 点击失败：{e}")
        # 截图
        page.screenshot(path='mail_click_fail.png')
        print("📸 已保存截图：mail_click_fail.png")

print("\n✅ 完成，按回车退出...")
input()

context.close()
playwright.stop()
