# -*- utf-8 -*-
import requests
import json

APP_ID = 'cli_a92024d097381cc5'
APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM'
SPREADSHEET_TOKEN = 'SO2Xs2vlkh4XKNt0VfOclqWYn6g'

# 获取 Token
resp = requests.post('https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal', 
                     json={'app_id': APP_ID, 'app_secret': APP_SECRET}, timeout=30)
app_token = resp.json().get('app_access_token')
print(f'✅ Token: {app_token[:50]}...')

# 准备数据
values = [
    ["序号", "邮件主题", "发件人", "分类", "优先级", "邮件地址", "内容总结"],
    ["1", "【阳光优采】关于近期平台上量过程中的问题及工作建议总结梳理", "李涛 (运营中心)", "电子商城", "⭐⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "6 大问题 +5 项建议：商品类型缺失（墨盒缺黑色、信创类、工业品）、新增商品流程慢（中资侧积压 3 月合同未审）、价格偏高（得力硒鼓高 7%）、供应商少（多数专区仅 4-5 家电商）、审核积压、理念局限（三家比价）。建议：联合电商沟通、引入本地供应商、价格巡查、深化中资合作、举办合规座谈会"],
    ["2", "【规范评审】服务器预规划流程增加 pinpoint 监控", "包亚峰", "系统通知", "⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "所有新立项重点项目（T 级、A 级、省级等）在服务器预规划和正式规划时，均需部署 Pinpoint 监控体系，用于快速追踪问题链路。期望 4 月 22 日下班前反馈"],
    ["3", "【商城专区开设】武汉光谷联合产权交易所黄石分公司", "罗永健", "电子商城", "⭐⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "与光谷联合产权交易所黄石分公司达成五五分成协议，建设黄石企业采购商城云平台，双方共同争取政策支持，加快在黄石市及全省应用推广。附件：合作协议.pdf"],
    ["4", "AI 评标系统废标情况查询", "沙宏宇", "招投标", "⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "招标代理反馈技术标废标异常：标段 E210106ET09000004001001，技术标个人打分表显示【大连众亿建筑工程有限公司】在两个评分点被废标，但实际废标结果显示另外两家单位。需协助排查，可能涉及项目复评"],
    ["5", "新疆阳光采购平台升级后市场推广上量事宜", "庞丹枫", "电子商城", "⭐⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "新疆平台参加国资委培训会议，明确平台定位。近期对 3 家国企（新疆机场集团、新疆有色技术集团、新疆文旅投集团）进行入企推广讲座。需优化 PPT：政策解读、8.0 系统功能、阳光优采商城、监管系统、智能辅助评标、远程异地评标等"],
    ["6", "山东兴多专区提取部署事宜", "庞鑫", "电子商城", "⭐⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "山东兴多项目管理有限公司（临沂前五代理）有意转向电子标，全年预估 100-200 个项目，约定年保底 130 个项目，连续两个月无项目则下线。合同法务审核中，申请提前开设专区"],
    ["7", "营销周报（4.7-4.10）", "徐志远", "招投标", "⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "上周工作内容：一平台一策。辽宁省：与运营经理沟通制定组合套餐内容；与 AI 机器管试点平台商务沟通，面向投标人进行产品市场调研"],
    ["8", "AI 沈阳试点项目私有模型部署", "沙宏宇", "其他", "⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "辽宁省第 8 个交易平台，由辽宁国泰运营，服务沈阳市纪委。客户协调 3 台物理机、24 张 910B 显卡。已部署 Qwen3-32B 和 Qwen3-VL-32B 模型，已升级 Qwen3.5-27B，效果优于商用模型。后续需完成剩余实例升级和算力压测"],
    ["9", "2026 年度企业职业技能等级（高级）认定工作", "耿李欢", "系统通知", "⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "公司内组织职业技能等级认定，4 月 20-23 日集中录制培训（约 1.5 小时），5 月 18-22 日理论 + 实操考核，60 分合格，通过认证后补贴 500 元。附件：申报人员名单.xlsx"],
    ["10", "中新建数字招采平台技术方案交流会", "王东 (交易兵团分公司)", "招投标", "⭐⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "中新建余畅总需了解平台落地技术方案，对运营模式（场地复用、硬件设备部署、服务器减半等）存疑。暂定下周二 10:30 进行技术方案交流汇报"],
    ["11", "阳光优采运营及产品相关工作", "黄严宝", "系统通知", "⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "阳光优采平台运营及产品规划工作清单：1.管理规范的审核工作 2.平台材料管理（合同、入驻准则等材料更新及整理）3.其他竞品运营情况了解及分析 4.每周二产品发版评审会议 5.每周五拉通行业代表沟通紧急需求"],
    ["12", "【季报】新点 e 交易 Q1 季报 2026 年 1-3 月", "钟明珠", "工作汇报", "⭐⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "2026 年第一季度季报，包含平台运营数据报告"],
    ["13", "阳光优采平台常见问题收集", "马博林", "招投标", "⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "围绕阳光优采平台直播运营已开展 24 场，目前只有全流程操作培训和标证通专项培训 2 大类。为进一步丰富直播内容，收集采购人、供应商在实际使用平台过程中遇到的问题，计划下下周组织开展常见问题主题直播培训。征集截止时间：4 月 15 日"],
    ["14", "E 招冀成 - 数据中台数据推送备案", "宋品桥", "招投标", "⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "河北招标集团网络科技有限公司找了石家庄五十四所开发了数据中台，要求我司开发的 E 招冀成电子交易平台与其进行数据对接。4 月 13、14 号提供接口文档，基本覆盖数据规范中的所有表、字段。对接接口暂时不进行数据校验，有数据则推送，没有则置空"],
    ["15", "新疆阳光采购平台升级建设立项协调", "庞丹枫", "招投标", "⭐⭐⭐", "https://oa.epoint.com.cn/OA9/oa9/mail/mailframe", "现经与阳采中心确认本次平台建设事项，现已可以进行平台升级建设工作。与阳采沟通，我司已与阳采签订过共同运营协议，根据之前协议，阳采无法就本次升级再次签约。因公司内部流程要求，无合同无法立项，导致无法开展平台升级工作。希望总部领导协调"]
]

# 更新表格
print('\n📊 更新飞书表格...')
url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{SPREADSHEET_TOKEN}/values/Sheet1!A1:G16'
headers = {
    'Authorization': f'Bearer {app_token}',
    'Content-Type': 'application/json'
}

data = {
    'values': values
}

resp = requests.put(url, headers=headers, json=data, timeout=30)
print(f'状态码：{resp.status_code}')
print(f'响应：{resp.text[:500]}')

if resp.status_code == 200:
    print('\n✅ 表格更新成功!')
    print(f'🔗 查看：https://www.feishu.cn/sheets/{SPREADSHEET_TOKEN}')
else:
    print(f'\n❌ 更新失败')
