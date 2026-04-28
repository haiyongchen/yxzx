# -*- utf-8 -*-
"""
OA 邮件分析 - 完整版
登录 OA 获取每封邮件的详情链接和完整内容
"""
import sys
import os
import time
import json
from datetime import datetime, timedelta

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
OA_MAIL_URL = "https://oa.epoint.com.cn:8080/OA9/oa9/mail/mailframe"

print("=" * 60)
print("OA 邮件分析 - 完整版")
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
                'category': '',
                'priority': ''
            }
            mails.append(mail_info)
            print(f"  [{len(mails)}] {subject[:50]} | {sender[:20]} | {date}")
            i += 3
            continue
    
    i += 1

print(f"\n✅ 获取到 {len(mails)} 封邮件")

# 阅读每封邮件获取详情
print(f"\n📖 阅读每封邮件获取详情...")

for idx, mail in enumerate(mails):
    print(f"\n  [{idx+1}/{len(mails)}] 阅读：{mail['subject'][:40]}...")
    
    try:
        # 点击邮件
        mail_row = frame.get_by_text(mail['subject'][:30], exact=False).first
        mail_row.click(timeout=5000)
        time.sleep(2)
        
        # 获取邮件详情
        detail_text = frame.locator('body').inner_text(timeout=5000)
        detail_lines = [l.strip() for l in detail_text.split('\n') if l.strip()]
        
        # 提取内容
        content_lines = []
        in_content = False
        for line in detail_lines:
            if any(kw in line for kw in ['返回', '添加', '转移', '转发', '回复', '更多', 'ON', 'OFF', '完整信息', '只显示', '反馈倒序']):
                continue
            if mail['subject'][:20] in line:
                in_content = True
                continue
            if in_content and len(line) > 5:
                if '邮件反馈' in line or '反馈（' in line:
                    break
                content_lines.append(line)
        
        mail['content'] = '\n'.join(content_lines[:10])
        mail['link'] = page.url
        
        # 分类
        content_all = f"{mail['subject']} {mail['content']}"
        if any(kw in content_all for kw in ['商城', '商品', '订单', '专区', '上量', 'e 交易']):
            mail['category'] = '电子商城'
            mail['priority'] = '⭐⭐⭐' if any(kw in content_all for kw in ['上量', '专区']) else '⭐⭐'
        elif any(kw in content_all for kw in ['招标', '投标', '标书', '开标', '评标', '中标', '采购']):
            mail['category'] = '招投标'
            mail['priority'] = '⭐⭐⭐' if any(kw in content_all for kw in ['推广', '立项', '交流']) else '⭐⭐'
        elif any(kw in content_all for kw in ['系统', '通知', '公告', '升级', '评审']):
            mail['category'] = '系统通知'
            mail['priority'] = '⭐⭐'
        elif any(kw in content_all for kw in ['周报', '月报', '日报', '总结', '汇报', '季报']):
            mail['category'] = '工作汇报'
            mail['priority'] = '⭐⭐⭐' if '季报' in content_all else '⭐'
        elif any(kw in content_all for kw in ['培训', '学习', '考试', '课程']):
            mail['category'] = '培训学习'
            mail['priority'] = '⭐'
        else:
            mail['category'] = '其他'
            mail['priority'] = '⭐'
        
        print(f"    ✅ 已阅读，内容长度：{len(mail['content'])}")
        
        # 返回列表
        try:
            back_btn = frame.get_by_text('返回', exact=True).first
            back_btn.click(timeout=3000)
            time.sleep(1)
        except:
            page.go_back()
            time.sleep(2)
        
    except Exception as e:
        print(f"    ❌ 阅读失败：{e}")
        mail['content'] = '阅读失败'
        mail['link'] = 'OA 邮件系统'
        mail['category'] = '其他'
        mail['priority'] = '⭐'

# 保存结果
print("\n💾 保存结果...")
result = {
    'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total': len(mails),
    'mails': mails
}

with open('D:/openclaw-workspace/oa_mails_full.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"✅ 结果已保存：D:/openclaw-workspace/oa_mails_full.json")

# 输出表格数据
print("\n📊 表格数据:")
for mail in mails:
    print(f"{mail['index']} | {mail['subject']} | {mail['sender']} | {mail['category']} | {mail['priority']} | {mail['link']} | {mail['content'][:100]}...")

print("\n按回车键退出...")
input()

context.close()
playwright.stop()
