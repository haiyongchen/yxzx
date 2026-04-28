const { execSync } = require('child_process');
const fs = require('fs');

// 设置 Token
process.env.TENCENT_DOCS_TOKEN = 'e23255dcdf51491cb208ecc9cc341e21';

// 读取 Markdown 文件
const mdFile = 'D:/openclaw-workspace/oa_mail_for_upload_20260419_161246.md';
const content = fs.readFileSync(mdFile, 'utf8');

const title = `OA 邮件分析报表-${new Date().toISOString().slice(0,10).replace(/-/g,'')}`;

console.log('🚀 创建腾讯文档...');
console.log(`标题：${title}`);
console.log(`内容长度：${content.length} 字符`);

// 写入临时 JSON 文件
const paramsFile = 'D:/openclaw-workspace/tencent_params.json';
const params = { title, mdx: content };
fs.writeFileSync(paramsFile, JSON.stringify(params, null, 2), 'utf8');

console.log(`\n📄 参数文件：${paramsFile}`);

// 使用文件方式调用
try {
    const result = execSync(`mcporter call tencent-docs create_smartcanvas_by_mdx --file ${paramsFile}`, {
        encoding: 'utf8',
        env: process.env,
        cwd: 'D:/openclaw-workspace'
    });
    
    console.log('\n✅ 结果:', result);
    
    const response = JSON.parse(result);
    if (response.error === '' || !response.error) {
        const fileId = response.file_id || response.node_id;
        const url = response.url || `https://docs.qq.com/doc/${fileId}`;
        console.log('\n🎉 创建成功!');
        console.log(`📄 文档 ID: ${fileId}`);
        console.log(`🔗 在线查看：${url}`);
    } else {
        console.log('\n❌ 错误:', response.error);
    }
} catch (error) {
    console.error('\n❌ 失败:', error.message);
    if (error.stdout) console.log('输出:', error.stdout.toString().slice(0, 1000));
    if (error.stderr) console.log('错误:', error.stderr.toString().slice(0, 1000));
}
