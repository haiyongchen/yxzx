# -*- coding: utf-8 -*-
"""
从已登录的浏览器提取 OA Token 并提交日志
"""
from playwright.sync_api import sync_playwright
import requests
import time
import json
import sys
import os

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
SSO_BASE = "https://oa.epoint.com.cn/epoint-sso-web"
OA_API_BASE = "https://oa.epoint.com.cn/oaextend/rest/dynamicapi"

print("=" * 60)
print("OA 日志自动提交工具 - Cookie 提取版")
print("=" * 60)

# 今天的工作内容
work_content = "OA 邮件分析工具优化（飞书集成）；招投标系统支持（AI 评标异常排查）；电子商城运营（山东/武汉/新疆专区）；技能包接入测试"
today = time.strftime('%Y-%m-%d')

try:
    playwright = sync_playwright().start()
    
    # 使用已保存的 Cookie 启动浏览器
    print("\n1️⃣ 启动浏览器（使用已保存的 Cookie）...")
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        channel="chrome",
        headless=True,  # 无头模式，不需要打开窗口
        args=["--disable-blink-features=AutomationControlled"]
    )
    
    page = context.new_page()
    
    # 访问 OA 首页获取 Cookie
    print("2️⃣ 访问 OA 系统获取 Cookie...")
    page.goto("https://oa.epoint.com.cn/wboa9/", wait_until='networkidle')
    time.sleep(3)
    
    # 提取 access_token Cookie
    cookies = context.cookies()
    access_token = None
    
    for cookie in cookies:
        if cookie.get('name') == 'access_token':
            access_token = cookie.get('value')
            break
    
    # 如果没找到，尝试从 localStorage 获取
    if not access_token:
        access_token = page.evaluate("localStorage.getItem('access_token')")
    
    context.close()
    playwright.stop()
    
    if not access_token:
        print("\n❌ 未找到 access_token，Cookie 可能已过期")
        print("👉 请先运行 oa_login_v2.py 刷新登录状态")
        sys.exit(1)
    
    print(f"3️⃣ 获取到 access_token: {access_token[:30]}...")
    
    # 验证 Token
    print("\n4️⃣ 验证 Token...")
    check_url = f"{SSO_BASE}/rest/oauth2/checktoken"
    check_data = {"checktype": "DTO", "access_token": access_token}
    check_resp = requests.post(check_url, data=check_data, timeout=10, verify=False)
    check_result = check_resp.json()
    
    if "error" in check_result:
        print(f"❌ Token 已失效：{check_result.get('error_description', 'Unknown')}")
        sys.exit(1)
    
    print("✅ Token 有效")
    
    # 提交日志
    print(f"\n5️⃣ 提交 {today} 的工作日志...")
    submit_url = f"{OA_API_BASE}/rz_insert_rzdetail_v2"
    
    # 先获取工作类型
    worktype_url = f"{OA_API_BASE}/rz_select_gzdworktype_v1"
    worktype_resp = requests.post(worktype_url, data={"parentareacode": ""}, 
                                   headers={"Authorization": f"Bearer {access_token}"}, 
                                   timeout=10, verify=False)
    worktype_result = worktype_resp.json()
    gzdw_worktype = "0103"  # 默认值
    
    if worktype_result.get('status', {}).get('code') == 1:
        codeitems = worktype_result.get('custom', {}).get('codeitem', [])
        if codeitems:
            gzdw_worktype = codeitems[0].get('code', '0103')
    
    # 提交日志
    submit_data = {
        "rzdate": today,
        "rzguid": "default_rzguid",
        "missionguid": "default_mission",
        "missionname": "日常运维",
        "gongzuosj": "8",
        "completepercent": "100",
        "gongzuonr": work_content,
        "contenttype": "01",
        "gzdworktype": gzdw_worktype,
        "projectname": "运营维护",
        "projectguid": "default_project"
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    submit_resp = requests.post(submit_url, data=submit_data, headers=headers, timeout=10, verify=False)
    submit_result = submit_resp.json()
    
    print(f"\n📊 提交结果：{submit_result}")
    
    if submit_result.get('status', {}).get('code') == 1:
        print(f"\n🎉 日志提交成功！")
        print(f"   日期：{today}")
        print(f"   工作内容：{work_content[:50]}...")
    else:
        print(f"\n⚠️  提交可能失败或需要额外参数")
        print(f"   响应：{submit_result}")
        print(f"   注意：可能需要先获取有效的 rzguid, missionguid, projectguid")
    
except Exception as e:
    print(f"\n❌ 错误：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
