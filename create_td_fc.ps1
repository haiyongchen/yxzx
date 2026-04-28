$env:TENCENT_DOCS_TOKEN = "e23255dcdf51491cb208ecc9cc341e21"

$content = Get-Content "D:\openclaw-workspace\oa_mail_for_upload_20260419_161246.md" -Raw -Encoding UTF8
$title = "OA 邮件分析报表-$(Get-Date -Format 'yyyyMMdd')"

Write-Host "🚀 创建腾讯文档..."
Write-Host "📄 标题：$title"
Write-Host ""

# 使用 function-call 语法
$result = mcporter call "tencent-docs.create_smartcanvas_by_mdx(title: `"$title`", mdx: `"$content`")"

Write-Host ""
Write-Host "结果：$result"

# 尝试解析
try {
    $response = $result | ConvertFrom-Json
    if ($response.error -eq "" -or -not $response.error) {
        Write-Host ""
        Write-Host "✅ 创建成功!" -ForegroundColor Green
        Write-Host "📄 文档 ID: $($response.file_id)"
        Write-Host "🔗 在线查看：$($response.url)"
    } else {
        Write-Host ""
        Write-Host "❌ 错误：$($response.error)" -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "❌ 解析失败：$_" -ForegroundColor Red
}
