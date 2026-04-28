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
OA_MAIL_RECEIVE_LIST = "https://oa.epoint.com.cn:8080/OA9/oa9/mail/mailreceivelist"

# Cookie 文件路径
COOKIES_FILE = os.path.join(USER_DATA_DIR, "Default", "Network", "Cookies")


class OAMailAnalyzer:
    """OA 邮件分析器"""
    
    def __init__(self, days_range=DAYS_RANGE):
        self.days_range = days_range
        self.playwright = None
        self.context = None
        self.page = None
        self.mails = []
        
    def check_cookies(self):
        """检查 Cookie 是否有效"""
        import os
        from datetime import datetime, timedelta
        
        if not os.path.exists(COOKIES_FILE):
            return False, "Cookie 文件不存在"
        
        # 检查文件修改时间（如果超过 7 天可能过期）
        mtime = datetime.fromtimestamp(os.path.getmtime(COOKIES_FILE))
        age = datetime.now() - mtime
        
        if age.days > 7:
            return False, f"Cookie 可能已过期（{age.days}天前）"
        
        return True, f"Cookie 有效（{age.seconds // 3600}小时前更新）"
    
    def launch_browser(self):
        """启动浏览器"""
        print("=" * 60)
        print("OA 邮件分析工具 v1.0")
        print("=" * 60)
        print(f"\n📅 分析时间范围：最近 {self.days_range} 天")
        print(f"📊 每页数量：{PAGE_SIZE}, 最大页数：{MAX_PAGES}")
        
        # 先检查 Cookie 状态
        print("\n🍪 检查 Cookie 状态...")
        valid, message = self.check_cookies()
        if valid:
            print(f"✅ {message}")
        else:
            print(f"⚠️  {message}")
        
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
        
        # 检查是否需要登录
        if 'login' in current_url.lower() or 'oauth2login' in current_url.lower():
            print("\n⚠️  Cookie 已过期，需要扫码登录")
            print("👉 请在浏览器中扫码后按回车继续...")
            input()
            time.sleep(3)
            
            # 等待登录完成
            try:
                with self.page.expect_navigation(timeout=15000):
                    pass
            except:
                pass
            time.sleep(2)
            
            # 再次检查
            current_url = self.page.url
            if 'login' in current_url.lower():
                print("\n❌ 登录未完成，退出")
                raise Exception("登录失败")
            
            print("\n✅ 登录成功，Cookie 已更新")
        else:
            print("\n✅ Cookie 有效，已自动登录")
        
        print(f"   当前页面：{self.page.title()}")
        
    def get_mail_list(self):
        """获取邮件列表"""
        print("\n📧 获取邮件列表...")
        
        try:
            # 直接访问邮件列表页面（不是首页）
            print(f"👉 直接访问邮件列表：{OA_MAIL_RECEIVE_LIST}")
            self.page.goto(OA_MAIL_RECEIVE_LIST, wait_until='networkidle', timeout=30000)
            time.sleep(3)
            
            # 检查是否被跳转到登录页
            current_url = self.page.url
            if 'login' in current_url.lower():
                print("\n⚠️  Cookie 已失效，需要重新登录")
                return
            
            # 截图保存当前状态
            self.page.screenshot(path='mail_page.png')
            print("📸 已保存页面截图：mail_page.png")
            
            # 尝试获取 iframe
            print("\n👉 查找邮件列表 iframe...")
            
            # 使用 frame_locator
            try:
                frame = self.page.frame_locator('#mail-rightframe')
                print("✅ 找到 iframe 框架")
                
                # 等待邮件列表加载
                time.sleep(3)
                
                # 获取邮件列表容器
                mail_list_container = frame.locator('.mail-list-container, .mini-datagrid-view, [class*="maillist"]')
                
                # 尝试获取邮件行
                mail_rows = None
                selectors_to_try = [
                    '.mail-list-row',
                    '.mini-datagrid-row',
                    '[class*="mailitem"]',
                    'tr[class*="row"]',
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
                    print("⚠️  未找到标准邮件列表，尝试获取所有文本...")
                    self._extract_mails_from_text(frame)
                    return
                
                # 解析邮件
                for i, row in enumerate(mail_rows[:PAGE_SIZE * MAX_PAGES]):
                    mail_info = self._parse_mail_row(row, i)
                    if mail_info and self._is_within_date_range(mail_info['date']):
                        self.mails.append(mail_info)
                        print(f"  [{len(self.mails)}] {mail_info['subject'][:60]} | {mail_info['sender'][:20]} | {mail_info['date']}")
                
                print(f"\n✅ 共获取 {len(self.mails)} 封时间范围内的邮件")
                
            except Exception as e:
                print(f"❌ iframe 访问失败：{e}")
                self._try_get_mails_from_main_page()
            
        except Exception as e:
            print(f"❌ 获取邮件列表失败：{e}")
            import traceback
            traceback.print_exc()
    
    def _parse_mail_row(self, row, index):
        """解析邮件行"""
        try:
            mail_info = {
                'index': index + 1,
                'subject': '',
                'sender': '',
                'date': '',
                'is_read': True,
                'raw_text': ''
            }
            
            # 获取整行文本
            try:
                mail_info['raw_text'] = row.inner_text(timeout=2000).strip()
            except:
                pass
            
            # 如果没有内容，跳过
            if not mail_info['raw_text'] or len(mail_info['raw_text']) < 5:
                return None
            
            # 尝试获取子元素
            try:
                cells = row.locator('td, div, span').all()
                for cell in cells:
                    try:
                        text = cell.inner_text(timeout=1000).strip()
                        if not text:
                            continue
                        
                        # 简单判断
                        if len(text) > len(mail_info['subject']) and len(text) < 200:
                            mail_info['subject'] = text
                        elif '@' in text or ('.' in text and len(text) < 50):
                            mail_info['sender'] = text
                        elif self._is_date_format(text):
                            mail_info['date'] = text
                    except:
                        continue
            except:
                pass
            
            # 检查是否未读
            try:
                row_class = row.get_attribute('class', timeout=1000) or ''
                if 'unread' in row_class.lower() or '未读' in mail_info['raw_text']:
                    mail_info['is_read'] = False
            except:
                pass
            
            # 如果主题还是空的，尝试从 raw_text 提取
            if not mail_info['subject'] and mail_info['raw_text']:
                lines = [l.strip() for l in mail_info['raw_text'].split('\n') if l.strip()]
                # 过滤掉 UI 噪音
                meaningful_lines = [
                    l for l in lines 
                    if len(l) > 3 
                    and not any(kw in l for kw in ['关键字', '搜索', '重置', '关闭', '每页', '条', '全文检索', '包含'])
                ]
                if meaningful_lines:
                    mail_info['subject'] = meaningful_lines[0]
                    if len(meaningful_lines) > 1:
                        mail_info['sender'] = meaningful_lines[-2] if len(meaningful_lines) > 1 else ''
                        mail_info['date'] = meaningful_lines[-1] if len(meaningful_lines) > 0 else ''
            
            # 跳过明显是 UI 元素的行
            if any(kw in mail_info['raw_text'] for kw in ['关键字：', '搜索范围：', '发件时间：', '每页', '条，共', '/ 367']):
                return None
            
            return mail_info
            
        except Exception as e:
            print(f"  解析邮件 {index+1} 失败：{str(e)[:50]}")
            return None
    
    def _extract_mails_from_text(self, frame):
        """从文本中提取邮件"""
        print("\n👉 从文本中提取邮件...")
        try:
            # 等待 iframe 内容加载
            time.sleep(2)
            
            # 尝试多种方式获取内容
            body_text = None
            
            # 方法 1: 直接获取 body 文本
            try:
                body_text = frame.locator('body').inner_text(timeout=3000)
            except:
                pass
            
            # 方法 2: 获取邮件列表容器
            if not body_text:
                try:
                    mail_list = frame.locator('.mail-list-container, .mini-datagrid').inner_text(timeout=3000)
                    body_text = mail_list
                except:
                    pass
            
            # 方法 3: 获取所有可见文本
            if not body_text:
                try:
                    body_text = frame.locator('html').inner_text(timeout=3000)
                except:
                    pass
            
            if not body_text:
                print("  ⚠️  无法获取 iframe 内容")
                return
            
            lines = [line.strip() for line in body_text.split('\n') if line.strip()]
            
            # 过滤 UI 噪音
            meaningful_lines = []
            for line in lines:
                if (len(line) > 5 and 
                    not any(kw in line for kw in ['关键字', '搜索', '重置', '关闭', '每页', '条', '全文检索', '包含', '发件时间', '至', '共'])):
                    meaningful_lines.append(line)
            
            print(f"  过滤后剩余 {len(meaningful_lines)} 行")
            
            # 每 3 行作为一封邮件（主题、发件人、日期）
            for i in range(0, len(meaningful_lines), 3):
                mail_info = {
                    'index': len(self.mails) + 1,
                    'subject': meaningful_lines[i] if i < len(meaningful_lines) else '',
                    'sender': meaningful_lines[i+1] if i+1 < len(meaningful_lines) else '',
                    'date': meaningful_lines[i+2] if i+2 < len(meaningful_lines) else '',
                    'is_read': True,
                    'raw_text': ' '.join(meaningful_lines[i:i+3])
                }
                
                if mail_info['subject'] and len(mail_info['subject']) > 3 and self._is_within_date_range(mail_info['date']):
                    self.mails.append(mail_info)
                    print(f"  [{len(self.mails)}] {mail_info['subject'][:60]} | {mail_info['date']}")
            
        except Exception as e:
            print(f"  提取失败：{e}")
    
    def _try_get_mails_from_main_page(self):
        """尝试从主页面获取邮件"""
        print("\n👉 尝试从主页面获取邮件...")
        try:
            body_text = self.page.locator('body').inner_text(timeout=5000)
            lines = [line.strip() for line in body_text.split('\n') if line.strip()]
            print(f"  页面文本行数：{len(lines)}")
        except Exception as e:
            print(f"  失败：{e}")
    
    def _is_date_format(self, text):
        """检查是否是日期格式"""
        if not text or len(text) > 30 or len(text) < 3:
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
                '%A %H:%M',  # 星期一 13:39
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
            
            # 如果是"星期一"这种格式，简单判断
            weekday_map = {
                '星期一': 0, '星期二': 1, '星期三': 2, '星期四': 3,
                '星期五': 4, '星期六': 5, '星期日': 6
            }
            for day_name, offset in weekday_map.items():
                if day_name in date_str:
                    # 假设是最近一周内的
                    return offset <= 1  # 只接受星期一、星期二的
            
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
                    subject = mail['subject'][:60].replace('\n', ' ').strip()
                    print(f"    - {subject} | {mail['date']}")
                if len(mails) > 5:
                    print(f"    ... 还有 {len(mails) - 5} 封")
        
        if total == 0:
            print("  ⚠️  未获取到有效邮件，请检查登录状态和网络连接")
        
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
                        subject = mail['subject'].replace('\n', ' ').strip()
                        f.write(f"{i}. **{subject}**\n")
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
                'classified': {
                    k: [
                        {
                            'subject': m['subject'],
                            'sender': m['sender'],
                            'date': m['date'],
                            'is_read': m['is_read']
                        } for m in v
                    ] for k, v in classified_mails.items()
                }
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
