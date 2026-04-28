# -*- coding: utf-8 -*-
"""
检查 OA 日志相关 API 可用性
"""
from playwright.sync_api import sync_playwright
import requests
import time
import sys
import os

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
SSO_BASE = "https://oa.epoint.com.cn/epoint-sso-web"
OA_API_BASE = "https://oa.epoint.com.cn/oaextend/rest/dynamicapi"

# 获取 Token
playwright = sync_playwright().start()
context = playwright.chromium.launch_persistent_context(
    user_data_dir=USER_DATA_DIR,
    channel="chrome",
    headless=True,
    args=["--disable-blink-features=AutomationControlled"]
)

page = context.new_page()
page.goto("https://oa.epoint.com.cn/wboa9/", wait_until='networkidle')
time.sleep(3)

cookies = context.cookies()
access_token = None
for cookie in cookies:
    if cookie.get('name') == 'access_token':
        access_token = cookie.get('value')
        break

context.close()
playwright.stop()

if not access_token:
    print("❌ 未找到 access_token")
    sys.exit(1)

print(f"✅ Token: {access_token[:30]}...\n")

headers = {"Authorization": f"Bearer {access_token}"}

# 测试各个 API
apis_to_test = [
    ("rz_select_rzinfo_list_v1", {"fromdate": "2026-04-20", "todate": "2026-04-20"}, "查询日志列表"),
    ("rz_checkuser_v2", {"rzdate": "2026-04-20"}, "检查用户状态"),
    ("rz_insert_rzdetail_v2", {"rzdate": "2026-04-20"}, "插入日志"),
    ("rz_getnowtime_v1", {}, "获取服务器时间"),
]

print("测试 API 可用性：\n")

for api_id, params, desc in apis_to_test:
    url = f"{OA_API_BASE}/{api_id}"
    try:
        resp = requests.post(url, data=params, headers=headers, timeout=10, verify=False)
        result = resp.json()
        status = "✅" if (result.get('status', {}).get('code') == 1 or 'error' not in result) else "❌"
        print(f"{status} {api_id} - {desc}")
        if result.get('error'):
            print(f"   错误：{result['error']}")
    except Exception as e:
        print(f"❌ {api_id} - {desc} - 异常：{e}")

print("\n完成！")
