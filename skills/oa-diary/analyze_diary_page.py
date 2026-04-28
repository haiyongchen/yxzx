# -*- coding: utf-8 -*-
"""
分析 OA 日志页面结构
"""
from playwright.sync_api import sync_playwright
import time
import sys
import os
import json

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
DIARY_URL = "https://oa.epoint.com.cn/wboa9/worklog/add.jsp"

try:
    playwright = sync_playwright().start()
    
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        channel="chrome",
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    
    page = context.new_page()
    page.goto(DIARY_URL, wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)
    
    # 获取页面 HTML 结构
    html = page.content()
    
    # 分析页面元素
    print("=" * 60)
    print("OA 日志页面结构分析")
    print("=" * 60)
    
    # 查找所有输入元素
    inputs = page.query_selector_all('input, textarea, button, select')
    print(f"\n找到 {len(inputs)} 个表单元素：\n")
    
    for i, el in enumerate(inputs[:50]):  # 最多显示 50 个
        tag = el.tag_name()
        name = el.get_attribute('name') or 'no-name'
        id_attr = el.get_attribute('id') or ''
        type_attr = el.get_attribute('type') or ''
        class_attr = el.get_attribute('class') or ''[:50]
        placeholder = el.get_attribute('placeholder') or ''[:50]
        value = el.input_value()[:50] if tag == 'input' and el.input_value() else ''
        
        print(f"[{i:2d}] {tag:8s} name={name:30s} type={type_attr:10s} id={id_attr[:30]}")
    
    # 检查 iframe
    frames = page.frames
    print(f"\n\n找到 {len(frames)} 个 frame/iframe：\n")
    for i, frame in enumerate(frames):
        print(f"[{i}] {frame.url[:100]}")
        
        # 查找 frame 内的输入元素
        try:
            frame_inputs = frame.query_selector_all('input, textarea')
            if frame_inputs:
                print(f"    包含 {len(frame_inputs)} 个输入元素")
                for fi in frame_inputs[:5]:
                    name = fi.get_attribute('name') or 'no-name'
                    print(f"      - {name}")
        except:
            pass
    
    # 保存页面 HTML
    with open('diary_page_source.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\n\n✅ 页面 HTML 已保存：diary_page_source.html")
    
    context.close()
    playwright.stop()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
