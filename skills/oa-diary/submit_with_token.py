# -*- coding: utf-8 -*-
"""
使用 oa_api.py 的 Token 提交日志
"""
import sys
import os
import json
import requests
import time

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Token 文件
TOKEN_FILE = r"D:\openclaw-workspace\skills\oa-diary\oa\access_token.txt"
SSO_BASE = "https://oa.epoint.com.cn/epoint-sso-web"
OA_API_BASE = "https://oa.epoint.com.cn/oaextend/rest/dynamicapi"

# 读取 Token
with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('access_token='):
            access_token = line.split('=', 1)[1].strip()
            break

print("=" * 60)
print("OA 日志自动提交工具")
print("=" * 60)
print(f"\n✅ Token: {access_token[:30]}...")

# 验证 Token
print("\n1️⃣ 验证 Token...")
check_url = f"{SSO_BASE}/rest/oauth2/checktoken"
check_data = {"checktype": "DTO", "access_token": access_token}
check_resp = requests.post(check_url, data=check_data, timeout=10, verify=False)
check_result = check_resp.json()

if "error" in check_result:
    print(f"❌ Token 已失效：{check_result.get('error_description', 'Unknown')}")
    sys.exit(1)

print("✅ Token 有效")

# 今天的工作内容
work_content = "OA 邮件分析工具优化（飞书集成）；招投标系统支持（AI 评标异常排查）；电子商城运营（山东/武汉/新疆专区）；技能包接入测试"
today = time.strftime('%Y-%m-%d')

# 获取工作类型
print(f"\n2️⃣ 获取工作类型...")
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
        print(f"   工作类型：{gzdw_worktype}")

# 提交日志
print(f"\n3️⃣ 提交 {today} 的工作日志...")
submit_url = f"{OA_API_BASE}/rz_insert_rzdetail_v2"

submit_data = {
    "rzdate": today,
    "rzguid": "default",
    "missionguid": "default",
    "missionname": "日常运维",
    "gongzuosj": "8",
    "completepercent": "100",
    "gongzuonr": work_content,
    "contenttype": "01",
    "gzdworktype": gzdw_worktype,
    "projectname": "运营维护",
    "projectguid": "default"
}

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/x-www-form-urlencoded"
}

submit_resp = requests.post(submit_url, data=submit_data, headers=headers, timeout=10, verify=False)
submit_result = submit_resp.json()

print(f"\n📊 提交结果：{json.dumps(submit_result, ensure_ascii=False, indent=2)}")

if submit_result.get('status', {}).get('code') == 1:
    print(f"\n🎉 日志提交成功！")
    print(f"   日期：{today}")
    print(f"   工作内容：{work_content[:50]}...")
elif submit_result.get('error') == '接口被禁用':
    print(f"\n⚠️  API 接口被禁用，无法通过 API 提交")
    print(f"   需要使用浏览器自动化填写网页表单")
else:
    print(f"\n⚠️  提交结果异常，请检查")
