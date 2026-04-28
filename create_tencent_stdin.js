const { spawn } = require('child_process');
const fs = require('fs');

// 设置 Token
process.env.TENCENT_DOCS_TOKEN = 'e23255dcdf51491cb208ecc9cc341e21';

// 读取 Markdown 文件
const mdFile = 'D:/openclaw-workspace/oa_mail_for_upload_20260419_161246.md';
const content = fs.readFileSync(mdFile, 'utf8');

const title = `OA 邮件分析报表-${new Date().toISOString().slice(0,10).replace(/-/g,'')}`;

console.log('🚀 创建腾讯文档...\n');
console.log(`📄 标题：${title}`);
console.log(`📝 内容长度：${content.length} 字符\n`);

// 使用 stdin 传递参数（避免命令行转义问题）
const mcporter = spawn('powershell', ['-ExecutionPolicy', 'Bypass', '-File', 'D:/nvm4w/nodejs/mcporter.ps1', 'call', 'tencent-docs', 'create_smartcanvas_by_mdx'], {
    env: process.env,
    stdio: ['pipe', 'pipe', 'pipe']
});

// 通过 stdin 传递 JSON 参数
const params = JSON.stringify({ title, mdx: content });
mcporter.stdin.write(params);
mcporter.stdin.end();

let output = '';
let error = '';

mcporter.stdout.on('data', (data) => {
    output += data.toString();
});

mcporter.stderr.on('data', (data) => {
    error += data.toString();
});

mcporter.on('close', (code) => {
    console.log(`返回码：${code}\n`);
    
    if (output) {
        console.log('输出:', output.slice(0, 1000));
    }
    if (error) {
        console.log('错误:', error.slice(0, 1000));
    }
    
    if (code === 0) {
        try {
            const response = JSON.parse(output.trim());
            if (response.error === '' || !response.error) {
                const fileId = response.file_id || response.node_id;
                const url = response.url || `https://docs.qq.com/doc/${fileId}`;
                console.log('\n✅ 创建成功!');
                console.log(`📄 文档 ID: ${fileId}`);
                console.log(`🔗 在线查看：${url}`);
            } else {
                console.log('\n❌ 错误:', response.error);
            }
        } catch (e) {
            console.log('\n❌ 解析失败:', e.message);
        }
    } else {
        console.log('\n❌ 创建失败');
    }
});
