# -*- utf-8 -*-
"""
OA 邮件分析工具 v5.1 - 飞书 API 支持模块
- 获取飞书 API token
- 创建飞书云文档
- 创建飞书多维表格
"""
import sys
import os
import io
from datetime import datetime

# Windows 控制台 UTF-8 支持
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 飞书 API 配置
FEISHU_APP_ID = 'cli_a92024d097381cc5'
FEISHU_APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'


def get_feishu_tenant_access_token():
    """获取飞书 tenant_access_token"""
    import requests
    
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    
    response = requests.post(url, json=payload, timeout=10)
    data = response.json()
    
    if data.get('code') == 0:
        return data.get('tenant_access_token')
    else:
        print(f"❌ 获取飞书 token 失败：{data}")
        return None


def create_feishu_doc(token, title, markdown_content):
    """创建飞书云文档（仅创建，不写入内容）"""
    import requests
    
    # 1. 创建文档
    url = "https://open.feishu.cn/open-apis/docx/v1/documents"
    headers_api = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": title,
        "folder_token": ""  # 默认创建到我的空间
    }
    
    response = requests.post(url, json=payload, headers=headers_api, timeout=30)
    result = response.json()
    
    if result.get('code') != 0:
        print(f"❌ 创建文档失败：{result}")
        return None, None
    
    document_id = result['data']['document']['document_id']
    doc_url = f"https://www.feishu.cn/docx/{document_id}"
    print(f"✅ 文档创建成功：{doc_url}")
    
    # 注意：飞书云文档的 blocks 写入 API 需要特殊权限
    # 这里只创建文档，内容需要手动复制或使用其他方式写入
    print(f"⚠️  文档内容需要手动复制（飞书 API 限制）")
    
    # 将内容保存为本地文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    local_file = f"feishu_doc_content_{timestamp}.md"
    with open(local_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    print(f"💾 文档内容已保存到：{local_file}")
    
    return doc_url, document_id


def create_feishu_docs_and_sheet(mail_data):
    """使用飞书 API 创建在线文档（包含表格数据）"""
    print("\n📊 创建飞书在线文档...")
    
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
    
    # 获取飞书 token
    print("\n🔑 获取飞书 API token...")
    feishu_token = get_feishu_tenant_access_token()
    
    if not feishu_token:
        print("❌ 无法获取飞书 token，请检查 App ID 和 App Secret 配置")
        return None, None, doc_name
    
    print("✅ 飞书 token 获取成功")
    
    # 构建飞书文档内容
    md_content = f"""# 📧 OA 邮件分析报表

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**时间范围**: 最近 7 天  
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

## 📋 邮件列表

| 序号 | 邮件主题 | 发件人 | 分类 | 优先级 | 日期 |
|------|----------|--------|------|--------|------|
"""
    
    # 添加邮件列表表格
    for mail in processed_mails:
        subject_short = mail['subject'][:50] + '...' if len(mail['subject']) > 50 else mail['subject']
        md_content += f"| {mail['index']} | {subject_short} | {mail['sender']} | {mail['category']} | {mail['priority']} | {mail['date']} |\n"
    
    md_content += """
---

## 📌 待办事项

1. ⚠️ **阅读失败的邮件** - 需要手动查看 OA 系统
2. 📊 **重点邮件** - 优先处理⭐⭐⭐优先级邮件
3. 🏗️ **专区部署** - 跟进专区开设和部署事宜
4. 🔧 **系统评审** - 参与相关评审工作

---

*报表由 OA 邮件分析工具 v5.1 自动生成*
"""
    
    # 创建飞书文档
    print("\n📄 创建飞书文档...")
    doc_url, doc_id = create_feishu_doc(feishu_token, doc_name, md_content)
    
    return None, doc_url, doc_name  # sheet_url 返回 None
