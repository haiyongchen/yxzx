# -*- utf-8 -*-
"""
OA 邮件阅读总结工具 v4.0
- 正确过滤 7 天内的邮件（从今天往前推 7 天）
- 点开邮件阅读正文内容
- 生成内容总结
"""
import sys
import os
import time
from datetime import datetime, timedelta

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

# ========== 可配置参数 ==========
DAYS_RANGE = 7  # 分析最近 7 天
MAX_MAILS_TO_READ = 10  # 最多阅读多少封邮件
# ================================

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
OA_MAIL_URL = "https://oa.epoint.com.cn:8080/OA9/oa9/mail/mailframe"


def parse_date(date_str):
    """解析日期字符串，返回 datetime 对象"""
    if not date_str:
        return None
    
    try:
        # 完整日期格式
        if '2026-' in date_str or '2025-' in date_str:
            for fmt in ['%Y-%m-%d %H:%M', '%Y-%m-%d']:
                try:
                    return datetime.strptime(date_str.strip(), fmt)
                except:
                    continue
        
        # 星期格式（星期六、星期五等）
        weekday_map = {
            '星期一': 0, '星期二': 1, '星期三': 2, '星期四': 3,
            '星期五': 4, '星期六': 5, '星期日': 6
        }
        
        today = datetime.now()
        for day_name, offset in weekday_map.items():
            if day_name in date_str:
                # 计算该星期是几天前
                days_ago = (today.weekday() - offset) % 7
                if days_ago == 0:
                    days_ago = 7  # 如果是今天，算 7 天前（避免重复）
                return today - timedelta(days=days_ago)
        
        # 简单日期格式（MM-DD）
        if '-' in date_str and len(date_str) == 5:
            try:
                date = datetime.strptime(f"2026-{date_str}", '%Y-%m-%d')
                return date
            except:
                pass
    
    except Exception as e:
        pass
    
    return None


def is_within_date_range(date_str, days=DAYS_RANGE):
    """检查日期是否在指定范围内"""
    mail_date = parse_date(date_str)
    if not mail_date:
        return True  # 无法解析的也保留
    
    cutoff_date = datetime.now() - timedelta(days=days)
    return mail_date >= cutoff_date


print("=" * 60)
print("OA 邮件阅读总结工具 v4.0")
print("=" * 60)
print(f"\n📅 分析时间范围：{DAYS_RANGE} 天")
print(f"   从 {datetime.now() - timedelta(days=DAYS_RANGE)} 到 {datetime.now()}")
print(f"📖 最多阅读邮件数：{MAX_MAILS_TO_READ}")

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

# 检查登录
if 'login' in page.url.lower():
    print("\n⚠️  需要扫码，请在浏览器中扫码后按回车...")
    input()
    time.sleep(3)
    try:
        with page.expect_navigation(timeout=15000):
            pass
    except:
        pass

print(f"\n✅ 登录成功：{page.title()}")

# 获取邮件列表
print("\n📧 获取邮件列表...")
time.sleep(2)

frame = page.frame_locator('#mail-rightframe')
body_text = frame.locator('body').inner_text(timeout=5000)
lines = [l.strip() for l in body_text.split('\n') if l.strip()]

print(f"  获取到 {len(lines)} 行文本")

# 解析邮件（格式：发件人 → 主题 → 日期）
mails = []
i = 0
while i < len(lines) and len(mails) < MAX_MAILS_TO_READ:
    line = lines[i]
    
    # 跳过 UI 元素
    if any(kw in line for kw in ['全选', '转移', '签收', '删除', '本周', '更早', '每页', '条', '关键字', '搜索', '返回', '添加']):
        i += 1
        continue
    
    # 检查是否是发件人
    if i + 2 < len(lines):
        sender = line
        subject = lines[i + 1]
        date = lines[i + 2]
        
        # 验证是否是合理的邮件结构
        if len(subject) > 3 and len(sender) > 1:
            # 检查日期是否在范围内
            if is_within_date_range(date, DAYS_RANGE):
                mail_info = {
                    'index': len(mails) + 1,
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'content': '',
                    'summary': ''
                }
                mails.append(mail_info)
                print(f"  [{len(mails)}] {subject[:50]} | {sender[:20]} | {date} ✅")
                i += 3
                continue
            else:
                print(f"  [跳过] {subject[:30]} | 日期超出范围：{date}")
                i += 3
                continue
    
    i += 1

print(f"\n✅ 获取到 {len(mails)} 封时间范围内的邮件")

# 阅读邮件内容
print(f"\n📖 阅读邮件内容...")

for idx, mail in enumerate(mails):
    print(f"\n  [{idx+1}/{len(mails)}] 阅读：{mail['subject'][:40]}...")
    
    try:
        # 点击邮件主题
        mail_row = frame.get_by_text(mail['subject'][:30], exact=False).first
        mail_row.click(timeout=5000)
        time.sleep(2)
        
        # 获取邮件正文
        detail_text = frame.locator('body').inner_text(timeout=5000)
        detail_lines = [l.strip() for l in detail_text.split('\n') if l.strip()]
        
        # 提取正文内容（跳过按钮等 UI 元素）
        content_lines = []
        in_content = False
        for line in detail_lines:
            # 跳过 UI 元素
            if any(kw in line for kw in ['返回', '添加', '转移', '转发', '回复', '更多', 'ON', 'OFF', '完整信息', '只显示', '反馈倒序']):
                continue
            
            # 找到邮件主题后开始提取
            if mail['subject'][:20] in line:
                in_content = True
                continue
            
            # 提取内容
            if in_content and len(line) > 5:
                # 跳过反馈部分
                if '邮件反馈' in line or '反馈（' in line:
                    break
                content_lines.append(line)
        
        mail['content'] = '\n'.join(content_lines[:15])  # 限制长度
        
        # 生成总结
        if mail['content']:
            # 提取关键信息
            first_lines = mail['content'].split('\n')[:3]
            mail['summary'] = ' '.join(first_lines)[:200]
            print(f"    ✅ 已阅读，内容长度：{len(mail['content'])}")
        else:
            mail['summary'] = '无法获取正文'
            print(f"    ⚠️  无法获取正文")
        
        # 返回邮件列表
        try:
            back_btn = frame.get_by_text('返回', exact=True).first
            back_btn.click(timeout=3000)
            time.sleep(1)
        except:
            page.go_back()
            time.sleep(2)
        
    except Exception as e:
        print(f"    ❌ 阅读失败：{e}")
        mail['content'] = ''
        mail['summary'] = '阅读失败'

# 分类
print("\n🔍 分析分类...")

categories = {
    '招投标': ['招标', '投标', '标书', '开标', '评标', '中标', '询价', '采购'],
    '电子商城': ['商城', '商品', '订单', '交易', '专区', '上量', 'e 交易', '阳光优采'],
    '培训学习': ['培训', '学习', '考试', '课程'],
    '系统通知': ['系统', '通知', '公告', '升级', '评审'],
    '工作汇报': ['周报', '月报', '日报', '总结', '汇报', '季报'],
    '其他': []
}

classified = {cat: [] for cat in categories.keys()}

for mail in mails:
    content = f"{mail['subject']} {mail['summary']}"
    
    matched = False
    for category, keywords in categories.items():
        if category == '其他':
            continue
        if any(kw in content for kw in keywords):
            classified[category].append(mail)
            matched = True
            break
    
    if not matched:
        classified['其他'].append(mail)

print("\n📊 分类统计:")
for category, mails_in_cat in classified.items():
    if mails_in_cat:
        print(f"  📁 {category}: {len(mails_in_cat)} 封")

# 保存报告
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
report_file = f'oa_mail_content_summary_{timestamp}.md'

print(f"\n💾 保存报告：{report_file}")

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(f"# OA 邮件内容总结报告\n\n")
    f.write(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"**时间范围**: 最近 {DAYS_RANGE} 天 ({datetime.now() - timedelta(days=DAYS_RANGE)} 至 {datetime.now()})\n")
    f.write(f"**阅读邮件数**: {len(mails)} 封\n\n")
    
    f.write("## 📊 分类统计\n\n")
    for category, mails_in_cat in classified.items():
        if mails_in_cat:
            f.write(f"- **{category}**: {len(mails_in_cat)} 封\n")
    f.write("\n")
    
    f.write("## 📧 邮件详细总结\n\n")
    
    for category, mails_in_cat in classified.items():
        if mails_in_cat:
            f.write(f"### {category}\n\n")
            
            for i, mail in enumerate(mails_in_cat, 1):
                f.write(f"#### {i}. {mail['subject']}\n\n")
                f.write(f"- **发件人**: {mail['sender']}\n")
                f.write(f"- **日期**: {mail['date']}\n")
                f.write(f"- **内容摘要**: {mail['summary']}\n\n")
                
                if mail['content']:
                    f.write(f"**原文内容**:\n> {mail['content']}\n\n")
                
                f.write("---\n\n")

print(f"✅ 报告已保存")
print(f"\n🎯 完成！")

print("\n按回车键退出...")
input()

context.close()
playwright.stop()
