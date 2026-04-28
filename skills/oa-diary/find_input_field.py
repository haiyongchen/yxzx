# -*- coding: utf-8 -*-
"""
分析 OA 日志页面结构 - 详细版
"""
from playwright.sync_api import sync_playwright
import time
import sys
import os

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\OAuto\oa_user_data"
DIARY_URL = "https://oa.epoint.com.cn/wboa9/worklog/add.jsp"

try:
    playwright = sync_playwright().start()
    
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        channel="chrome",
        headless=False,  # 显示窗口
        args=["--disable-blink-features=AutomationControlled"]
    )
    
    page = context.new_page()
    
    print("正在访问日志页面...")
    page.goto(DIARY_URL, wait_until='networkidle', timeout=60000)
    time.sleep(10)  # 等待 JavaScript 执行
    
    print("页面已加载，正在分析...")
    
    # 获取页面标题和 URL
    print(f"\n页面标题：{page.title()}")
    print(f"页面 URL: {page.url}")
    
    # 查找所有可能的输入区域
    selectors_to_try = [
        '#content', '#workcontent', '#rznr', '#nr',
        '[name="content"]', '[name="workcontent"]', '[name="rznr"]',
        '.content', '.workcontent', '.editor',
        'iframe', 'frame',
        '.ueditor', '.kindeditor', '.tinymce',  # 常见富文本编辑器
        '[contenteditable="true"]',  # 可编辑区域
    ]
    
    print("\n查找可能的输入区域：")
    for selector in selectors_to_try:
        try:
            elements = page.query_selector_all(selector)
            if elements:
                print(f"✅ {selector}: 找到 {len(elements)} 个元素")
                for i, el in enumerate(elements[:3]):
                    tag = el.tag_name()
                    text = el.inner_text()[:100] if tag != 'input' else el.input_value()[:100]
                    print(f"   [{i}] tag={tag}, text={text[:50]}...")
        except Exception as e:
            pass
    
    # 截图
    page.screenshot(path='diary_page_full.png', full_page=True)
    print("\n📸 页面截图已保存：diary_page_full.png")
    
    print("\n👉 浏览器窗口保持打开，请查看页面结构")
    print("   告诉我日志内容输入框的特征，我可以自动填写")
    
    # 保持窗口打开 2 分钟
    time.sleep(120)
    
    context.close()
    playwright.stop()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
    time.sleep(60)
