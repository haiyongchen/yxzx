# 创建腾讯文档
$env:TENCENT_DOCS_TOKEN = "e23255dcdf51491cb208ecc9cc341e21"

# 读取内容
$content = Get-Content "D:\openclaw-workspace\oa_mail_for_upload_20260419_161246.md" -Raw -Encoding UTF8
$title = "OA 邮件分析报表-$(Get-Date -Format 'yyyyMMdd')"

# 创建临时文件存储 JSON
$jsonFile = "$env:TEMP\tencent_params.json"
@{
    title = $title
    mdx = $content
} | ConvertTo-Json -Depth 10 -Compress | Out-File -FilePath $jsonFile -Encoding UTF8

Write-Host "📄 标题：$title"
Write-Host "📝 内容长度：$($content.Length) 字符"
Write-Host "💾 JSON 文件：$jsonFile"
Write-Host ""
Write-Host "🚀 创建腾讯文档..."

# 读取 JSON 文件内容作为参数
$jsonContent = Get-Content $jsonFile -Raw -Encoding UTF8

# 调用 mcporter
$result = mcporter call tencent-docs create_smartcanvas_by_mdx $jsonContent

Write-Host ""
Write-Host "结果：$result"
