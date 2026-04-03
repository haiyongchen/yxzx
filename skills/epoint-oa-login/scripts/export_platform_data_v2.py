# -*- coding: utf-8 -*-
"""
导出平台数据脚本 V2
使用更精确的定位方式
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright, expect

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\OAuto\oa_user_data"
TARGET_URL = "https://dui.epoint.com.cn/transferplatform/pages/transferplatform/yfw/strategicmaplist"


def export_platform_data():
    """导出平台数据"""
    print("=" * 60)
    print("导出平台数据 - V2")
    print("=" * 60)
    
    with sync_playwright() as p:
        print("\n👉 正在启动浏览器...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            channel="chrome",
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        
        page = context.new_page()
        
        print(f"👉 正在访问: {TARGET_URL}")
        page.goto(TARGET_URL)
        
        print("👉 等待页面加载...")
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        # 检查是否需要登录
        current_url = page.url
        if 'login' in current_url.lower() or 'oauth2login' in current_url.lower():
            print("\n⚠️ 需要登录，请在浏览器窗口中扫码登录")
            print("👉 登录完成后，按回车键继续...")
            input()
            time.sleep(3)
        
        print(f"\n✅ 页面已加载: {page.title()}")
        
        try:
            # 1. 去除月份搜索条件
            print("\n👉 步骤1: 去除月份搜索条件...")
            
            # 查找月份输入框（通常在"月:"标签后面）
            # 尝试多种方式定位
            month_input = None
            
            # 方式1: 通过 placeholder
            try:
                month_input = page.locator('input[placeholder="选择月份"], input[placeholder*="月"]').first
                if month_input.is_visible():
                    print("   找到月份输入框 (placeholder)")
            except:
                pass
            
            # 方式2: 通过标签文本"月"查找相邻的输入框
            if not month_input:
                try:
                    # 查找包含"月"的标签，然后找相邻的输入框
                    month_label = page.locator('text=月:').first
                    if month_label.is_visible():
                        # 找到父元素，然后找 input
                        parent = month_label.locator('..')
                        month_input = parent.locator('input').first
                        print("   找到月份输入框 (通过标签)")
                except:
                    pass
            
            # 方式3: 查找所有日期/月份类型的输入框
            if not month_input:
                try:
                    inputs = page.locator('input[type="text"]').all()
                    for i, inp in enumerate(inputs):
                        if inp.is_visible():
                            # 检查是否是月份选择器
                            try:
                                placeholder = inp.get_attribute('placeholder') or ''
                                if '月' in placeholder or 'month' in placeholder.lower():
                                    month_input = inp
                                    print(f"   找到月份输入框 (第{i+1}个输入框)")
                                    break
                            except:
                                continue
                except:
                    pass
            
            # 清除月份条件
            if month_input and month_input.is_visible():
                month_input.click()
                time.sleep(1)
                
                # 尝试点击清除按钮
                try:
                    clear_btn = page.locator('.el-input__clear, .el-icon-circle-close, .clear-icon').first
                    if clear_btn.is_visible():
                        clear_btn.click()
                        print("   ✅ 已清除月份条件")
                    else:
                        # 按 Delete 或 Backspace 清除
                        month_input.press('Control+a')
                        month_input.press('Delete')
                        print("   ✅ 已清除月份条件 (键盘)")
                except:
                    page.keyboard.press('Escape')
                    print("   ⚠️ 未能清除月份条件")
            else:
                print("   ⚠️ 未找到月份输入框")
            
            time.sleep(2)
            
            # 2. 点击搜索按钮
            print("\n👉 步骤2: 点击搜索按钮...")
            
            search_btn = None
            
            # 方式1: 通过文本查找
            try:
                search_btn = page.get_by_text('搜索').first
                if search_btn.is_visible():
                    print("   找到搜索按钮 (文本)")
            except:
                pass
            
            # 方式2: 通过按钮类型和图标
            if not search_btn:
                try:
                    search_btn = page.locator('button.el-button--primary:has-text("搜索")').first
                    if search_btn.is_visible():
                        print("   找到搜索按钮 (按钮样式)")
                except:
                    pass
            
            # 方式3: 通过图标查找
            if not search_btn:
                try:
                    # 查找包含搜索图标的按钮
                    search_btn = page.locator('button:has(.el-icon-search), button:has(.fa-search)').first
                    if search_btn.is_visible():
                        print("   找到搜索按钮 (图标)")
                except:
                    pass
            
            if search_btn and search_btn.is_visible():
                search_btn.click()
                print("   ✅ 已点击搜索")
            else:
                print("   ⚠️ 未找到搜索按钮")
            
            # 等待搜索结果加载
            print("👉 等待搜索结果加载...")
            time.sleep(5)
            
            # 3. 点击导出平台数据按钮
            print("\n👉 步骤3: 点击导出平台数据按钮...")
            
            export_btn = None
            
            # 方式1: 通过完整文本
            try:
                export_btn = page.get_by_text('导出平台数据').first
                if export_btn.is_visible():
                    print("   找到导出按钮 (完整文本)")
            except:
                pass
            
            # 方式2: 通过部分文本
            if not export_btn:
                try:
                    export_btn = page.get_by_text('导出').filter(has_text='平台').first
                    if export_btn.is_visible():
                        print("   找到导出按钮 (部分文本)")
                except:
                    pass
            
            # 方式3: 通过按钮样式（导出按钮通常是主要按钮）
            if not export_btn:
                try:
                    # 查找所有按钮，检查文本
                    buttons = page.locator('button').all()
                    for btn in buttons:
                        try:
                            text = btn.inner_text()
                            if '导出' in text and '平台' in text:
                                export_btn = btn
                                print(f"   找到导出按钮 (遍历): {text}")
                                break
                        except:
                            continue
                except:
                    pass
            
            # 方式4: 通过 CSS 选择器和位置（通常在页面顶部）
            if not export_btn:
                try:
                    # 根据截图，导出按钮在搜索区域附近
                    export_btn = page.locator('.operation-btns button:has-text("导出"), .btn-group button:has-text("导出")').first
                    if export_btn.is_visible():
                        print("   找到导出按钮 (CSS选择器)")
                except:
                    pass
            
            if export_btn and export_btn.is_visible():
                export_btn.click()
                print("   ✅ 已点击导出平台数据按钮")
                print("   ⏳ 等待文件下载...")
                time.sleep(15)  # 等待下载完成
                print("   ✅ 下载完成（请检查下载文件夹）")
            else:
                print("   ⚠️ 未找到导出按钮，请手动点击")
                print("   按回车键继续...")
                input()
            
            print("\n" + "=" * 60)
            print("✅ 操作完成")
            print("=" * 60)
            
            # 保持浏览器运行
            print("\n👉 浏览器将保持运行 10 秒...")
            time.sleep(10)
            
        except Exception as e:
            print(f"\n❌ 操作失败: {str(e)}")
            import traceback
            traceback.print_exc()
            print("\n按回车键关闭浏览器...")
            input()
        
        context.close()


if __name__ == '__main__':
    export_platform_data()
