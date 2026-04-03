# -*- coding: utf-8 -*-
"""
导出平台数据脚本 V3
1. 点击月份搜索条件的"×"清空
2. 点击搜索
3. 点击导出平台数据
4. 处理导出弹窗，再次点击导出
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\OAuto\oa_user_data"
TARGET_URL = "https://dui.epoint.com.cn/transferplatform/pages/transferplatform/yfw/strategicmaplist"


def export_platform_data():
    """导出平台数据"""
    print("=" * 60)
    print("导出平台数据 - V3")
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
            # 1. 清空月份搜索条件（点击"×"）
            print("\n👉 步骤1: 清空月份搜索条件...")
            
            # 查找月份输入框旁边的清除按钮（×）
            clear_btn = None
            
            # 方式1: 通过清除按钮的类名
            try:
                # 通常清除按钮有 el-input__clear 或类似的类
                clear_buttons = page.locator('.el-input__clear, .clear-icon, .el-icon-circle-close, [class*="clear"]').all()
                for btn in clear_buttons:
                    if btn.is_visible():
                        # 检查是否在月份输入框附近
                        clear_btn = btn
                        print("   找到清除按钮 (类名)")
                        break
            except:
                pass
            
            # 方式2: 通过 SVG 图标或图片
            if not clear_btn:
                try:
                    # 查找关闭/清除图标
                    clear_btn = page.locator('svg[class*="close"], svg[class*="clear"], i[class*="close"]').first
                    if clear_btn.is_visible():
                        print("   找到清除按钮 (图标)")
                except:
                    pass
            
            # 方式3: 查找所有可见的按钮，检查位置（通常在搜索区域）
            if not clear_btn:
                try:
                    # 获取搜索区域
                    search_area = page.locator('.search-form, .filter-form, [class*="search"]').first
                    if search_area.is_visible():
                        # 在搜索区域内查找清除按钮
                        clear_btn = search_area.locator('.el-input__clear, .clear-icon').first
                        if clear_btn.is_visible():
                            print("   找到清除按钮 (搜索区域内)")
                except:
                    pass
            
            if clear_btn and clear_btn.is_visible():
                clear_btn.click()
                print("   ✅ 已点击清除按钮（×）")
            else:
                print("   ⚠️ 未找到清除按钮，尝试直接清空输入框...")
                # 尝试找到月份输入框并清空
                try:
                    month_input = page.locator('input[placeholder*="月"], .el-date-editor input').first
                    if month_input.is_visible():
                        month_input.click()
                        time.sleep(0.5)
                        month_input.press('Control+a')
                        month_input.press('Delete')
                        print("   ✅ 已清空月份输入框")
                except:
                    print("   ⚠️ 未能清空月份条件")
            
            time.sleep(2)
            
            # 2. 点击搜索按钮
            print("\n👉 步骤2: 点击搜索按钮...")
            
            search_btn = None
            
            # 通过文本查找
            try:
                search_btn = page.get_by_text('搜索', exact=False).first
                if search_btn.is_visible():
                    print("   找到搜索按钮")
            except:
                pass
            
            # 通过按钮样式
            if not search_btn:
                try:
                    search_btn = page.locator('button.el-button--primary').first
                    if search_btn.is_visible():
                        print("   找到搜索按钮 (样式)")
                except:
                    pass
            
            if search_btn and search_btn.is_visible():
                search_btn.click()
                print("   ✅ 已点击搜索")
                time.sleep(3)
            else:
                print("   ⚠️ 未找到搜索按钮")
            
            # 3. 点击导出平台数据按钮
            print("\n👉 步骤3: 点击导出平台数据按钮...")
            
            export_btn = None
            
            # 通过完整文本
            try:
                export_btn = page.get_by_text('导出平台数据', exact=True).first
                if export_btn.is_visible():
                    print("   找到导出按钮")
            except:
                pass
            
            # 通过部分文本遍历
            if not export_btn:
                try:
                    buttons = page.locator('button').all()
                    for btn in buttons:
                        try:
                            text = btn.inner_text()
                            if '导出' in text and '平台' in text:
                                export_btn = btn
                                print(f"   找到导出按钮: {text}")
                                break
                        except:
                            continue
                except:
                    pass
            
            if export_btn and export_btn.is_visible():
                export_btn.click()
                print("   ✅ 已点击导出平台数据按钮")
                time.sleep(2)
            else:
                print("   ⚠️ 未找到导出按钮")
                return
            
            # 4. 处理导出弹窗，再次点击导出
            print("\n👉 步骤4: 处理导出弹窗...")
            
            # 等待弹窗出现
            time.sleep(2)
            
            dialog_export_btn = None
            
            # 方式1: 在弹窗/对话框中查找导出按钮
            try:
                # 查找弹窗
                dialog = page.locator('.el-dialog, .modal-dialog, [class*="dialog"], [class*="modal"]').first
                if dialog.is_visible():
                    print("   找到弹窗")
                    # 在弹窗中查找导出按钮
                    dialog_export_btn = dialog.locator('button:has-text("导出"), .el-button--primary').first
                    if dialog_export_btn.is_visible():
                        print("   找到弹窗内的导出按钮")
            except:
                pass
            
            # 方式2: 查找页面上的所有导出按钮（可能有多个）
            if not dialog_export_btn:
                try:
                    export_buttons = page.get_by_text('导出').all()
                    for btn in export_buttons:
                        if btn.is_visible():
                            # 检查是否在弹窗内
                            dialog_export_btn = btn
                            print("   找到导出按钮（可能是弹窗内）")
                            break
                except:
                    pass
            
            # 方式3: 查找确认/确定按钮
            if not dialog_export_btn:
                try:
                    dialog_export_btn = page.get_by_text('确定').first
                    if dialog_export_btn.is_visible():
                        print("   找到确定按钮")
                except:
                    pass
            
            if dialog_export_btn and dialog_export_btn.is_visible():
                dialog_export_btn.click()
                print("   ✅ 已点击弹窗内的导出/确定按钮")
                print("   ⏳ 等待文件下载...")
                time.sleep(15)
                print("   ✅ 下载完成（请检查下载文件夹）")
            else:
                print("   ⚠️ 未找到弹窗内的导出按钮，请手动点击")
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
