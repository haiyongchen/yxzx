# -*- coding: utf-8 -*-
"""
OA 日志自动填写 - 浏览器自动化
"""
from playwright.sync_api import sync_playwright
import time
import sys
import os

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"

# 今天的工作内容
work_content = "OA 邮件分析工具优化（飞书集成）；招投标系统支持（AI 评标异常排查）；电子商城运营（山东/武汉/新疆专区）；技能包接入测试"

print("=" * 60)
print("OA 日志自动填写工具 - 浏览器自动化版")
print("=" * 60)

try:
    playwright = sync_playwright().start()
    
    # 使用已保存的 Cookie 启动浏览器
    print("\n1️⃣ 启动浏览器（使用已保存的 Cookie）...")
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        channel="chrome",
        headless=False,  # 显示窗口，方便调试
        args=["--disable-blink-features=AutomationControlled"]
    )
    
    page = context.new_page()
    
    # 尝试访问日志页面
    print("2️⃣ 访问 OA 日志系统...")
    
    # 常见的日志页面 URL 尝试
    diary_urls = [
        "https://oa.epoint.com.cn/oaextend/pages/rz/rzadd.html",  # 日志添加
        "https://oa.epoint.com.cn/wboa9/rz/rzadd.jsp",
        "https://oa.epoint.com.cn/oa9/worklog/logAdd.jsp",
        "https://oa.epoint.com.cn/wboa9/worklog/add.jsp",
    ]
    
    found = False
    for url in diary_urls:
        try:
            print(f"   尝试：{url}")
            page.goto(url, wait_until='domcontentloaded', timeout=10000)
            time.sleep(3)
            
            # 检查是否在日志页面（查找表单元素）
            if page.query_selector('textarea[name*="content"], textarea[name*="nr"], input[name*="title"]'):
                print(f"✅ 找到日志填写页面：{url}")
                found = True
                break
        except Exception as e:
            continue
    
    if not found:
        print("\n❌ 未找到日志填写页面")
        print("👉 请提供日志填写页面的 URL")
        
        # 打开 OA 首页，让用户手动导航
        print("\n👉 打开 OA 首页，请手动导航到日志页面...")
        page.goto("https://oa.epoint.com.cn/wboa9/")
        time.sleep(5)
    
    print("\n👉 浏览器窗口已打开")
    print("   如果已找到日志页面，将自动填写")
    print("   否则请手动导航到日志页面后告诉我")
    
    # 保持浏览器打开
    time.sleep(60)
    
    context.close()
    playwright.stop()
    
    print("\n✅ 完成！")
    
except Exception as e:
    print(f"\n❌ 错误：{e}")
    import traceback
    traceback.print_exc()
