# -*- utf-8 -*-
"""
OA 日志填写工具
"""
import sys
import io
import subprocess
import json
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# OA API 脚本路径
OA_API_SCRIPT = r"D:\openclaw-workspace\skills\oa-diary\oa\scripts\oa_api.py"

def call_oa_api(api_path, params):
    """调用 OA API"""
    cmd = [sys.executable, OA_API_SCRIPT, api_path, json.dumps(params, ensure_ascii=False)]
    print(f"👉 调用 API: {api_path}")
    print(f"   参数：{params}")
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, encoding='utf-8')
    
    if result.returncode == 0:
        try:
            return json.loads(result.stdout.strip())
        except:
            print(f"❌ 响应解析失败：{result.stdout[:200]}")
            return None
    else:
        print(f"❌ 调用失败：{result.stderr[:200]}")
        return None

def submit_daily_report(work_content, project_name="日常运维", work_hours="8", complete_percent=100):
    """提交工作日志"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    print(f"\n📝 准备提交 {today} 的工作日志...")
    print(f"   工作内容：{work_content}")
    print(f"   项目名称：{project_name}")
    print(f"   工作时长：{work_hours} 小时")
    print(f"   完成度：{complete_percent}%")
    
    # 1. 检查用户状态
    print("\n1️⃣ 检查用户状态...")
    check_result = call_oa_api('rz_checkuser_v2', {'rzdate': today})
    
    if not check_result:
        print("❌ 无法检查用户状态")
        return False
    
    # 2. 获取工作类型字典
    print("\n2️⃣ 获取工作类型...")
    worktype_result = call_oa_api('rz_select_gzdworktype_v1', {'parentareacode': ''})
    
    # 3. 插入日志明细
    print("\n3️⃣ 提交日志...")
    
    # 注意：实际调用需要 rzguid, missionguid 等参数，这些需要从其他接口获取
    # 这里简化处理，先查询当日是否已有日志
    query_result = call_oa_api('rz_select_rzinfo_list_v1', {
        'fromdate': today,
        'todate': today
    })
    
    if query_result and 'custom' in query_result and 'rzinfo' in query_result['custom']:
        existing_logs = query_result['custom']['rzinfo']
        if existing_logs:
            print(f"⚠️  今日已提交 {len(existing_logs)} 条日志")
            for log in existing_logs:
                print(f"   - {log.get('missionname', 'N/A')}: {log.get('gongzuonr', 'N/A')[:50]}")
        else:
            print("✅ 今日尚未提交日志")
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("OA 日志填写工具 v1.0")
    print("=" * 60)
    
    # 示例工作内容
    work_content = """
1. OA 邮件分析工具优化
   - 修复飞书 API 调用问题
   - 实现邮件自动分类和优先级标注
   - 生成飞书在线文档和表格

2. 招投标系统支持
   - 处理 AI 评标系统废标异常排查
   - 支持沈阳试点项目私有模型部署

3. 电子商城运营
   - 山东兴多专区开设（年保底 130 个项目）
   - 武汉光谷专区合作协议（五五分成）
   - 新疆阳光采购平台推广上量
"""
    
    success = submit_daily_report(work_content.strip())
    
    if success:
        print("\n✅ 日志处理完成！")
    else:
        print("\n❌ 日志处理失败，需要扫码登录或手动处理")
    
    print("\n按回车键退出...")
    input()
