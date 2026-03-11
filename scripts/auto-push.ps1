# 运营中心 Git 自动推送脚本
# 执行时间：每天晚上 23:00
# 路径：D:\work\运营中心\yxzx

$repoPath = "D:\work\运营中心\yxzx"
$logFile = "D:\work\运营中心\yxzx\scripts\push-log.txt"

# 记录开始时间
$startTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logMessage = "[$startTime] 开始执行 Git 自动推送`n"

try {
    # 切换到仓库目录
    Set-Location $repoPath
    
    # 配置 Git 用户信息（如果未配置）
    git config user.name "OpenClaw Bot" 2>$null
    git config user.email "bot@openclaw.local" 2>$null
    
    # 添加所有更改
    $addResult = git add -A 2>&1
    $logMessage += "[$startTime] Git add 完成`n"
    
    # 检查是否有更改
    $status = git status --porcelain
    if ($status) {
        # 有更改，执行提交
        $commitTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $commitResult = git commit -m "Auto-commit: 每日备份 $commitTime" 2>&1
        $logMessage += "[$startTime] Git commit 完成：$commitResult`n"
        
        # 推送到远程
        $pushResult = git push origin main 2>&1
        $logMessage += "[$startTime] Git push 完成：$pushResult`n"
    } else {
        $logMessage += "[$startTime] 无更改，跳过推送`n"
    }
    
    $logMessage += "[$startTime] ✅ 执行成功`n"
}
catch {
    $logMessage += "[$startTime] ❌ 执行失败：$($_.Exception.Message)`n"
}

# 写入日志
$logMessage += "`n"
Add-Content -Path $logFile -Value $logMessage -Encoding UTF8

# 只保留最近 30 天的日志
if (Test-Path $logFile) {
    $content = Get-Content $logFile -Raw
    $lines = $content -split "`n"
    if ($lines.Count -gt 500) {
        $lines[-500..-1] | Set-Content $logFile -Encoding UTF8
    }
}
