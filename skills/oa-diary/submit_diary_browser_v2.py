# -*- coding: utf-8 -*-
"""
OA 日志自动填写 - 浏览器自动化最终版
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
print("OA 日志自动填写工具 - 浏览器自动化最终版")
print("=" * 60)

try:
    playwright = sync_playwright().start()
    
    print("\n1️⃣ 启动浏览器（使用已保存的 Cookie）...")
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        channel="chrome",
        headless=False,  # 显示窗口
        args=["--disable-blink-features=AutomationControlled"]
    )
    
    page = context.new_page()
    
    print(f"2️⃣ 访问日志页面：{DIARY_URL}")
    page.goto(DIARY_URL, wait_until='networkidle', timeout=60000)
    time.sleep(10)  # 等待页面完全加载
    
    print("3️⃣ 查找输入框...")
    
    # 尝试多种可能的输入框选择器
    selectors = [
        'textarea[name="content"]',
        'textarea[name="workcontent"]', 
        'textarea[name="nr"]',
        'textarea[name="rznr"]',
        'textarea[id="content"]',
        'textarea[class*="content"]',
        '.ueditor-container textarea',
        '.kindeditor textarea',
        '[contenteditable="true"]',
        'iframe',
    ]
    
    found_element = None
    for selector in selectors:
        try:
            elements = page.query_selector_all(selector)
            if elements:
                print(f"✅ 找到：{selector} ({len(elements)} 个)")
                found_element = elements[0]
                break
        except:
            pass
    
    # 如果没找到，尝试查找所有 iframe 并在 iframe 内查找
    if not found_element:
        print("   尝试在 iframe 内查找...")
        frames = page.frames
        for i, frame in enumerate(frames):
            try:
                textareas = frame.query_selector_all('textarea')
                if textareas:
                    print(f"✅ 在 frame[{i}] 中找到 {len(textareas)} 个 textarea")
                    found_element = textareas[0]
                    break
            except:
                pass
    
    # 如果还是没找到，使用 JavaScript 查找
    if not found_element:
        print("   使用 JavaScript 查找...")
        found_element = page.evaluate("""
            () => {
                // 查找所有 textarea
                const textareas = document.querySelectorAll('textarea');
                if (textareas.length > 0) {
                    return textareas[0].name || textareas[0].id || 'textarea';
                }
                // 查找可编辑区域
                const editable = document.querySelector('[contenteditable="true"]');
                if (editable) {
                    return 'contenteditable';
                }
                return null;
            }
        """)
        print(f"   JavaScript 找到：{found_element}")
    
    if found_element:
        print("\n4️⃣ 填写日志内容...")
        
        # 如果是普通 textarea
        if hasattr(found_element, 'fill'):
            found_element.fill(work_content)
        # 如果是 contenteditable 区域
        elif hasattr(found_element, 'type'):
            found_element.type(work_content)
        
        time.sleep(3)
        
        # 查找提交按钮
        print("5️⃣ 查找提交按钮...")
        submit_selectors = [
            'input[type="submit"]',
            'button[type="submit"]',
            'button[class*="submit"]',
            'input[value*="提交"]',
            'button:has-text("提交")',
            'button:has-text("保存")',
        ]
        
        submit_button = None
        for selector in submit_selectors:
            try:
                elements = page.query_selector_all(selector)
                if elements:
                    print(f"✅ 找到提交按钮：{selector}")
                    submit_button = elements[0]
                    break
            except:
                pass
        
        if submit_button:
            print("6️⃣ 提交日志...")
            submit_button.click()
            time.sleep(5)
            
            # 检查提交结果
            if "成功" in page.content() or "提交成功" in page.content():
                print("\n🎉 日志提交成功！")
            else:
                print("\n⚠️  已点击提交，请确认结果")
        else:
            print("\n⚠️  未找到提交按钮，请手动点击")
    else:
        print("\n⚠️  未找到输入框，请手动填写")
    
    print("\n👉 浏览器窗口保持打开 60 秒...")
    print("   可以手动操作或查看页面结构")
    time.sleep(60)
    
    context.close()
    playwright.stop()
    
    print("\n✅ 完成！")
    
except Exception as e:
    print(f"\n❌ 错误：{e}")
    import traceback
    traceback.print_exc()
    print("\n👉 浏览器窗口保持打开，请手动操作")
    time.sleep(60)
