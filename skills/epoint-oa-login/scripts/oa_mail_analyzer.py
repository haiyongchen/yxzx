# -*- utf-8 -*-
"""
OA 邮件分析工具 - 获取指定时间范围内的邮件并智能分类
技能版本：v1.0
"""
import sys
import os
import time
import json
from datetime import datetime, timedelta
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ==================== 可配置参数 ====================
# 时间范围（天数），默认 7 天
DAYS_RANGE = 7
# 邮件列表每页数量
PAGE_SIZE = 50
# 最大获取页数
MAX_PAGES = 10
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
        
    def launch_browser(self):
        """启动浏览器"""
        print("=" * 60)
        print("OA 邮件分析工具 v1.0")
        print("=" * 60)
        print(f"\n📅 分析时间范围：最近 {self.days_range} 天")
        print(f"📊 每页数量：{PAGE_SIZE}, 最大页数：{MAX_PAGES}")
        
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
        """检查并登录"""
        print(f"\n👉 访问邮件系统：{OA_MAIL_URL}")
        self.page.goto(OA_MAIL_URL, wait_until='networkidle', timeout=30000)
        time.sleep(3)
        
        current_url = self.page.url
        if 'login' in current_url.lower():
            print("\n⚠️  需要扫码登录")
            print("👉 请在浏览器中扫码后按回车继续...")
            input()
            time.sleep(3)
        
        print("\n✅ 登录成功")
        
    def get_mail_list(self):
        """获取邮件列表"""
        print("\n📧 获取邮件列表...")
        
        try:
            # 等待页面加载
            time.sleep(3)
            
            # 截图保存当前状态
            self.page.screenshot(path='mail_page.png')
            print("📸 已保存页面截图：mail_page.png")
            
            # 获取页面完整 HTML
            html = self.page.content()
            with open('mail_page.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("💾 已保存页面 HTML: mail_page.html")
            
            # 尝试获取 iframe
            print("\n👉 查找邮件列表 iframe...")
            
            # 方法 1: 使用 frame_locator
            try:
                frame = self.page.frame_locator('#mail-rightframe')
                print("✅ 找到 iframe 框架")
                
                # 等待邮件列表加载
                time.sleep(3)
                
                # 尝试获取邮件行
                mail_rows = None
                selectors_to_try = [
                    '.mail-list-row',
                    '.mail-item',
                    '[class*="mail-row"]',
                    '[class*="mailitem"]',
                    'tr[class*="mail"]',
                    'div[class*="mail"]',
                ]
                
                for selector in selectors_to_try:
                    try:
                        mail_rows = frame.locator(selector).all()
                        if mail_rows:
                            print(f"  使用选择器 '{selector}' 找到 {len(mail_rows)} 封邮件")
                            break
                    except:
                        continue
                
                if not mail_rows or len(mail_rows) == 0:
                    print("⚠️  未找到邮件列表，尝试直接读取页面文本...")
                    # 获取 iframe 内的文本内容
                    try:
                        frame_content = frame.locator('body').inner_text(timeout=5000)
                        print(f"  iframe 内容长度：{len(frame_content)}")
                        # 简单的邮件信息提取
                        lines = [line.strip() for line in frame_content.split('\n') if line.strip()][:50]
                        print("  前 50 行内容:")
                        for line in lines[:20]:
                            print(f"    {line[:100]}")
                    except Exception as e:
                        print(f"  获取 iframe 内容失败：{e}")
                    return
                
                # 解析邮件
                for i, row in enumerate(mail_rows[:PAGE_SIZE * MAX_PAGES]):
                    try:
                        mail_info = {
                            'index': i + 1,
                            'subject': '',
                            'sender': '',
                            'date': '',
                            'is_read': True,
                            'raw_text': ''
                        }
                        
                        # 获取整行文本
                        try:
                            mail_info['raw_text'] = row.inner_text(timeout=2000)
                        except:
                            pass
                        
                        # 尝试获取各个字段 - 使用 locator 的 children
                        try:
                            cells = row.locator('td, div, span').all()
                            for cell in cells:
                                try:
                                    text = cell.inner_text(timeout=1000).strip()
                                    if not text:
                                        continue
                                    
                                    # 简单判断：最长的文本通常是主题
                                    if len(text) > len(mail_info['subject']):
                                        mail_info['subject'] = text
                                    elif '@' in text or '.' in text:
                                        mail_info['sender'] = text
                                    elif self._is_date_format(text):
                                        mail_info['date'] = text
                                except:
                                    continue
                        except:
                            pass
                        
                        # 如果 raw_text 有内容，尝试解析
                        if mail_info['raw_text']:
                            parts = mail_info['raw_text'].split()
                            if len(parts) >= 3:
                                if not mail_info['subject']:
                                    mail_info['subject'] = ' '.join(parts[:-2])
                                if not mail_info['sender']:
                                    mail_info['sender'] = parts[-2] if len(parts) > 2 else ''
                                if not mail_info['date']:
                                    mail_info['date'] = parts[-1] if len(parts) > 1 else ''
                        
                        # 检查是否未读
                        try:
                            row_class = row.get_attribute('class', timeout=1000) or ''
                            if 'unread' in row_class.lower() or '未读' in mail_info['raw_text']:
                                mail_info['is_read'] = False
                        except:
                            pass
                        
                        # 过滤时间范围内的邮件
                        if self._is_within_date_range(mail_info['date']):
                            self.mails.append(mail_info)
                            print(f"  [{len(self.mails)}] {mail_info['subject'][:60]} | {mail_info['sender'][:20]} | {mail_info['date']}")
                        
                    except Exception as e:
                        print(f"  解析邮件 {i+1} 失败：{str(e)[:50]}")
                        continue
                
                print(f"\n✅ 共获取 {len(self.mails)} 封时间范围内的邮件")
                
            except Exception as e:
                print(f"❌ iframe 访问失败：{e}")
                # 尝试在主页面查找
                self._try_get_mails_from_main_page()
            
        except Exception as e:
            print(f"❌ 获取邮件列表失败：{e}")
            import traceback
            traceback.print_exc()
    
    def _try_get_mails_from_main_page(self):
        """尝试从主页面获取邮件"""
        print("\n👉 尝试从主页面获取邮件...")
        try:
            body_text = self.page.locator('body').inner_text(timeout=5000)
            lines = [line.strip() for line in body_text.split('\n') if line.strip()]
            print(f"  页面文本行数：{len(lines)}")
            for line in lines[:30]:
                print(f"    {line[:100]}")
        except Exception as e:
            print(f"  失败：{e}")
    
    def _is_date_format(self, text):
        """检查是否是日期格式"""
        if not text or len(text) > 30:
            return False
        date_patterns = ['-', '/', '年', '月', '日', ':']
        return any(p in text for p in date_patterns)
    
    def _is_within_date_range(self, date_str):
        """检查日期是否在指定范围内"""
        if not date_str:
            return True
        
        try:
            date_formats = [
                '%Y-%m-%d', '%Y/%m/%d',
                '%Y-%m-%d %H:%M', '%Y/%m/%d %H:%M',
                '%Y-%m-%d %H:%M:%S',
                '%m-%d', '%m/%d',
            ]
            
            for fmt in date_formats:
                try:
                    mail_date = datetime.strptime(date_str.strip(), fmt)
                    if mail_date.year == 1900:
                        mail_date = mail_date.replace(year=datetime.now().year)
                    
                    cutoff_date = datetime.now() - timedelta(days=self.days_range)
                    return mail_date >= cutoff_date
                except:
                    continue
            
            return True
        except:
            return True
    
    def analyze_and_classify(self):
        """分析并分类邮件"""
        print("\n🔍 分析邮件内容并分类...")
        
        categories = {
            '招投标': ['招标', '投标', '标书', '开标', '评标', '中标', '询价', '采购'],
            '电子商城': ['商城', '商品', '订单', '交易', '店铺', '运营', '上量', '专区', 'e 交易'],
            '培训学习': ['培训', '学习', '考试', '课程', '教程', '讲座'],
            '系统通知': ['系统', '通知', '提醒', '公告', '更新', '升级', '维护'],
            '工作汇报': ['周报', '月报', '日报', '总结', '计划', '汇报', 'SA 周报'],
            '财务相关': ['发票', '报销', '付款', '收款', '对账', '结算', '成本', '收益'],
            '会议活动': ['会议', '活动', '聚会', '座谈', '研讨'],
            '人事行政': ['人事', '考勤', '请假', '入职', '离职', '行政'],
            '技术支持': ['技术', '支持', 'bug', '问题', '故障', '运维'],
            '其他': []
        }
        
        classified = {cat: [] for cat in categories.keys()}
        
        for mail in self.mails:
            content = f"{mail['subject']} {mail['sender']} {mail['raw_text']}"
            
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
        
        # 输出分类结果
        print("\n📊 邮件分类统计:")
        total = 0
        for category, mails in classified.items():
            if mails:
                total += len(mails)
                print(f"\n  📁 {category}: {len(mails)} 封")
                for mail in mails[:5]:
                    print(f"    - {mail['subject'][:60]} | {mail['date']}")
                if len(mails) > 5:
                    print(f"    ... 还有 {len(mails) - 5} 封")
        
        if total == 0:
            print("  ⚠️  未获取到邮件，请检查登录状态和网络连接")
        
        return classified
    
    def save_report(self, classified_mails):
        """保存分析报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'oa_mail_report_{timestamp}.md'
        
        print(f"\n💾 保存分析报告：{report_file}")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# OA 邮件分析报告\n\n")
            f.write(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**时间范围**: 最近 {self.days_range} 天\n")
            f.write(f"**邮件总数**: {len(self.mails)} 封\n\n")
            
            f.write("## 分类统计\n\n")
            total = 0
            for category, mails in classified_mails.items():
                if mails:
                    f.write(f"### 📁 {category}: {len(mails)} 封\n\n")
                    total += len(mails)
                    for i, mail in enumerate(mails, 1):
                        f.write(f"{i}. **{mail['subject']}**\n")
                        f.write(f"   - 发件人：{mail['sender']}\n")
                        f.write(f"   - 日期：{mail['date']}\n")
                        f.write(f"   - 状态：{'未读' if not mail['is_read'] else '已读'}\n\n")
                    f.write("\n")
            
            f.write(f"\n**总计**: {total} 封邮件\n")
            
            # 添加使用说明
            f.write("\n---\n\n")
            f.write("## 使用说明\n\n")
            f.write("修改分析天数：编辑脚本中的 `DAYS_RANGE` 参数，或使用命令行参数：\n")
            f.write("```bash\n")
            f.write("python oa_mail_analyzer.py 15  # 分析最近 15 天\n")
            f.write("```\n")
        
        # 保存 JSON 数据
        json_file = f'oa_mail_data_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'analysis_time': datetime.now().isoformat(),
                'days_range': self.days_range,
                'total_mails': len(self.mails),
                'mails': self.mails,
                'classified': {k: [{'subject': m['subject'], 'sender': m['sender'], 'date': m['date'], 'is_read': m['is_read']} for m in v] for k, v in classified_mails.items()}
            }, f, ensure_ascii=False, indent=2)
        
        print(f"💾 保存原始数据：{json_file}")
        
        return report_file, json_file
    
    def cleanup(self):
        """清理资源"""
        print("\n✅ 分析完成！")
        print("   浏览器保持打开，按回车键退出...")
        try:
            input()
        except:
            pass
        
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()
    
    def run(self):
        """执行完整流程"""
        try:
            self.launch_browser()
            self.login_if_needed()
            self.get_mail_list()
            classified = self.analyze_and_classify()
            self.save_report(classified)
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()


if __name__ == '__main__':
    # 支持命令行参数配置天数
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
            print(f"使用命令行参数：{days} 天")
            analyzer = OAMailAnalyzer(days_range=days)
        except:
            analyzer = OAMailAnalyzer()
    else:
        analyzer = OAMailAnalyzer()
    
    analyzer.run()
