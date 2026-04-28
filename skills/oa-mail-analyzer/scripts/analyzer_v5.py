# -*- utf-8 -*-
"""
OA 邮件分析工具 v5.1
- 读取 7 天内邮件
- 阅读邮件正文内容
- 创建飞书在线文档和表格
- 返回飞书文档地址
"""
import sys
import os
import time
import json
import subprocess
from datetime import datetime, timedelta

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

# ========== 可配置参数 ==========
DAYS_RANGE = 7
MAX_MAILS_TO_READ = 15
# ================================

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
OA_MAIL_URL = "https://oa.epoint.com.cn:8080/OA9/oa9/mail/mailframe"


def parse_date(date_str):
    """解析日期字符串"""
    if not date_str:
        return None
    
    try:
        if '2026-' in date_str or '2025-' in date_str:
            for fmt in ['%Y-%m-%d %H:%M', '%Y-%m-%d']:
                try:
                    return datetime.strptime(date_str.strip(), fmt)
                except:
                    continue
        
        weekday_map = {
            '星期一': 0, '星期二': 1, '星期三': 2, '星期四': 3,
            '星期五': 4, '星期六': 5, '星期日': 6
        }
        
        today = datetime.now()
        for day_name, offset in weekday_map.items():
            if day_name in date_str:
                days_ago = (today.weekday() - offset) % 7
                if days_ago == 0:
                    days_ago = 7
                return today - timedelta(days=days_ago)
        
        if '-' in date_str and len(date_str) == 5:
            try:
                return datetime.strptime(f"2026-{date_str}", '%Y-%m-%d')
            except:
                pass
    except:
        pass
    
    return None


def is_within_date_range(date_str, days=DAYS_RANGE):
    """检查日期是否在范围内"""
    mail_date = parse_date(date_str)
    if not mail_date:
        return True
    
    cutoff_date = datetime.now() - timedelta(days=days)
    return mail_date >= cutoff_date


def create_feishu_docs_and_sheet(mail_data):
    """使用飞书 API 创建在线文档和表格"""
    print("\n📊 创建飞书在线文档和表格...")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    doc_name = f"OA 邮件分析报表（{datetime.now().strftime('%Y-%m-%d')}）"
    
    # 准备分类和优先级数据
    categories = {
        '招投标': ['招标', '投标', '标书', '开标', '评标', '中标', '询价', '采购'],
        '电子商城': ['商城', '商品', '订单', '交易', '专区', '上量', 'e 交易', '阳光优采'],
        '培训学习': ['培训', '学习', '考试', '课程'],
        '系统通知': ['系统', '通知', '公告', '升级', '评审'],
        '工作汇报': ['周报', '月报', '日报', '总结', '汇报', '季报'],
        '其他': []
    }
    
    # 处理邮件数据
    processed_mails = []
    for idx, mail in enumerate(mail_data, 1):
        content = f"{mail['subject']} {mail.get('summary', '')}"
        
        # 分类
        category = '其他'
        for cat, keywords in categories.items():
            if cat == '其他':
                continue
            if any(kw in content for kw in keywords):
                category = cat
                break
        
        # 优先级
        priority = '⭐'
        if any(kw in content for kw in ['上量', '专区', '立项', '季报', '推广']):
            priority = '⭐⭐⭐'
        elif any(kw in content for kw in ['评审', '部署', '对接', '协调']):
            priority = '⭐⭐'
        
        summary = mail.get('summary', '')[:200].replace('\n', ' ')
        
        processed_mails.append({
            'index': idx,
            'subject': mail['subject'],
            'sender': mail['sender'],
            'date': mail['date'],
            'category': category,
            'summary': summary,
            'priority': priority
        })
    
    # 统计信息
    cat_count = {}
    priority_count = {}
    for mail in processed_mails:
        cat_count[mail['category']] = cat_count.get(mail['category'], 0) + 1
        priority_count[mail['priority']] = priority_count.get(mail['priority'], 0) + 1
    
    # ========== 创建飞书表格 ==========
    print("\n📊 创建飞书表格...")
    
    # 准备表格数据
    headers = ['邮件主题', '发件人', '分类', '优先级', '日期', '内容摘要']
    values = []
    for mail in processed_mails:
        values.append([
            mail['subject'],
            mail['sender'],
            mail['category'],
            mail['priority'],
            mail['date'],
            mail['summary']
        ])
    
    # 使用 subprocess 调用 feishu_sheet 创建
    import subprocess
    import json as json_lib
    
    sheet_params = {
        'action': 'create',
        'title': doc_name,
        'headers': headers,
        'data': values
    }
    
    # 写入临时 JSON 文件
    params_file = os.path.join(os.path.dirname(__file__), 'feishu_sheet_params.json')
    with open(params_file, 'w', encoding='utf-8') as f:
        json_lib.dump(sheet_params, f, ensure_ascii=False)
    
    print(f"💾 表格参数已保存：{params_file}")
    print("⚠️  请使用以下命令创建飞书表格：")
    print(f"   python -c \"import json; from feishu_sheet_tool import create; params=json.load(open('{params_file}')); create(**params)\"")
    
    # ========== 创建飞书文档 ==========
    print("\n📄 创建飞书文档...")
    
    # 构建飞书文档 Markdown 内容
    md_content = f"""# 📧 OA 邮件分析报表

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**时间范围**: 最近 {DAYS_RANGE} 天  
**邮件总数**: {len(mail_data)} 封  

---

## 📊 分类统计

| 分类 | 数量 | 占比 |
|------|------|------|
"""
    
    for cat, count in sorted(cat_count.items(), key=lambda x: -x[1]):
        percentage = round(count / len(mail_data) * 100)
        md_content += f"| {cat} | {count} | {percentage}% |\n"
    
    md_content += f"""
## ⭐ 优先级分布

| 优先级 | 数量 | 说明 |
|--------|------|------|
| ⭐⭐⭐ | {priority_count.get('⭐⭐⭐', 0)} | 重点邮件（上量、专区、立项、季报等） |
| ⭐⭐ | {priority_count.get('⭐⭐', 0)} | 重要邮件（评审、部署、协调等） |
| ⭐ | {priority_count.get('⭐', 0)} | 常规邮件 |

---

## 📋 邮件详情

"""
    
    # 按优先级分组邮件
    priority_groups = {'⭐⭐⭐': [], '⭐⭐': [], '⭐': []}
    for mail in processed_mails:
        priority_groups[mail['priority']].append(mail)
    
    priority_names = {'⭐⭐⭐': '🔴 优先级 ⭐⭐⭐', '⭐⭐': '🟡 优先级 ⭐⭐', '⭐': '🟢 优先级 ⭐'}
    
    for priority in ['⭐⭐⭐', '⭐⭐', '⭐']:
        mails_in_group = priority_groups[priority]
        if mails_in_group:
            md_content += f"### {priority_names[priority]}（{len(mails_in_group)} 封）\n\n"
            for mail in mails_in_group:
                md_content += f"#### {mail['subject']}\n"
                md_content += f"- **发件人**: {mail['sender']}\n"
                md_content += f"- **日期**: {mail['date']}\n"
                md_content += f"- **分类**: {mail['category']}\n"
                md_content += f"- **摘要**: {mail['summary']}\n\n"
    
    md_content += """---

## 📌 待办事项

1. ⚠️ **阅读失败的邮件** - 需要手动查看 OA 系统
2. 📊 **重点邮件** - 优先处理⭐⭐⭐优先级邮件
3. 🏗️ **专区部署** - 跟进专区开设和部署事宜
4. 🔧 **系统评审** - 参与相关评审工作

---

*报表由 OA 邮件分析工具 v5.1 自动生成*
"""
    
    # 保存文档内容
    md_file = os.path.join(os.path.dirname(__file__), 'feishu_doc_content.md')
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"💾 文档内容已保存：{md_file}")
    print("⚠️  请使用以下命令创建飞书文档：")
    print(f"   python -c \"from feishu_doc_tool import create; create(title='{doc_name}', markdown=open('{md_file}', encoding='utf-8').read())\"")
    
    return params_file, md_file, doc_name


print("=" * 60)
print("OA 邮件分析工具 v5.1 - 飞书版")
print("=" * 60)
print(f"\n📅 分析时间范围：{DAYS_RANGE} 天")
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
while i < len(lines) and len(mails) < MAX_MAILS_TO_READ:
    line = lines[i]
    
    if any(kw in line for kw in ['全选', '转移', '签收', '删除', '本周', '更早', '每页', '条', '关键字', '搜索', '返回', '添加']):
        i += 1
        continue
    
    if i + 2 < len(lines):
        sender = line
        subject = lines[i + 1]
        date = lines[i + 2]
        
        if len(subject) > 3 and len(sender) > 1:
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
    
    i += 1

print(f"\n✅ 获取到 {len(mails)} 封邮件")

# 阅读邮件内容
print(f"\n📖 阅读邮件内容...")

for idx, mail in enumerate(mails):
    print(f"\n  [{idx+1}/{len(mails)}] 阅读：{mail['subject'][:40]}...")
    
    try:
        mail_row = frame.get_by_text(mail['subject'][:30], exact=False).first
        mail_row.click(timeout=5000)
        time.sleep(2)
        
        detail_text = frame.locator('body').inner_text(timeout=5000)
        detail_lines = [l.strip() for l in detail_text.split('\n') if l.strip()]
        
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
        
        mail['content'] = '\n'.join(content_lines[:15])
        
        if mail['content']:
            first_lines = mail['content'].split('\n')[:3]
            mail['summary'] = ' '.join(first_lines)[:200]
            print(f"    ✅ 已阅读，内容长度：{len(mail['content'])}")
        else:
            mail['summary'] = '无法获取正文'
            print(f"    ⚠️  无法获取正文")
        
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

# 保存邮件数据为 JSON，供 OpenClaw 创建飞书文档和表格
print("\n📊 保存邮件数据为 JSON...")

import json
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
json_file = f'D:\\openclaw-workspace\\oa_mails_{timestamp}.json'

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump({
        'analysis_time': datetime.now().isoformat(),
        'days_range': DAYS_RANGE,
        'total_mails': len(mails),
        'mails': mails
    }, f, ensure_ascii=False, indent=2)

print(f"✅ 邮件数据已保存：{json_file}")
print(f"👉 请 OpenClaw 使用飞书工具创建在线文档和表格...")

# 输出文件路径，供 OpenClaw 读取
print(f"\nJSON_FILE={json_file}")

# 保存本地备份
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
local_file = f'oa_mail_backup_{timestamp}.md'

with open(local_file, 'w', encoding='utf-8') as f:
    f.write(f"# 📧 OA 邮件分析报表\n\n")
    f.write(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"**时间范围**: 最近 {DAYS_RANGE} 天\n")
    f.write(f"**邮件总数**: {len(mails)} 封\n\n")
    
    f.write(f"**📄 飞书文档**: (待创建)\n")
    f.write(f"**📊 飞书表格**: (待创建)\n\n")
    
    f.write("## 📊 邮件列表\n\n")
    for mail in mails:
        f.write(f"### {mail['subject']}\n\n")
        f.write(f"- **发件人**: {mail['sender']}\n")
        f.write(f"- **日期**: {mail['date']}\n")
        f.write(f"- **摘要**: {mail['summary']}\n\n")

print(f"\n💾 本地备份：{local_file}")

print(f"\n🎉 邮件获取完成！")
print(f"   📊 数据文件：{json_file}")
print(f"   💾 本地备份：{local_file}")
print(f"\n👉 下一步：OpenClaw 将使用飞书工具创建在线文档和表格...")

print("\n按回车键退出...")
input()

context.close()
playwright.stop()
