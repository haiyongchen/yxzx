# -*- coding: utf-8 -*-
"""
OA 日志自动填写 - 直接访问日志页面
"""
from playwright.sync_api import sync_playwright
import time
import sys
import os

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
DIARY_URL = "https://oa.epoint.com.cn/wboa9/worklog/add.jsp"

# 今天的工作内容
work_content = "OA 邮件分析工具优化（飞书集成）；招投标系统支持（AI 评标异常排查）；电子商城运营（山东/武汉/新疆专区）；技能包接入测试"

print("=" * 60)
print("OA 日志自动填写工具 - 直接访问日志页面")
print("=" * 60)

try:
    playwright = sync_playwright().start()
    
    print("\n1️⃣ 启动浏览器（使用已保存的 Cookie）...")
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        channel="chrome",
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )
    
    page = context.new_page()
    
    print(f"2️⃣ 访问日志页面：{DIARY_URL}")
    page.goto(DIARY_URL, wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)
    
    # 截图查看页面
    screenshot = "diary_page.png"
    page.screenshot(path=screenshot)
    print(f"📸 页面截图已保存：{screenshot}")
    
    # 查找表单字段
    print("\n3️⃣ 查找表单字段...")
    
    # 常见的日志内容 textarea
    textarea_selectors = [
        'textarea[name="content"]',
        'textarea[name="workcontent"]',
        'textarea[name="nr"]',
        'textarea[name="rznr"]',
        'textarea[id*="content"]',
        'textarea[class*="content"]',
    ]
    
    content_field = None
    for selector in textarea_selectors:
        element = page.query_selector(selector)
        if element:
            content_field = element
            print(f"✅ 找到内容输入框：{selector}")
            break
    
    if not content_field:
        # 尝试查找所有 textarea
        textareas = page.query_selector_all('textarea')
        print(f"   找到 {len(textareas)} 个 textarea 元素")
        for i, ta in enumerate(textareas):
            name = ta.get_attribute('name') or 'no-name'
            placeholder = ta.get_attribute('placeholder') or ''
            print(f"   [{i}] name={name}, placeholder={placeholder[:50]}")
    
    # 查找提交按钮
    submit_selectors = [
        'input[type="submit"]',
        'button[type="submit"]',
        'button[class*="submit"]',
        'input[value*="提交"]',
        'button:has-text("提交")',
    ]
    
    submit_button = None
    for selector in submit_selectors:
        element = page.query_selector(selector)
        if element:
            submit_button = element
            print(f"✅ 找到提交按钮：{selector}")
            break
    
    if content_field and submit_button:
        print("\n4️⃣ 填写日志内容...")
        content_field.fill(work_content)
        time.sleep(2)
        
        print("5️⃣ 提交日志...")
        submit_button.click()
        time.sleep(5)
        
        # 检查提交结果
        if "成功" in page.content() or "提交成功" in page.content():
            print("\n🎉 日志提交成功！")
        else:
            print("\n⚠️  提交完成，请确认结果")
    else:
        print("\n⚠️  未找到完整的表单元素，请手动填写")
        print("👉 浏览器窗口保持打开，可以手动操作")
    
    # 保持窗口打开
    print("\n👉 浏览器窗口保持打开 30 秒...")
    time.sleep(30)
    
    context.close()
    playwright.stop()
    
    print("\n✅ 完成！")
    
except Exception as e:
    print(f"\n❌ 错误：{e}")
    import traceback
    traceback.print_exc()
    print("\n👉 浏览器窗口保持打开，请手动操作")
    time.sleep(60)
