# 测试 Git 推送脚本
# 用于手动测试推送功能

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  运营中心 Git 推送测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repoPath = "D:\work\运营中心\yxzx"
Set-Location $repoPath

Write-Host "📁 仓库路径：$repoPath" -ForegroundColor Yellow
Write-Host ""

# 检查 Git 状态
Write-Host "📊 检查 Git 状态..." -ForegroundColor Green
$status = git status --porcelain
if ($status) {
    Write-Host "发现以下更改:" -ForegroundColor Yellow
    $status | ForEach-Object { Write-Host "  $_" }
} else {
    Write-Host "✅ 无更改" -ForegroundColor Green
}
Write-Host ""

# 添加所有更改
Write-Host "📝 添加所有更改..." -ForegroundColor Green
git add -A
Write-Host "✅ 添加完成" -ForegroundColor Green
Write-Host ""

# 检查是否有更改需要提交
$status = git status --porcelain
if ($status) {
    Write-Host "💾 提交更改..." -ForegroundColor Green
    $commitTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "Test commit: 测试推送 $commitTime"
    Write-Host "✅ 提交完成" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "🚀 推送到远程..." -ForegroundColor Green
    git push origin main
    Write-Host "✅ 推送完成" -ForegroundColor Green
} else {
    Write-Host "⏭️  无更改，跳过推送" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  测试完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
