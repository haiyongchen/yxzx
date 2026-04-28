# -*- utf-8 -*-
"""
OA 邮件分析工具 v2.0 - 使用 API 方式获取邮件
技能版本：v2.0
"""
import sys
import os
import time
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ==================== 可配置参数 ====================
# 时间范围（天数），默认 7 天
DAYS_RANGE = 7
# 每页邮件数
PAGE_SIZE = 50
# 最大页数
MAX_PAGES = 10
# ================================================

# OA API 配置
OA_API_BASE = "https://oa.epoint.com.cn/oaextend/rest"
OA_MAIL_API = f"{OA_API_BASE}/dynamicapi/mail_getunreadlist_v7"

# Cookie 文件路径（用于 playwright）
USER_DATA_DIR = r"D:\work\运营中心\yxzx\新点 e 交易相关材料\日常数据运维工具\OAuto\oa_user_data"


class OAMailAnalyzer:
    """OA 邮件分析器 - API 版本"""
    
    def __init__(self, days_range=DAYS_RANGE):
        self.days_range = days_range
        self.token = None
        self.mails = []
        
    def check_cookies(self):
        """检查 Cookie 状态"""
        cookies_file = os.path.join(USER_DATA_DIR, "Default", "Network", "Cookies")
        
        if not os.path.exists(cookies_file):
            return False, "Cookie 文件不存在"
        
        mtime = datetime.fromtimestamp(os.path.getmtime(cookies_file))
        age = datetime.now() - mtime
        
        if age.days > 7:
            return False, f"Cookie 可能已过期（{age.days}天前）"
        
        return True, f"Cookie 有效（{age.seconds // 3600}小时前更新）"
    
    def get_token(self):
        """获取 API Token（通过扫码）"""
        print("\n🔑 获取 API Token...")
        
        # 使用 oa_api.py 脚本获取 token
        script_path = r"D:\openclaw-workspace\skills\epoint-oa-api\scripts\oa_api.py"
        
        if not os.path.exists(script_path):
            print("❌ 找不到 oa_api.py 脚本")
            return False
        
        # 尝试调用 API，如果 token 不存在会自动提示扫码
        import subprocess
        
        try:
            # 先测试调用
            result = subprocess.run(
                [sys.executable, script_path, "mail_getunreadlist_v7", '{"currentpageindex": 0, "pagesize": 1}'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if "未找到本地 Token" in result.stdout or "未找到本地 Token" in result.stderr:
                print("\n⚠️  需要扫码授权 API 访问")
                print("👉 请在弹出的二维码中使用 OA App 扫码")
                subprocess.run(
                    [sys.executable, script_path, "mail_getunreadlist_v7", '{"currentpageindex": 0, "pagesize": 1}'],
                    timeout=60
                )
            
            print("✅ Token 获取成功")
            return True
            
        except subprocess.TimeoutExpired:
            print("⏱️  扫码超时，请重试")
            return False
        except Exception as e:
            print(f"❌ 获取 Token 失败：{e}")
            return False
    
    def fetch_mails(self):
        """获取邮件列表"""
        print("\n📧 获取邮件列表...")
        
        script_path = r"D:\openclaw-workspace\skills\epoint-oa-api\scripts\oa_api.py"
        
        all_mails = []
        page = 0
        
        while page < MAX_PAGES:
            print(f"\n  获取第 {page + 1} 页...")
            
            params = json.dumps({
                "currentpageindex": page,
                "pagesize": PAGE_SIZE
            })
            
            import subprocess
            try:
                result = subprocess.run(
                    [sys.executable, script_path, "mail_getunreadlist_v7", params],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    encoding='utf-8'
                )
                
                # 解析返回的 JSON
                try:
                    data = json.loads(result.stdout.strip())
                    
                    if 'record' in data or 'items' in data or 'data' in data:
                        mails = data.get('record', data.get('items', data.get('data', [])))
                        
                        if not mails:
                            print("  没有更多邮件了")
                            break
                        
                        for mail in mails:
                            mail_info = {
                                'subject': mail.get('subject', mail.get('title', '')),
                                'sender': mail.get('sender', mail.get('sendername', '')),
                                'date': mail.get('senddate', mail.get('date', '')),
                                'is_read': mail.get('isread', True),
                                'raw_data': mail
                            }
                            all_mails.append(mail_info)
                            print(f"    [{len(all_mails)}] {mail_info['subject'][:60]} | {mail_info['date']}")
                        
                        if len(mails) < PAGE_SIZE:
                            break
                        
                        page += 1
                    else:
                        print(f"  返回数据格式异常：{result.stdout[:200]}")
                        break
                        
                except json.JSONDecodeError as e:
                    print(f"  JSON 解析失败：{e}")
                    print(f"  原始输出：{result.stdout[:200]}")
                    break
                    
            except subprocess.TimeoutExpired:
                print("  请求超时")
                break
            except Exception as e:
                print(f"  请求失败：{e}")
                break
        
        # 过滤时间范围内的邮件
        print(f"\n📅 过滤最近 {self.days_range} 天的邮件...")
        cutoff_date = datetime.now() - timedelta(days=self.days_range)
        
        filtered_mails = []
        for mail in all_mails:
            if self._is_within_date_range(mail['date'], cutoff_date):
                filtered_mails.append(mail)
        
        self.mails = filtered_mails
        print(f"✅ 共获取 {len(filtered_mails)} 封时间范围内的邮件")
        
        return filtered_mails
    
    def _is_date_format(self, text):
        """检查是否是日期格式"""
        if not text or len(text) > 30 or len(text) < 3:
            return False
        date_patterns = ['-', '/', '年', '月', '日', ':']
        return any(p in text for p in date_patterns)
    
    def _is_within_date_range(self, date_str, cutoff_date=None):
        """检查日期是否在指定范围内"""
        if not date_str:
            return True
        
        if cutoff_date is None:
            cutoff_date = datetime.now() - timedelta(days=self.days_range)
        
        try:
            date_formats = [
                '%Y-%m-%d', '%Y/%m/%d',
                '%Y-%m-%d %H:%M', '%Y/%m/%d %H:%M',
                '%Y-%m-%d %H:%M:%S',
            ]
            
            for fmt in date_formats:
                try:
                    mail_date = datetime.strptime(date_str.strip(), fmt)
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
            content = f"{mail['subject']} {mail['sender']}"
            
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
            print("  ⚠️  未获取到有效邮件")
        
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
            f.write("\n---\n\n")
            f.write("## 使用说明\n\n")
            f.write("修改分析天数：编辑脚本中的 `DAYS_RANGE` 参数，或使用命令行参数：\n")
            f.write("```bash\n")
            f.write("python oa_mail_analyzer_api.py 15  # 分析最近 15 天\n")
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
                    k: [{'subject': m['subject'], 'sender': m['sender'], 'date': m['date'], 'is_read': m['is_read']} for m in v]
                    for k, v in classified_mails.items()
                }
            }, f, ensure_ascii=False, indent=2)
        
        print(f"💾 保存原始数据：{json_file}")
        
        return report_file, json_file
    
    def run(self):
        """执行完整流程"""
        try:
            print("=" * 60)
            print("OA 邮件分析工具 v2.0 (API 版本)")
            print("=" * 60)
            print(f"\n📅 分析时间范围：最近 {self.days_range} 天")
            
            # 检查 Cookie
            print("\n🍪 检查 Cookie 状态...")
            valid, message = self.check_cookies()
            if valid:
                print(f"✅ {message}")
            else:
                print(f"⚠️  {message}")
            
            # 获取 Token
            if not self.get_token():
                print("\n❌ 无法获取 API Token，退出")
                return
            
            # 获取邮件
            self.fetch_mails()
            
            # 分析分类
            classified = self.analyze_and_classify()
            
            # 保存报告
            self.save_report(classified)
            
            print("\n✅ 分析完成！")
            
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            import traceback
            traceback.print_exc()


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
