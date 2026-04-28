$env:TENCENT_DOCS_TOKEN = "e23255dcdf51491cb208ecc9cc341e21"

$content = Get-Content "D:\openclaw-workspace\oa_mail_for_upload_20260419_161246.md" -Raw -Encoding UTF8
$title = "OA 邮件分析报表-$(Get-Date -Format 'yyyyMMdd')"

Write-Host "🚀 创建腾讯文档..."
Write-Host "📄 标题：$title"
Write-Host "📝 内容长度：$($content.Length) 字符"
Write-Host ""

# 使用 key=value 格式调用
# 注意：需要将内容转义
$escapedContent = $content -replace '"', '``"' -replace '\n', '`n'

$result = mcporter call tencent-docs create_smartcanvas_by_mdx "title=$title" "mdx=$content"

Write-Host ""
Write-Host "结果：$result"
