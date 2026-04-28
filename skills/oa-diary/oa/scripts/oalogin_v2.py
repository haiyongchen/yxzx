#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OA 系统登录 - 改进版（支持 Windows 打开二维码图片）
"""
import json, requests, qrcode, os, time, sys, tempfile

# Windows UTF-8 支持
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from urllib.parse import urlencode

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
TOKEN_FILE = os.path.join(BASE_DIR, "access_token.txt")

SSO_BASE = "https://oa.epoint.com.cn/epoint-sso-web"
OA_BASE = "https://oa.epoint.com.cn/epointoa9"
CLIENT_ID = "8b205e73-955a-4ac7-a7ab-53ece32f396c"
REDIRECT_URI = f"{OA_BASE}/frame/pages/login/login"

requests.packages.urllib3.disable_warnings()

def new_session():
    s = requests.Session()
    s.verify = False
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json',
        'Origin': 'https://oa.epoint.com.cn',
        'Referer': f'{SSO_BASE}/login/oauth2login',
    })
    return s

def create_qr(session):
    """生成二维码"""
    url = f"{SSO_BASE}/rest/login/epoa9ssologinaction/page_load"
    params = {
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'isCommondto': 'true',
    }
    session.post(url, params=params, data='', timeout=10)
    
    import base64
    now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    org = base64.b64encode(f"111@{now_str}".encode()).decode()
    request_body = {
        "action": "createQR",
        "request": {
            "qrcodetype": "1",
            "signatureobjects": [{"objid": "", "org": org, "desc": "扫码登陆", "signed": ""}]
        }
    }
    params_json = json.dumps(request_body, separators=(',', ':'))
    api = f"{SSO_BASE}/rest/mcerthtmlservice/doAction"
    resp = session.post(api, files={'params': (None, params_json, 'application/json')}, timeout=10)
    data = resp.json()
    
    if data.get('status') == 1 and data.get('request', {}).get('qrcodeurl'):
        qr_url = data['request']['qrcodeurl']
        print(f"✅ 二维码生成成功")
        return qr_url
    else:
        print(f"❌ 二维码生成失败：{data}")
        return None

def show_qr_image(qr_url):
    """显示二维码图片"""
    # 下载二维码图片
    resp = requests.get(qr_url, verify=False, timeout=10)
    
    # 保存到临时文件
    img_path = os.path.join(tempfile.gettempdir(), "oa_qrcode.png")
    with open(img_path, 'wb') as f:
        f.write(resp.content)
    
    # 在 Windows 上打开图片
    if sys.platform == 'win32':
        os.startfile(img_path)
        print(f"\n✅ 二维码图片已打开（Windows 图片查看器）")
        print(f"   图片路径：{img_path}")
        print(f"\n📱 请用 OA App 扫描屏幕上的二维码！\n")
    else:
        import subprocess
        subprocess.run(["open", img_path])
        print(f"\n✅ 二维码图片已打开")
        print(f"   图片路径：{img_path}\n")
    
    return img_path

def check_scan_status(session, qr_url):
    """检查扫码状态"""
    api = f"{SSO_BASE}/rest/mcerthtmlservice/doAction"
    request_body = {
        "action": "checkStatus",
        "request": {"qrcodeurl": qr_url}
    }
    params_json = json.dumps(request_body, separators=(',', ':'))
    resp = session.post(api, files={'params': (None, params_json, 'application/json')}, timeout=10)
    return resp.json()

def get_token(session, qr_url):
    """获取 access_token"""
    api = f"{SSO_BASE}/rest/mcerthtmlservice/doAction"
    request_body = {
        "action": "getToken",
        "request": {"qrcodeurl": qr_url}
    }
    params_json = json.dumps(request_body, separators=(',', ':'))
    resp = session.post(api, files={'params': (None, params_json, 'application/json')}, timeout=10)
    return resp.json()

def save_token(access_token):
    """保存 token"""
    with open(TOKEN_FILE, "w", encoding='utf-8') as f:
        f.write(f"access_token={access_token}\n")
    print(f"✅ Token 已保存：{TOKEN_FILE}")

if __name__ == '__main__':
    print("=" * 60)
    print("OA 系统扫码登录工具 v2.0 (Windows 改进版)")
    print("=" * 60)
    print()
    
    session = new_session()
    
    # 1. 生成二维码
    print("1️⃣ 生成二维码...")
    qr_url = create_qr(session)
    if not qr_url:
        print("❌ 退出")
        sys.exit(1)
    
    # 2. 显示二维码
    print("\n2️⃣ 显示二维码...")
    show_qr_image(qr_url)
    
    # 3. 轮询检查扫码状态
    print("3️⃣ 等待扫码...\n")
    max_attempts = 180  # 等待 3 分钟
    for i in range(max_attempts):
        time.sleep(1)
        
        if i % 10 == 0:
            print(f"   等待中... ({i//10}秒)", end='\r')
        
        status = check_scan_status(session, qr_url)
        
        if status.get('status') == 1:
            print("\n\n✅ 扫码成功！")
            
            # 获取 token
            token_result = get_token(session, qr_url)
            if token_result.get('status') == 1:
                access_token = token_result['request']['access_token']
                save_token(access_token)
                
                # 验证 token
                check_url = f"{SSO_BASE}/rest/oauth2/checktoken"
                check_data = {"checktype": "DTO", "access_token": access_token}
                check_resp = session.post(check_url, data=check_data, timeout=10)
                check_result = check_resp.json()
                
                if "error" not in check_result:
                    print("\n🎉 登录成功！Token 有效！")
                    sys.exit(0)
                else:
                    print(f"\n⚠️  Token 验证失败：{check_result.get('error_description', 'Unknown')}")
                    sys.exit(1)
            else:
                print(f"\n❌ 获取 Token 失败：{token_result}")
                sys.exit(1)
    
    print("\n\n❌ 扫码超时（3 分钟），请重新运行脚本")
    sys.exit(1)
