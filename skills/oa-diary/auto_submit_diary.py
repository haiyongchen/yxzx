# -*- utf-8 -*-
"""
OA 日志自动填写工具 - 使用 Cookie 自动登录
"""
import sys
import io
import os
import json
import time
import requests
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 配置
USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
OA_MAIL_URL = "https://oa.epoint.com.cn:8080/OA9/oa9/mail/mailframe"
OA_API_BASE = "https://oa.epoint.com.cn/oaextend/rest/dynamicapi"

def check_cookie_status():
    """检查 Cookie 文件是否存在"""
    cookies_file = os.path.join(USER_DATA_DIR, "Default", "Network", "Cookies")
    if os.path.exists(cookies_file):
        mtime = datetime.fromtimestamp(os.path.getmtime(cookies_file))
        age = datetime.now() - mtime
        print(f"✅ Cookie 文件存在（{age.days}天前更新）")
        return True
    else:
        print("❌ Cookie 文件不存在")
        return False

def get_token_from_cookie():
    """从 Cookie 文件读取 Token"""
    # 这里需要从 SQLite 数据库读取 Cookie
    # 简化处理：直接返回已保存的 Token 文件
    token_file = r"D:\openclaw-workspace\skills\oa-diary\oa\access_token.txt"
    if os.path.exists(token_file):
        with open(token_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('access_token='):
                    token = line.split('=', 1)[1].strip()
                    print(f"✅ 从文件读取 Token: {token[:30]}...")
                    return token
    return None

def check_token_valid(token):
    """检查 Token 是否有效"""
    url = "https://oa.epoint.com.cn/epoint-sso-web/rest/oauth2/checktoken"
    data = {
        "checktype": "DTO",
        "access_token": token
    }
    try:
        resp = requests.post(url, data=data, timeout=10, verify=False)
        result = resp.json()
        if "error" not in result:
            print("✅ Token 有效")
            return True
        else:
            print(f"❌ Token 失效：{result.get('error_description', 'Unknown')}")
            return False
    except Exception as e:
        print(f"❌ Token 检查失败：{e}")
        return False

def submit_daily_report(token, work_content):
    """提交工作日志"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    print(f"\n📝 准备提交 {today} 的工作日志...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 1. 查询今日是否已有日志
    print("\n1️⃣ 查询今日日志...")
    url = f"{OA_API_BASE}/rz_select_rzinfo_list_v1"
    params = {
        "fromdate": today,
        "todate": today
    }
    
    resp = requests.post(url, headers=headers, data=params, timeout=20, verify=False)
    result = resp.json()
    
    if result.get('status', {}).get('code') == 1:
        existing_logs = result.get('custom', {}).get('rzinfo', [])
        if existing_logs:
            print(f"⚠️  今日已提交 {len(existing_logs)} 条日志")
            for log in existing_logs:
                print(f"   - {log.get('missionname', 'N/A')}: {log.get('gongzuonr', 'N/A')[:50]}")
            return False
        else:
            print("✅ 今日尚未提交日志")
    
    # 2. 获取工作类型
    print("\n2️⃣ 获取工作类型...")
    url = f"{OA_API_BASE}/rz_select_gzdworktype_v1"
    params = {"parentareacode": ""}
    resp = requests.post(url, headers=headers, data=params, timeout=20, verify=False)
    worktype_result = resp.json()
    
    # 默认使用第一个工作类型
    gzdw_worktype = "0103"  # 默认值
    if worktype_result.get('status', {}).get('code') == 1:
        codeitems = worktype_result.get('custom', {}).get('codeitem', [])
        if codeitems:
            gzdw_worktype = codeitems[0].get('code', '0103')
            print(f"   使用工作类型：{gzdw_worktype}")
    
    # 3. 插入日志明细
    print("\n3️⃣ 提交日志...")
    url = f"{OA_API_BASE}/rz_insert_rzdetail_v2"
    
    # 注意：实际提交需要 rzguid, missionguid, projectguid 等
    # 这里使用占位符，实际使用时需要替换
    params = {
        "rzdate": today,
        "rzguid": "default_rzguid",  # 需要从日志分类获取
        "missionguid": "default_mission",  # 需要从任务列表获取
        "missionname": "日常运维",
        "gongzuosj": "8",
        "completepercent": "100",
        "gongzuonr": work_content,
        "contenttype": "01",
        "gzdworktype": gzdw_worktype,
        "projectname": "运营维护",
        "projectguid": "default_project"
    }
    
    resp = requests.post(url, headers=headers, data=params, timeout=20, verify=False)
    result = resp.json()
    
    if result.get('status', {}).get('code') == 1:
        print("✅ 日志提交成功！")
        return True
    else:
        print(f"❌ 日志提交失败：{result}")
        print("⚠️  可能需要先获取有效的 rzguid, missionguid, projectguid")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("OA 日志自动填写工具 v1.0")
    print("=" * 60)
    
    # 检查 Cookie
    if not check_cookie_status():
        print("\n❌ 请先运行 oalogin.py 扫码登录")
        sys.exit(1)
    
    # 获取 Token
    token = get_token_from_cookie()
    if not token:
        print("\n❌ 未找到 Token，请先扫码登录")
        sys.exit(1)
    
    # 检查 Token 有效性
    if not check_token_valid(token):
        print("\n❌ Token 已失效，请重新扫码登录")
        print("👉 运行：python oalogin.py")
        sys.exit(1)
    
    # 今天的工作内容
    work_content = "OA 邮件分析工具优化（飞书集成）；招投标系统支持（AI 评标异常排查）；电子商城运营（山东/武汉/新疆专区）；技能包接入测试"
    
    # 提交日志
    success = submit_daily_report(token, work_content)
    
    if success:
        print("\n🎉 日志填写完成！")
    else:
        print("\n⚠️  日志填写失败，请检查参数或手动填写")
    
    print("\n按回车键退出...")
    input()
