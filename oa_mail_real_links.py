# -*- utf-8 -*-
"""
OA 邮件分析 - 获取真实邮件详情链接
"""
import sys
import os
import time
import json
from datetime import datetime

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
OA_MAIL_URL = "https://oa.epoint.com.cn:8080/OA9/oa9/mail/mailframe"

print("=" * 60)
print("OA 邮件分析 - 获取真实邮件详情链接")
print("=" * 60)

playwright = sync_playwright().start()

print("\n👉 启动浏览器...")
context = playwright.chromium.launch_persistent_context(
    user_data_dir=USER_DATA_DIR,
    channel="chrome",
    headless=False,
    args=["--disable-blink-features=AutomationControlled"]
)

page = context.new_page()

print(f"👉 访问：{OA_MAIL_URL}")
page.goto(OA_MAIL_URL, wait_until='networkidle', timeout=30000)
time.sleep(3)

if 'login' in page.url.lower():
    print("\n⚠️  需要扫码")
    input()
    time.sleep(3)

print(f"\n✅ 登录成功：{page.title()}")

# 获取邮件列表
print("\n📧 获取邮件列表...")
time.sleep(2)

frame = page.frame_locator('#mail-rightframe')
body_text = frame.locator('body').inner_text(timeout=5000)
lines = [l.strip() for l in body_text.split('\n') if l.strip()]

mails = []
i = 0
while i < len(lines) and len(mails) < 15:
    line = lines[i]
    
    if any(kw in line for kw in ['全选', '转移', '签收', '删除', '本周', '更早', '每页', '条', '关键字', '搜索', '返回', '添加']):
        i += 1
        continue
    
    if i + 2 < len(lines):
        sender = line
        subject = lines[i + 1]
        date = lines[i + 2]
        
        if len(subject) > 3 and len(sender) > 1:
            mail_info = {
                'index': len(mails) + 1,
                'subject': subject,
                'sender': sender,
                'date': date,
                'link': '',
                'content': '',
                'summary': ''
            }
            mails.append(mail_info)
            print(f"  [{len(mails)}] {subject[:50]}")
            i += 3
            continue
    
    i += 1

print(f"\n✅ 获取到 {len(mails)} 封邮件")

# 阅读每封邮件获取详情链接
print(f"\n📖 阅读每封邮件获取详情链接...")

for idx, mail in enumerate(mails):
    print(f"\n  [{idx+1}/{len(mails)}] 阅读：{mail['subject'][:40]}...")
    
    try:
        # 点击邮件主题
        mail_row = frame.get_by_text(mail['subject'][:30], exact=False).first
        mail_row.click(timeout=5000)
        time.sleep(3)
        
        # 等待页面加载
        page.wait_for_load_state('networkidle', timeout=10000)
        time.sleep(2)
        
        # 获取当前 URL
        current_url = page.url
        print(f"    当前 URL: {current_url[:100]}...")
        
        # 尝试获取 iframe 中的链接
        try:
            # 查找邮件详情容器
            detail_frame = frame.locator('[class*="mail-detail"], [class*="mailview"]').first
            if detail_frame:
                print(f"    ✅ 找到详情容器")
        except:
            pass
        
        # 如果 URL 包含 detailguid，记录下来
        if 'detailguid=' in current_url:
            mail['link'] = current_url
            print(f"    ✅ 链接：{current_url[:120]}...")
        else:
            # 尝试获取框架源码
            mail['link'] = current_url
            print(f"    ⚠️  无 detailguid，使用：{current_url[:80]}...")
        
        # 获取邮件内容
        detail_text = frame.locator('body').inner_text(timeout=5000)
        detail_lines = [l.strip() for l in detail_text.split('\n') if l.strip()]
        
        # 提取内容
        content_lines = []
        in_content = False
        for line in detail_lines:
            if any(kw in line for kw in ['返回', '添加', '转移', '转发', '回复', '更多', 'ON', 'OFF', '完整信息']):
                continue
            if mail['subject'][:20] in line:
                in_content = True
                continue
            if in_content and len(line) > 5:
                if '邮件反馈' in line or '反馈（' in line:
                    break
                content_lines.append(line)
        
        mail['content'] = '\n'.join(content_lines[:8])
        mail['summary'] = mail['content'][:150].replace('\n', ' ') + '...' if len(mail['content']) > 150 else mail['content'].replace('\n', ' ')
        
        # 返回列表
        try:
            back_btn = frame.get_by_text('返回', exact=True).first
            back_btn.click(timeout=3000)
            time.sleep(2)
            page.wait_for_load_state('networkidle', timeout=10000)
        except:
            page.go_back()
            time.sleep(2)
        
    except Exception as e:
        print(f"    ❌ 阅读失败：{e}")
        mail['link'] = 'https://oa.epoint.com.cn/OA9/oa9/mail/mailframe'
        mail['content'] = '阅读失败'
        mail['summary'] = '无法获取内容'

# 保存结果
print("\n💾 保存结果...")
result = {
    'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total': len(mails),
    'mails': mails
}

with open('D:/openclaw-workspace/oa_mails_real_links.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"✅ 结果已保存：D:/openclaw-workspace/oa_mails_real_links.json")

# 输出链接
print("\n📊 邮件链接:")
for mail in mails:
    print(f"{mail['index']}. {mail['subject'][:30]}...")
    print(f"   链接：{mail['link']}")

print("\n按回车键退出...")
input()

context.close()
playwright.stop()
