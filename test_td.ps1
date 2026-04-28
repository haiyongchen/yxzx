$env:TENCENT_DOCS_TOKEN = "e23255dcdf51491cb208ecc9cc341e21"

Write-Host "🚀 测试创建腾讯文档..."

$result = mcporter call "tencent-docs.create_smartcanvas_by_mdx(title: `"测试文档`", mdx: `"# 测试`n`n这是测试内容`")"

Write-Host "结果：$result"

try {
    $response = $result | ConvertFrom-Json
    if ($response.error -eq "" -or -not $response.error) {
        Write-Host "`n✅ 创建成功!" -ForegroundColor Green
        Write-Host "📄 文档 ID: $($response.file_id)"
        Write-Host "🔗 在线查看：$($response.url)" -ForegroundColor Cyan
    } else {
        Write-Host "`n❌ 错误：$($response.error)" -ForegroundColor Red
    }
} catch {
    Write-Host "`n❌ 解析失败：$_" -ForegroundColor Red
    Write-Host "原始输出：$result"
}
