param(
    [string]$Title,
    [string]$Mdx
)

$env:TENCENT_DOCS_TOKEN = "e23255dcdf51491cb208ecc9cc341e21"

# 创建参数对象
$params = @{
    title = $Title
    mdx = $Mdx
}

# 转换为 JSON
$json = $params | ConvertTo-Json -Depth 10 -Compress

# 写入临时文件
$tempFile = "$env:TEMP\td_params_$((Get-Date).ToString('yyyyMMdd_HHmmss')).json"
$json | Out-File -FilePath $tempFile -Encoding UTF8 -NoNewline

Write-Host "📄 标题：$Title"
Write-Host "📝 内容长度：$($Mdx.Length) 字符"
Write-Host "💾 参数文件：$tempFile"
Write-Host ""
Write-Host "🚀 创建腾讯文档..."

# 调用 mcporter
$result = mcporter call tencent-docs create_smartcanvas_by_mdx --file $tempFile

Write-Host ""
Write-Host "结果：$result"

# 清理
Remove-Item $tempFile -Force
