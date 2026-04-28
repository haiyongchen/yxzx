const fs = require('fs');
const { execSync } = require('child_process');

// 读取 Markdown 文件
const content = fs.readFileSync('D:/openclaw-workspace/oa_mail_for_upload_20260419_161246.md', 'utf8');

// 创建文档
const title = `OA 邮件分析报表-${new Date().toISOString().slice(0,10).replace(/-/g,'')}`;

console.log('🚀 创建腾讯文档...');
console.log(`标题：${title}`);

try {
    // 设置环境变量
    process.env.TENCENT_DOCS_TOKEN = 'e23255dcdf51491cb208ecc9cc341e21';
    
    // 调用 mcporter
    const args = JSON.stringify({ title, content });
    const result = execSync(`mcporter call tencent-docs create_smartcanvas_by_mdx --args '${args.replace(/'/g, "'\\''")}'`, {
        encoding: 'utf8',
        env: process.env
    });
    
    console.log('\n✅ 结果:', result);
    
    // 解析响应
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
    if (error.stdout) console.log('输出:', error.stdout.toString());
    if (error.stderr) console.log('错误:', error.stderr.toString());
}
