# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    Git 自动提交脚本（带通知功能）
.DESCRIPTION
    执行 git 提交并发送飞书通知
#>

param(
    [string]$WorkspacePath = "D:\openclaw-workspace",
    [string]$CommitMessage = "Auto commit daily backup"
)

$startTime = Get-Date
$logFile = "$WorkspacePath\logs\git-auto-commit-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

# 确保日志目录存在
New-Item -ItemType Directory -Force -Path "$WorkspacePath\logs" | Out-Null

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Tee-Object -FilePath $logFile -Append
}

function Send-FeishuNotification {
    param(
        [string]$Title,
        [string]$Content,
        [string]$Status = "info"
    )
    
    try {
        # 使用 OpenClaw 的飞书通道发送消息
        $message = @{
            title = $Title
            content = $Content
            status = $Status
            timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        } | ConvertTo-Json
        
        # 写入通知队列文件
        $notifyFile = "$WorkspacePath\.notifications\$(Get-Date -Format 'yyyyMMdd-HHmmss')-$Status.json"
        New-Item -ItemType Directory -Force -Path "$WorkspacePath\.notifications" | Out-Null
        $message | Out-File -FilePath $notifyFile -Encoding UTF8
        
        Write-Log "通知已保存: $notifyFile"
    }
    catch {
        Write-Log "发送通知失败: $($_.Exception.Message)"
    }
}

Write-Log "=========================================="
Write-Log "Git 自动提交任务开始"
Write-Log "工作目录: $WorkspacePath"
Write-Log "提交信息: $CommitMessage"
Write-Log "=========================================="

try {
    # 切换到工作目录
    Set-Location $WorkspacePath
    
    # 检查是否有变更
    $status = git status --porcelain
    
    if ([string]::IsNullOrWhiteSpace($status)) {
        $msg = "没有需要提交的变更"
        Write-Log $msg
        
        Send-FeishuNotification `
            -Title "Git 自动提交 - 无变更" `
            -Content $msg `
            -Status "info"
        
        exit 0
    }
    
    # 显示变更文件
    Write-Log "检测到以下变更:"
    $status | ForEach-Object { Write-Log "  $_" }
    
    # 添加所有变更
    Write-Log "正在添加文件..."
    git add . 2>&1 | ForEach-Object { Write-Log "  $_" }
    
    # 提交
    Write-Log "正在提交..."
    $commitOutput = git commit -m "$CommitMessage" 2>&1
    $commitOutput | ForEach-Object { Write-Log "  $_" }
    
    # 推送
    Write-Log "正在推送到远程..."
    $pushOutput = git push 2>&1
    $pushOutput | ForEach-Object { Write-Log "  $_" }
    
    $endTime = Get-Date
    $duration = $endTime - $startTime
    
    $successMsg = @"
✅ Git 自动提交成功

📁 工作目录: $WorkspacePath
📝 提交信息: $CommitMessage
⏱️ 执行时间: $($duration.TotalSeconds) 秒
📊 变更文件数: $($status.Count)

🕐 开始时间: $($startTime.ToString("yyyy-MM-dd HH:mm:ss"))
🕐 结束时间: $($endTime.ToString("yyyy-MM-dd HH:mm:ss"))
"@
    
    Write-Log $successMsg
    
    Send-FeishuNotification `
        -Title "Git 自动提交 - 成功" `
        -Content $successMsg `
        -Status "success"
    
    Write-Log "任务完成"
    exit 0
}
catch {
    $errorMsg = @"
❌ Git 自动提交失败

📁 工作目录: $WorkspacePath
❌ 错误信息: $($_.Exception.Message)
📋 详细错误: $($_.ScriptStackTrace)

🕐 失败时间: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@
    
    Write-Log $errorMsg
    
    Send-FeishuNotification `
        -Title "Git 自动提交 - 失败" `
        -Content $errorMsg `
        -Status "error"
    
    exit 1
}
