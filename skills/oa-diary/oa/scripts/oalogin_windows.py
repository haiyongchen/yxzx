# -*- coding: utf-8 -*-
"""
OA 系统扫码登录 - Windows 兼容版
自动打开二维码图片，等待扫码后保存 Token
"""
import json, requests, qrcode, os, time, sys, re, subprocess, tempfile
from urllib.parse import urlencode, urlparse, parse_qs

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
TOKEN_FILE = os.path.join(BASE_DIR, "access_token.txt")

SSO_BASE = "https://oa.epoint.com.cn/epoint-sso-web"
OA_BASE = "https://oa.epoint.com.cn/epointoa9"
QR_LOGIN_URL = "http://218.4.136.126:1443/epointoa9/H5/oatest/ejs.m7.mobileframe.oa/pages/scanLogin/scan_login.html"
CLIENT_ID = "8b205e73-955a-4ac7-a7ab-53ece32f396c"
REDIRECT_URI = f"{OA_BASE}/frame/pages/login/login"

requests.packages.urllib3.disable_warnings()

# Windows UTF-8 支持
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def new_session():
    s = requests.Session()
    s.verify = False
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
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
    
    # 调试：打印响应内容
    print(f"   响应状态码：{resp.status_code}")
    print(f"   响应内容：{resp.text[:200]}")
    
    try:
        data = resp.json()
        qrcodeid = data["custom"]["qrcodeid"]
        return qrcodeid
    except Exception as e:
        print(f"   JSON 解析失败：{e}")
        print(f"   可能是网络问题或 API 变更")
        raise

def show_qr(qr_url):
    """显示二维码 - Windows 自动打开图片"""
    # 1. 生成二维码图片
    img = qrcode.QRCode(version=3, border=2, error_correction=qrcode.constants.ERROR_CORRECT_H)
    img.add_data(qr_url)
    img.make(fit=True)
    
    # 保存到临时文件
    img_path = os.path.join(tempfile.gettempdir(), "oa_qrcode.png")
    img.make_image(fill_color="black", back_color="white").save(img_path)
    
    # 2. Windows 自动打开图片
    if sys.platform == 'win32':
        os.startfile(img_path)
        print(f"\n✅ 二维码图片已打开（Windows 图片查看器）")
        print(f"   图片路径：{img_path}")
        print(f"\n📱 请用 OA App 扫描屏幕上的二维码！")
        print(f"   如果图片被遮挡，可扫描下方终端二维码\n")
    
    # 3. 同时显示终端 ASCII 二维码（备用）
    os.system('mode con: cols=120 >nul 2>&1')
    qr = qrcode.QRCode(border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(qr_url)
    qr.make(fit=True)
    print("\n终端备用二维码：\n")
    qr.print_ascii(invert=True)
    print()
    
    return img_path

def poll_scan(session, code):
    """轮询扫码状态"""
    url = f"{SSO_BASE}/rest/qrcode/qrloginquery"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    data = {
        'code': code,
        'time': timestamp,
        'order': 'query',
    }
    resp = session.post(url, data=data, timeout=10)
    try:
        result = resp.json()
        return result
    except:
        return {"scanned": False, "invalid": False}

def do_login(session, code):
    """扫码成功后登录"""
    url = f"{SSO_BASE}/rest/qrcode/qrloginquery"
    data = {
        'code': code,
        'time': '',
        'order': 'login',
    }
    resp = session.post(url, data=data, timeout=10)
    return resp.json()

def oauth2_login(session, token, state):
    """OAuth2 登录获取 code"""
    url = f"{SSO_BASE}/rest/login/loginaction/login"
    commonDto = json.dumps([{
        "id": "epointca1",
        "type": "epointca",
        "action": "epointcaValue",
        "dataOptions": "{CAType:195}",
        "mapClass": "com.epoint.usercontrol.EpointCa",
        "value": json.dumps({
            "sN": "", "cN": "", "publicKey": "", "ePublicKey": "",
            "deviceNum": "", "qZ": "", "dS": "",
            "orgData": f"111@{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
            "cK": "", "yXQ": ""
        })
    }, {
        "id": "_common_hidden_viewdata",
        "type": "hidden",
        "value": ""
    }])
    
    cmdParams = json.dumps({
        "EpStr6": token,
        "EpStr1": "qrcodelogin",
        "loadType": "3"
    })
    
    resp = session.post(url, data={
        'commonDto': commonDto,
        'cmdParams': cmdParams,
    }, timeout=10)
    
    result = resp.json()
    if result.get('status', {}).get('code') == '307':
        return result['status']['url']
    return None

def get_access_token(session, oauth2_url, state):
    """通过 OAuth2 获取 access_token"""
    full_url = f"{SSO_BASE}/{oauth2_url}"
    resp = session.get(full_url, allow_redirects=False, timeout=10)
    
    if resp.status_code == 302:
        location = resp.headers.get('Location', '')
        code_match = re.search(r'code=([a-f0-9]+)', location)
        if code_match:
            oauth_code = code_match.group(1)
            print(f"[OAuth2] 获取到 code: {oauth_code}")
            
            callback_url = location
            resp2 = session.get(callback_url, allow_redirects=False, timeout=10)
            
            for cookie in session.cookies:
                if cookie.name == 'access_token':
                    return cookie.value
            
            if resp2.status_code == 302:
                location2 = resp2.headers.get('Location', '')
                if 'access_token' in location2:
                    token_match = re.search(r'access_token=([^&]+)', location2)
                    if token_match:
                        return token_match.group(1)
    
    return None

def save_token(access_token):
    """保存 token"""
    with open(TOKEN_FILE, "w", encoding='utf-8') as f:
        f.write(f"access_token={access_token}\n")
    print(f"\n✅ Token 已保存：{TOKEN_FILE}")

def main():
    print("=" * 60)
    print("OA 系统扫码登录工具 v1.0 (Windows 兼容版)")
    print("=" * 60)
    
    # 检查已有 Token
    if os.path.exists(TOKEN_FILE):
        print(f"\n⚠️  检测到已有 Token 文件：{TOKEN_FILE}")
        print("   如需重新登录，请删除该文件后重新运行")
        with open(TOKEN_FILE, "r", encoding='utf-8') as f:
            print(f"\n{f.read().strip()}")
        return
    
    session = new_session()
    
    # Step 1: 生成二维码
    print("\n1️⃣ 生成二维码...")
    qrcodeid = create_qr(session)
    qr_url = f"{QR_LOGIN_URL}?code={qrcodeid}"
    print(f"   二维码 ID: {qrcodeid[:20]}...")
    
    # Step 2: 显示二维码（自动打开图片）
    print("\n2️⃣ 显示二维码...")
    img_path = show_qr(qr_url)
    
    # Step 3: 轮询等待扫码
    print("\n3️⃣ 等待扫码...（最多等待 3 分钟）\n")
    max_attempts = 180
    scanned = False
    
    for i in range(max_attempts):
        time.sleep(1)
        if i % 10 == 0:
            print(f"   等待中... ({i//10}秒)", end='\r')
        
        result = poll_scan(session, qrcodeid)
        
        if result.get('scanned') == '1' or result.get('status') == 1:
            print("\n\n✅ 扫码成功！")
            scanned = True
            break
        
        if result.get('invalid') == '1':
            print("\n\n❌ 二维码已失效，请重新运行脚本")
            return
    
    if not scanned:
        print("\n\n❌ 扫码超时（3 分钟），请重新运行脚本")
        return
    
    # Step 4: 执行登录
    print("\n4️⃣ 执行登录...")
    login_result = do_login(session, qrcodeid)
    
    if login_result.get('status') == 1:
        token = login_result.get('custom', {}).get('token', '')
        if token:
            print("   获取到临时 Token")
            
            # Step 5: OAuth2 登录
            print("\n5️⃣ OAuth2 授权...")
            oauth2_url = oauth2_login(session, token, None)
            
            if oauth2_url:
                access_token = get_access_token(session, oauth2_url, None)
                
                if access_token:
                    save_token(access_token)
                    
                    # 验证 Token
                    print("\n6️⃣ 验证 Token...")
                    check_url = f"{SSO_BASE}/rest/oauth2/checktoken"
                    check_data = {"checktype": "DTO", "access_token": access_token}
                    check_resp = session.post(check_url, data=check_data, timeout=10)
                    check_result = check_resp.json()
                    
                    if "error" not in check_result:
                        print("\n🎉 登录成功！Token 有效！")
                        print(f"\n✅ 现在可以提交日志了")
                        return
                    else:
                        print(f"\n⚠️  Token 验证失败：{check_result.get('error_description', 'Unknown')}")
                else:
                    print("\n❌ 获取 access_token 失败")
            else:
                print("\n❌ OAuth2 登录失败")
        else:
            print("\n❌ 登录失败，未获取到 token")
    else:
        print(f"\n❌ 登录失败：{login_result}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n按回车键退出...")
    input()
