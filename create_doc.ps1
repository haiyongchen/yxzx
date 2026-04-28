# 创建腾讯文档
$env:TENCENT_DOCS_TOKEN = "e23255dcdf51491cb208ecc9cc341e21"

# 读取本地 Markdown 文件
$content = Get-Content "D:\openclaw-workspace\oa_mail_for_upload_20260419_161246.md" -Raw -Encoding UTF8

# 创建 JSON 参数
$jsonParams = @{
    title = "OA 邮件分析报表-$(Get-Date -Format 'yyyyMMdd')"
    content = $content
} | ConvertTo-Json -Compress

Write-Host "🚀 创建腾讯文档..."
Write-Host "参数：$jsonParams"

# 调用 mcporter
$result = mcporter call tencent-docs create_smartcanvas_by_mdx --args $jsonParams

Write-Host "`n结果：$result"
