from playwright.sync_api import sync_playwright
import json

user_data_dir = r"D:\work\运营中心\yxzx\新点e交易相关材料\日常数据运维工具\OAuto\oa_user_data"

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
    )
    
    # 访问OA获取cookie
    page = browser.new_page()
    page.goto("https://oa.epoint.com.cn/wboa9/")
    page.wait_for_load_state("networkidle")
    
    # 获取所有cookie
    cookies = page.context.cookies()
    
    # 过滤OA域名的cookie
    oa_cookies = [c for c in cookies if 'epoint.com.cn' in c['domain']]
    
    print("=== OA Cookies ===")
    for c in oa_cookies:
        print(f"{c['name']}: {c['value'][:30]}...")
    
    # 保存到文件
    with open(r"D:\openclaw-workspace\skills\epoint-oa-api\oa_cookies.json", "w", encoding="utf-8") as f:
        json.dump(oa_cookies, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Cookies已保存到 epoint-oa-api/oa_cookies.json")
    
    input("\n按回车键关闭浏览器...")
    browser.close()
