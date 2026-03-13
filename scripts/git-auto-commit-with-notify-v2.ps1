# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    Git 自动提交脚本（带飞书通知功能 v2）
.DESCRIPTION
    执行 git 提交并通过飞书发送通知
#>

param(
    [string]$WorkspacePath = "D:\openclaw-workspace",
    [string]$CommitMessage = "Auto commit daily backup",
    [string]$FeishuWebhook = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"  # 需要配置实际的 webhook
)

$startTime = Get-Date
$logFile = "$WorkspacePath\logs\git-auto-commit-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

# 确保日志目录存在
New-Item -ItemType Directory -Force -Path "$WorkspacePath\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "$WorkspacePath\.notifications" | Out-Null

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
        # 构建飞书消息卡片
        $color = switch ($Status) {
            "success" { "green" }
            "error" { "red" }
            default { "blue" }
        }
        
        $message = @{
            msg_type = "interactive"
            card = @{
                config = @{
                    wide_screen_mode = $true
                    enable_forward = $true
                }
                header = @{
                    title = @{
                        tag = "plain_text"
                        content = $Title
                    }
                    template = $color
                }
                elements = @(
                    @{
                        tag = "div"
                        text = @{
                            tag = "lark_md"
                            content = $Content
                        }
                    }
                )
            }
        } | ConvertTo-Json -Depth 10
        
        # 保存到本地通知文件（用于调试）
        $notifyFile = "$WorkspacePath\.notifications\$(Get-Date -Format 'yyyyMMdd-HHmmss')-$Status.json"
        $message | Out-File -FilePath $notifyFile -Encoding UTF8
        
        # 尝试发送飞书消息（如果有配置 webhook）
        if ($FeishuWebhook -ne "https://open.feishu.cn/open-apis/bot/v2/hook/xxx") {
            $response = Invoke-RestMethod -Uri $FeishuWebhook -Method Post -ContentType "application/json" -Body $message
            Write-Log "飞书通知已发送: $response"
        } else {
            Write-Log "飞书 Webhook 未配置，通知已保存到: $notifyFile"
            
            # 尝试通过 OpenClaw 发送消息
            try {
                $env:OPENCLAW_NOTIFY = $message
                Write-Log "已设置 OPENCLAW_NOTIFY 环境变量"
            } catch {
                Write-Log "OpenClaw 通知设置失败: $($_.Exception.Message)"
            }
        }
    }
    catch {
        Write-Log "发送通知失败: $($_.Exception.Message)"
    }
}

Write-Log "=========================================="
Write-Log "Git 自动提交任务开始 (v2)"
Write-Log "工作目录: $WorkspacePath"
Write-Log "提交信息: $CommitMessage"
Write-Log "=========================================="

try {
    # 切换到工作目录
    Set-Location $WorkspacePath
    
    # 检查是否有变更
    $status = git status --porcelain
    
    if ([string]::IsNullOrWhiteSpace($status)) {
        $msg = "✅ 没有需要提交的变更"
        Write-Log $msg
        
        Send-FeishuNotification `
            -Title "Git 自动提交 - 无变更" `
            -Content "**时间**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`n工作目录: $WorkspacePath`n`n没有检测到需要提交的变更。" `
            -Status "info"
        
        exit 0
    }
    
    # 显示变更文件
    Write-Log "检测到以下变更:"
    $fileList = $status | ForEach-Object { 
        Write-Log "  $_"
        "- $_"
    }
    
    # 添加所有变更
    Write-Log "正在添加文件..."
    git add . 2>&1 | ForEach-Object { Write-Log "  $_" }
    
    # 提交
    Write-Log "正在提交..."
    $commitOutput = git commit -m "$CommitMessage" 2>&1
    $commitOutput | ForEach-Object { Write-Log "  $_" }
    
    # 获取提交哈希
    $commitHash = git rev-parse --short HEAD
    
    # 推送
    Write-Log "正在推送到远程..."
    $pushOutput = git push 2>&1
    $pushOutput | ForEach-Object { Write-Log "  $_" }
    
    $endTime = Get-Date
    $duration = $endTime - $startTime
    
    $successContent = @"
**✅ Git 自动提交成功**

**📊 提交信息**
- 提交哈希: $commitHash
- 提交信息: $CommitMessage
- 变更文件数: $($fileList.Count)

**⏱️ 执行时间**
- 开始: $($startTime.ToString("yyyy-MM-dd HH:mm:ss"))
- 结束: $($endTime.ToString("yyyy-MM-dd HH:mm:ss"))
- 耗时: $($duration.TotalSeconds) 秒

**📁 变更文件**
$($fileList | Join-String -Separator "`n")
"@
    
    Write-Log "提交成功: $commitHash"
    
    Send-FeishuNotification `
        -Title "Git 自动提交 - 成功" `
        -Content $successContent `
        -Status "success"
    
    Write-Log "任务完成"
    exit 0
}
catch {
    $errorContent = @"
**❌ Git 自动提交失败**

**📁 工作目录**: $WorkspacePath

**❌ 错误信息**:
```
$($_.Exception.Message)
```

**🕐 失败时间**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@
    
    Write-Log "错误: $($_.Exception.Message)"
    
    Send-FeishuNotification `
        -Title "Git 自动提交 - 失败" `
        -Content $errorContent `
        -Status "error"
    
    exit 1
}
