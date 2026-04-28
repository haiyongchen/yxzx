# -*- coding: utf-8 -*-
"""
OA 日志自动填写工具 - 使用已登录的浏览器
"""
from playwright.sync_api import sync_playwright
import time
import sys
import os

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
OA_DIARY_URL = "https://oa.epoint.com.cn/oaextend/rest/dynamicapi/rz_insert_rzdetail_v2"

print("=" * 60)
print("OA 日志自动填写工具")
print("=" * 60)

# 今天的工作内容
work_content = "OA 邮件分析工具优化（飞书集成）；招投标系统支持（AI 评标异常排查）；电子商城运营（山东/武汉/新疆专区）；技能包接入测试"

try:
    playwright = sync_playwright().start()
    
    # 使用已保存的 Cookie 启动浏览器
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        channel="chrome",
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )
    
    page = context.new_page()
    
    print("\n👉 正在访问 OA 日志系统...")
    
    # 访问日志填写页面（这里需要实际的日志填写页面 URL）
    # 由于 OA 系统日志填写是表单形式，我们直接使用 API 调用
    
    print("✅ 浏览器已启动，Cookie 已加载")
    print(f"\n📝 今日工作内容：{work_content}")
    print("\n⚠️  注意：OA 日志填写需要具体的页面 URL 和表单结构")
    print("   请提供日志填写页面的 URL，或者使用 API 方式提交")
    
    # 保持浏览器打开
    print("\n👉 浏览器窗口已打开，可以手动填写日志")
    print("   或者提供日志页面 URL 让我自动填写")
    
    time.sleep(30)
    
    context.close()
    playwright.stop()
    
    print("\n✅ 完成！")
    
except Exception as e:
    print(f"\n❌ 错误：{e}")
    import traceback
    traceback.print_exc()
