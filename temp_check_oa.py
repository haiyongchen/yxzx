from playwright.sync_api import sync_playwright

user_data_dir = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\OAuto\oa_user_data"

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        args=['--disable-blink-features=AutomationControlled']
    )
    page = browser.new_page()
    page.goto("https://oa.epoint.com.cn/wboa9/")
    page.wait_for_load_state("networkidle")
    print(f"Title: {page.title()}")
    print(f"URL: {page.url}")
    
    # 检查是否已登录
    if "login" in page.url.lower() or "登录" in page.title().lower():
        print("未登录，需要扫码")
    else:
        print("已登录!")
    
    input("按回车键关闭浏览器...")
    browser.close()
