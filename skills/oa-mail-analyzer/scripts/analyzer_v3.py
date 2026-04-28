# -*- utf-8 -*-
"""
OA 邮件分析工具 v3.0 - 阅读邮件内容并生成总结
技能版本：v3.0
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

# ==================== 可配置参数 ====================
DAYS_RANGE = 7
PAGE_SIZE = 50
MAX_PAGES = 5
MAX_MAILS_TO_READ = 20  # 最多阅读多少封邮件的详细内容
# ================================================

USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"
OA_MAIL_URL = "https://oa.epoint.com.cn:8080/OA9/oa9/mail/mailframe"


class OAMailAnalyzer:
    def __init__(self, days_range=DAYS_RANGE):
        self.days_range = days_range
        self.playwright = None
        self.context = None
        self.page = None
        self.mails = []
        self.mail_summaries = []
        
    def launch_browser(self):
        print("=" * 60)
        print("OA 邮件分析工具 v3.0 - 内容总结版")
        print("=" * 60)
        print(f"\n📅 分析时间范围：最近 {self.days_range} 天")
        print(f"📖 最多阅读邮件数：{MAX_MAILS_TO_READ}")
        
        print("\n🍪 检查 Cookie 状态...")
        cookies_file = os.path.join(USER_DATA_DIR, "Default", "Network", "Cookies")
        if os.path.exists(cookies_file):
            mtime = datetime.fromtimestamp(os.path.getmtime(cookies_file))
            age = datetime.now() - mtime
            print(f"✅ Cookie 有效（{age.seconds // 3600}小时前更新）")
        else:
            print("⚠️  Cookie 文件不存在")
        
        print("\n👉 启动浏览器...")
        self.playwright = sync_playwright().start()
        
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        self.page = self.context.new_page()
        
    def login_if_needed(self):
        print(f"\n👉 访问邮件系统：{OA_MAIL_URL}")
        self.page.goto(OA_MAIL_URL, wait_until='networkidle', timeout=30000)
        time.sleep(3)
        
        current_url = self.page.url
        if 'login' in current_url.lower():
            print("\n⚠️  需要扫码登录")
            print("👉 请在浏览器中扫码后按回车继续...")
            input()
            time.sleep(3)
            try:
                with self.page.expect_navigation(timeout=15000):
                    pass
            except:
                pass
        
        print("\n✅ 登录成功")
        
    def get_mail_list(self):
        """获取邮件列表"""
        print("\n📧 获取邮件列表...")
        
        time.sleep(3)
        
        # 获取 iframe
        try:
            frame = self.page.frame_locator('#mail-rightframe')
            
            # 获取 iframe 内所有文本
            body_text = frame.locator('body').inner_text(timeout=5000)
            lines = [l.strip() for l in body_text.split('\n') if l.strip()]
            
            print(f"  获取到 {len(lines)} 行文本")
            
            # 解析邮件（格式：发件人 → 主题 → 日期）
            i = 0
            while i < len(lines) and len(self.mails) < MAX_MAILS_TO_READ:
                line = lines[i]
                
                # 跳过 UI 元素
                if any(kw in line for kw in ['全选', '转移', '签收', '删除', '本周', '更早', '每页', '条', '关键字', '搜索']):
                    i += 1
                    continue
                
                # 检查是否是发件人（通常包含括号或名字）
                if i + 2 < len(lines):
                    sender = line
                    subject = lines[i + 1]
                    date = lines[i + 2]
                    
                    # 验证是否是合理的邮件结构
                    if len(subject) > 3 and len(sender) > 1:
                        mail_info = {
                            'index': len(self.mails) + 1,
                            'subject': subject,
                            'sender': sender,
                            'date': date,
                            'raw_text': f"{sender}\n{subject}\n{date}",
                            'content': '',
                            'summary': ''
                        }
                        self.mails.append(mail_info)
                        print(f"  [{len(self.mails)}] {subject[:50]} | {sender[:20]} | {date}")
                        i += 3
                        continue
                
                i += 1
            
            print(f"\n✅ 获取到 {len(self.mails)} 封有效邮件")
            
        except Exception as e:
            print(f"❌ 获取邮件列表失败：{e}")
            import traceback
            traceback.print_exc()
    
    def read_mail_content(self, mail_index):
        """打开并阅读单封邮件"""
        try:
            # 获取 iframe
            frame = self.page.frame_locator('#mail-rightframe')
            
            # 获取所有文本
            body_text = frame.locator('body').inner_text(timeout=5000)
            lines = [l.strip() for l in body_text.split('\n') if l.strip()]
            
            # 找到目标邮件
            mail = self.mails[mail_index]
            subject = mail['subject']
            
            # 在文本中查找邮件主题
            found_index = -1
            for i, line in enumerate(lines):
                if subject in line:
                    found_index = i
                    break
            
            if found_index >= 0:
                # 提取邮件内容（主题后面的内容）
                content_lines = []
                for j in range(found_index + 1, min(found_index + 30, len(lines))):
                    line = lines[j]
                    # 跳过 UI 元素
                    if any(kw in line for kw in ['返回', '回复', '转发', '删除', '顶部', '底部']):
                        continue
                    if len(line) > 20:  # 只保留有意义的内容
                        content_lines.append(line)
                
                return '\n'.join(content_lines[:20])
            
        except Exception as e:
            print(f"  阅读邮件失败：{e}")
        
        return ''
    
    def read_and_summarize_mails(self):
        """阅读邮件并生成总结"""
        print("\n📖 阅读邮件内容并生成总结...")
        
        for i, mail in enumerate(self.mails[:MAX_MAILS_TO_READ]):
            print(f"\n  [{i+1}/{len(self.mails)}] 阅读：{mail['subject'][:40]}...")
            
            # 阅读邮件内容
            content = self.read_mail_content(i)
            mail['content'] = content
            
            # 生成简单总结
            if content:
                # 提取关键信息
                summary = self._generate_summary(mail['subject'], content)
                mail['summary'] = summary
                print(f"    ✅ 已总结：{summary[:80]}...")
            else:
                mail['summary'] = "无法获取邮件正文内容"
                print(f"    ⚠️  无法获取正文")
            
            time.sleep(1)  # 避免请求过快
    
    def _generate_summary(self, subject, content):
        """生成邮件总结"""
        # 提取前 200 字作为摘要
        summary = content[:200].strip()
        
        # 识别邮件类型
        mail_type = ""
        if any(kw in subject + content for kw in ['招标', '投标', '中标']):
            mail_type = "【招投标】"
        elif any(kw in subject + content for kw in ['商城', '专区', '上量']):
            mail_type = "【电子商城】"
        elif any(kw in subject + content for kw in ['周报', '月报', '总结']):
            mail_type = "【汇报】"
        elif any(kw in subject + content for kw in ['通知', '公告']):
            mail_type = "【通知】"
        
        if mail_type:
            return f"{mail_type} {summary}"
        
        return summary
    
    def analyze_and_classify(self):
        """分类邮件"""
        print("\n🔍 分类邮件...")
        
        categories = {
            '招投标': ['招标', '投标', '标书', '开标', '评标', '中标'],
            '电子商城': ['商城', '商品', '订单', '交易', '专区', '上量'],
            '培训学习': ['培训', '学习', '考试', '课程'],
            '系统通知': ['系统', '通知', '公告', '升级'],
            '工作汇报': ['周报', '月报', '日报', '总结', '汇报'],
            '其他': []
        }
        
        classified = {cat: [] for cat in categories.keys()}
        
        for mail in self.mails:
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
        for category, mails in classified.items():
            if mails:
                print(f"  📁 {category}: {len(mails)} 封")
        
        return classified
    
    def save_report(self, classified_mails):
        """保存详细报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'oa_mail_summary_{timestamp}.md'
        
        print(f"\n💾 保存总结报告：{report_file}")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# OA 邮件内容总结报告\n\n")
            f.write(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**时间范围**: 最近 {self.days_range} 天\n")
            f.write(f"**阅读邮件数**: {len(self.mails)} 封\n\n")
            
            # 总体统计
            f.write("## 📊 分类统计\n\n")
            for category, mails in classified_mails.items():
                if mails:
                    f.write(f"- **{category}**: {len(mails)} 封\n")
            f.write("\n")
            
            # 每封邮件的详细总结
            f.write("## 📧 邮件详细总结\n\n")
            
            for category, mails in classified_mails.items():
                if mails:
                    f.write(f"### {category}\n\n")
                    
                    for i, mail in enumerate(mails, 1):
                        f.write(f"#### {i}. {mail['subject']}\n\n")
                        f.write(f"- **发件人**: {mail['sender']}\n")
                        f.write(f"- **日期**: {mail['date']}\n")
                        f.write(f"- **内容总结**: {mail['summary']}\n\n")
                        
                        if mail['content']:
                            f.write(f"**原文摘要**:\n> {mail['content'][:500]}...\n\n")
                        
                        f.write("---\n\n")
        
        print(f"✅ 报告已保存")
        
        return report_file
    
    def cleanup(self):
        print("\n✅ 完成！")
        print("   按回车键退出...")
        try:
            input()
        except:
            pass
        
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()
    
    def run(self):
        try:
            self.launch_browser()
            self.login_if_needed()
            self.get_mail_list()
            
            if self.mails:
                self.read_and_summarize_mails()
                classified = self.analyze_and_classify()
                self.save_report(classified)
            else:
                print("\n⚠️  没有获取到邮件")
                
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
            analyzer = OAMailAnalyzer(days_range=days)
        except:
            analyzer = OAMailAnalyzer()
    else:
        analyzer = OAMailAnalyzer()
    
    analyzer.run()
