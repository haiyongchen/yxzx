const https = require('https');

const APP_ID = 'cli_a92024d097381cc5';
const APP_SECRET = 'bccDjxYuqOpx08k7MwcYxfYRMUQJMYWM';
const OWNER_OPEN_ID = 'ou_a2ec1244bbefe1fc19ace7d85718ea08';

// 邮件数据
const EMAIL_DATA = [
  ["1", "【阳光优采】关于近期平台上量过程中的问题及工作建议总结梳理", "李涛 (运营中心)", "星期六 08:33", "电子商城", "6 大问题 +5 项建议", "⭐⭐⭐"],
  ["2", "【规范评审】服务器预规划流程、正式部署流程增加 pinpoint 监控体系内容评审", "包亚峰", "星期五 16:26", "系统通知", "Pinpoint 监控评审", "⭐⭐"],
  ["3", "【商城专区开设】武汉光谷联合产权交易所黄石分公司", "罗永健", "星期五 08:35", "招投标", "五五分成协议", "⭐⭐⭐"],
  ["4", "AI 评标系统废标情况查询", "沙宏宇", "星期二 17:44", "招投标", "技术标废标异常排查", "⭐⭐"],
  ["5", "关于新疆阳光采购平台升级后市场推广上量相关事宜的沟通", "庞丹枫", "星期二 13:03", "招投标", "3 家国企入企推广", "⭐⭐⭐"],
  ["6", "山东兴多专区提取部署事宜", "庞鑫", "星期二 11:16", "电子商城", "年保底 130 个项目", "⭐⭐"],
  ["7", "营销周报（4.7-4.10）-徐志远", "徐志远", "星期二 09:36", "工作汇报", "每周营销汇报", "⭐"],
  ["8", "AI 沈阳试点项目私有模型调试和切换工作协调备案", "沙宏宇", "星期一 18:54", "电子商城", "私有模型部署进展", "⭐⭐"],
  ["9", "2026 年度企业职业技能等级（高级）认定工作开展", "耿李欢", "星期一 14:52", "培训学习", "职业技能认定", "⭐"],
  ["10", "关于中新建数字发展有限责任公司建设兵团国有企业招采平台技术方案交流会事宜", "王东 (交易兵团分公司)", "星期一 14:51", "招投标", "技术方案交流", "⭐⭐⭐"],
  ["11", "关于阳光优采运营及产品相关工作", "黄严宝", "星期一 13:39", "电子商城", "运营产品工作", "⭐⭐"],
  ["12", "【季报】\"新点 e 交易\"平台第一季度季报 2026 年 1-3 月", "钟明珠", "2026-04-12", "工作汇报", "Q1 季报", "⭐⭐⭐"],
  ["13", "关于阳光优采平台常见问题收集的专项邮件", "马博林", "2026-04-10", "电子商城", "问题收集", "⭐⭐"],
  ["14", "E 招冀成 - 对接客户数据中台数据推送工作说明备案", "宋品桥", "2026-04-10", "系统通知", "数据推送备案", "⭐⭐"],
  ["15", "关于新疆阳光采购平台升级建设工作立项事宜内部协调", "庞丹枫", "2026-04-10", "招投标", "项目立项协调", "⭐⭐⭐"]
];

function httpRequest(options, data = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          resolve(result);
        } catch (e) {
          reject(new Error(`JSON 解析失败：${body}`));
        }
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

async function getTenantAccessToken() {
  const data = JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET });
  const options = {
    hostname: 'open.feishu.cn',
    port: 443,
    path: '/open-apis/auth/v3/tenant_access_token/internal',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  };
  const result = await httpRequest(options, data);
  if (result.code !== 0) throw new Error(`获取 token 失败：${result.msg}`);
  return result.tenant_access_token;
}

async function createDoc(token, title, ownerOpenId) {
  const data = JSON.stringify({ title, owner_id: ownerOpenId, id_type: 'open_id' });
  const options = {
    hostname: 'open.feishu.cn',
    port: 443,
    path: '/open-apis/docx/v1/documents',
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
  };
  const result = await httpRequest(options, data);
  if (result.code !== 0) throw new Error(`创建文档失败：${result.msg}`);
  return result.data;
}

async function createTableWithValues(token, docId, values) {
  const data = JSON.stringify({
    parent_block_id: docId,
    row_size: values.length,
    column_size: values[0].length,
    column_width: [50, 300, 100, 100, 80, 200, 60],
    cells: values.map((row, rowIndex) => 
      row.map((cell, colIndex) => ({
        row_index: rowIndex,
        column_index: colIndex,
        text: { content: cell }
      }))
    ).flat()
  });
  const options = {
    hostname: 'open.feishu.cn',
    port: 443,
    path: '/open-apis/docx/v1/documents/' + docId + '/blocks/table',
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
  };
  const result = await httpRequest(options, data);
  if (result.code !== 0) throw new Error(`创建表格失败：${result.msg}`);
  return result.data;
}

async function main() {
  try {
    console.log('1. 获取访问令牌...');
    const token = await getTenantAccessToken();
    console.log('   ✓ 令牌获取成功');

    console.log('2. 创建文档...');
    const doc = await createDoc(token, 'OA 邮件分析报表 - 2026-04-19', OWNER_OPEN_ID);
    console.log('   ✓ 文档创建成功');
    console.log('   文档 ID:', doc.document_id);

    console.log('3. 创建表格并填入数据...');
    // 添加表头
    const headerRow = ['序号', '邮件主题', '发件人', '日期', '分类', '内容摘要', '优先级'];
    const allRows = [headerRow, ...EMAIL_DATA];
    
    const table = await createTableWithValues(token, doc.document_id, allRows);
    console.log('   ✓ 表格创建成功');
    console.log('   表格块 ID:', table.block_id);

    const docUrl = `https://xxx.feishu.cn/docx/${doc.document_id}`;
    console.log('\n✅ 完成！文档链接：' + docUrl);
    console.log('\n文档信息：');
    console.log('  标题：OA 邮件分析报表 - 2026-04-19');
    console.log('  行数：' + allRows.length + ' (1 行表头 + 15 行数据)');
    console.log('  列数：7');
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

main();
