# -*- coding: utf-8 -*-
"""
导出平台数据脚本
1. 登录对账平台
2. 去除月份搜索条件
3. 点击搜索
4. 点击导出平台数据按钮
"""
import sys
import os
import time

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright

# 用户数据目录
USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\OAuto\oa_user_data"

# 目标 URL
TARGET_URL = "https://dui.epoint.com.cn/transferplatform/pages/transferplatform/yfw/strategicmaplist"


def export_platform_data():
    """导出平台数据"""
    print("=" * 60)
    print("导出平台数据")
    print("=" * 60)
    
    with sync_playwright() as p:
        # 启动浏览器（使用已保存的登录状态）
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
        
        # 访问目标页面
        print(f"👉 正在访问: {TARGET_URL}")
        page.goto(TARGET_URL)
        
        # 等待页面加载
        print("👉 等待页面加载...")
        time.sleep(5)
        
        # 检查是否需要登录
        current_url = page.url
        if 'login' in current_url.lower() or 'oauth2login' in current_url.lower():
            print("\n⚠️ 需要登录")
            print("👉 请在浏览器窗口中扫码登录")
            print("👉 登录完成后，按回车键继续...")
            input()
            time.sleep(3)
        
        print(f"\n当前页面: {page.url}")
        print(f"页面标题: {page.title()}")
        
        try:
            # 1. 去除月份搜索条件
            print("\n👉 步骤1: 去除月份搜索条件...")
            # 找到月份选择框并清空
            # 根据截图，月份选择框在 "月:" 标签旁边
            month_select = page.locator('input[placeholder*="月"], .el-input__inner').nth(1)
            if month_select.is_visible():
                month_select.click()
                time.sleep(1)
                # 选择空值或清除
                clear_btn = page.locator('.el-input__clear, .el-icon-circle-close')
                if clear_btn.is_visible():
                    clear_btn.click()
                    print("   已清除月份条件")
                else:
                    # 按 ESC 关闭下拉框
                    page.keyboard.press('Escape')
                    print("   已关闭月份选择")
            time.sleep(2)
            
            # 2. 点击搜索按钮
            print("\n👉 步骤2: 点击搜索按钮...")
            # 根据截图，搜索按钮是蓝色的，有放大镜图标
            search_btn = page.locator('button:has-text("搜索"), button.el-button--primary').first
            if search_btn.is_visible():
                search_btn.click()
                print("   已点击搜索")
            else:
                # 尝试通过图标查找
                search_btn = page.locator('button i.el-icon-search, button .fa-search').first
                if search_btn.is_visible():
                    search_btn.click()
                    print("   已点击搜索（通过图标）")
            
            # 等待搜索结果加载
            print("👉 等待搜索结果加载...")
            time.sleep(5)
            
            # 3. 点击导出平台数据按钮
            print("\n👉 步骤3: 点击导出平台数据按钮...")
            # 根据截图，导出按钮在页面顶部，红色边框标注
            export_btn = page.locator('button:has-text("导出平台数据"), button:has-text("导出")').first
            if export_btn.is_visible():
                export_btn.click()
                print("   已点击导出平台数据按钮")
                print("   请等待文件下载完成...")
                time.sleep(10)  # 等待下载完成
            else:
                print("   ⚠️ 未找到导出按钮，请手动点击")
                print("   按回车键继续...")
                input()
            
            print("\n✅ 操作完成")
            print("👉 请检查下载文件夹获取导出的文件")
            
            # 保持浏览器运行一段时间
            print("\n👉 浏览器将保持运行 10 秒...")
            time.sleep(10)
            
        except Exception as e:
            print(f"\n❌ 操作失败: {str(e)}")
            print("按回车键关闭浏览器...")
            input()
        
        context.close()
    
    print("\n" + "=" * 60)
    print("脚本执行完成")
    print("=" * 60)


if __name__ == '__main__':
    export_platform_data()
