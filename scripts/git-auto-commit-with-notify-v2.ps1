# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    Git auto commit script with Feishu notification v2
.DESCRIPTION
    Execute git commit and send notification via Feishu
#>

param(
    [string]$WorkspacePath = "D:\openclaw-workspace",
    [string]$CommitMessage = "Auto commit daily backup",
    [string]$FeishuWebhook = "https://open.feishu.cn/open-apis/bot/v2/hook/dbd0d203-ba15-40ec-adfe-2311a8ba0f8c"
)

$startTime = Get-Date
$logFile = "$WorkspacePath\logs\git-auto-commit-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

# Ensure log directory exists
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

    # Build Feishu message card
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

    # Save to local notification file (for debugging)
    $notifyFile = "$WorkspacePath\.notifications\$(Get-Date -Format 'yyyyMMdd-HHmmss')-$Status.json"
    $message | Out-File -FilePath $notifyFile -Encoding UTF8

    # Try to send Feishu message (if webhook is configured)
    if ($FeishuWebhook -ne "https://open.feishu.cn/open-apis/bot/v2/hook/xxx") {
        try {
            $response = Invoke-RestMethod -Uri $FeishuWebhook -Method Post -ContentType "application/json" -Body $message
            Write-Log "Feishu notification sent: $response"
        } catch {
            Write-Log "Failed to send Feishu notification: $($_.Exception.Message)"
        }
    } else {
        Write-Log "Feishu Webhook not configured, notification saved to: $notifyFile"
    }
}

# Main execution
Write-Log "=========================================="
Write-Log "Git auto commit task started (v2)"
Write-Log "Workspace: $WorkspacePath"
Write-Log "Commit message: $CommitMessage"
Write-Log "=========================================="

try {
    # Change to workspace directory
    Set-Location $WorkspacePath

    # Check for changes
    $status = git status --porcelain

    if ([string]::IsNullOrWhiteSpace($status)) {
        $msg = "No changes to commit"
        Write-Log $msg

        Send-FeishuNotification `
            -Title "Git Auto Commit - No Changes" `
            -Content "**Time**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`nWorkspace: $WorkspacePath`n`nNo changes detected." `
            -Status "info"

        exit 0
    }

    # Show changed files
    Write-Log "Detected changes:"
    $fileList = $status | ForEach-Object {
        Write-Log "  $_"
        "- $_"
    }

    # Add all changes
    Write-Log "Adding files..."
    git add . 2>&1 | ForEach-Object { Write-Log "  $_" }

    # Commit
    Write-Log "Committing..."
    $commitOutput = git commit -m "$CommitMessage" 2>&1
    $commitOutput | ForEach-Object { Write-Log "  $_" }

    # Get commit hash
    $commitHash = git rev-parse --short HEAD

    # Push
    Write-Log "Pushing to remote..."
    $pushOutput = git push 2>&1
    $pushOutput | ForEach-Object { Write-Log "  $_" }

    $endTime = Get-Date
    $duration = $endTime - $startTime

    $successContent = @"
**Git Auto Commit Success**

**Commit Info**
- Commit hash: $commitHash
- Commit message: $CommitMessage
- Changed files: $($fileList.Count)

**Execution Time**
- Start: $($startTime.ToString("yyyy-MM-dd HH:mm:ss"))
- End: $($endTime.ToString("yyyy-MM-dd HH:mm:ss"))
- Duration: $($duration.TotalSeconds) seconds

**Changed Files**
$($fileList | Join-String -Separator "`n")
"@

    Write-Log "Commit successful: $commitHash"

    Send-FeishuNotification `
        -Title "Git Auto Commit - Success" `
        -Content $successContent `
        -Status "success"

    Write-Log "Task completed"
    exit 0
}
catch {
    $errorContent = @"
**Git Auto Commit Failed**

**Workspace**: $WorkspacePath

**Error Message**:
```
$($_.Exception.Message)
```

**Failed Time**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

    Write-Log "Error: $($_.Exception.Message)"

    Send-FeishuNotification `
        -Title "Git Auto Commit - Failed" `
        -Content $errorContent `
        -Status "error"

    exit 1
}
