# -*- coding: utf-8 -*-
"""
保存 OA 登录状态
首次登录后运行此脚本，保持浏览器运行 10 秒确保状态保存
"""
from browser_manager import init_browser, close_browser
from oa_tools import wait_for_oa_ready

print("=" * 60)
print("OA 登录状态保存工具")
print("=" * 60)

# 打开浏览器
page = init_browser()

# 访问 OA
print("\n👉 正在打开 OA 系统...")
page.goto("https://oa.epoint.com.cn")

# 等待页面加载
wait_for_oa_ready(page)

print(f"\n当前 URL: {page.url}")
print(f"页面标题: {page.title()}")

if "login" in page.url.lower() or "登录" in page.title():
    print("\n⚠️ 检测到登录页面，请先扫码登录...")
    input("\n👉 完成登录后，按回车键继续保存状态...")
    
    # 再次等待页面稳定
    wait_for_oa_ready(page)
    print(f"\n登录后 URL: {page.url}")
    print(f"登录后标题: {page.title()}")

# 保持运行一段时间，确保状态保存到磁盘
print("\n👉 正在保存登录状态，请等待 10 秒...")
page.wait_for_timeout(10000)

# 正确关闭浏览器
close_browser()

print("\n" + "=" * 60)
print("✅ 登录状态已保存！")
print("下次可以直接使用，无需再次登录")
print("=" * 60)
