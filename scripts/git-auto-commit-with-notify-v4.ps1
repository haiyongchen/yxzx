# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    Git auto commit script with email and Feishu notification v4
.DESCRIPTION
    Execute git commit, push to remote, and send email + Feishu notification
#>

param(
    [string]$WorkspacePath = "D:\openclaw-workspace",
    [string]$CommitMessage = "Auto commit daily backup",
    [string]$EmailScriptPath = "D:\openclaw-workspace\skills\qq-email-sender\scripts\send_email.py",
    [string]$FeishuUserId = "ou_a2ec1244bbefe1fc19ace7d85718ea08"
)

$startTime = Get-Date
$logFile = "$WorkspacePath\logs\git-auto-commit-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

# Ensure log directory exists
New-Item -ItemType Directory -Force -Path "$WorkspacePath\logs" | Out-Null

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Tee-Object -FilePath $logFile -Append
}

function Send-EmailNotification {
    param(
        [string]$Subject,
        [string]$Body
    )
    
    try {
        if (Test-Path $EmailScriptPath) {
            $escapedSubject = $Subject -replace '"', '\"'
            $escapedBody = $Body -replace '"', '\"'
            Invoke-Expression "python `"$EmailScriptPath`" `"$escapedSubject`" `"$escapedBody`"" 2>&1 | ForEach-Object { Write-Log "  Email: $_" }
        } else {
            Write-Log "Email script not found: $EmailScriptPath"
        }
    } catch {
        Write-Log "Failed to send email: $($_.Exception.Message)"
    }
}

function Send-FeishuNotification {
    param(
        [string]$Message
    )
    
    try {
        Write-Log "Sending Feishu notification..."
        
        # Use openclaw to send message via current session
        $feishuCmd = "openclaw message send --channel feishu --target `"$FeishuUserId`" --message `"$Message`""
        Invoke-Expression $feishuCmd 2>&1 | ForEach-Object { Write-Log "  Feishu: $_" }
        
        Write-Log "Feishu notification sent successfully"
    } catch {
        Write-Log "Failed to send Feishu notification: $($_.Exception.Message)"
    }
}

# Main execution
Write-Log "=========================================="
Write-Log "Git auto commit task started (v4)"
Write-Log "Workspace: $WorkspacePath"
Write-Log "Commit message: $CommitMessage"
Write-Log "=========================================="

try {
    # Change to workspace directory
    $originalLocation = Get-Location
    Set-Location $WorkspacePath
    Write-Log "Changed to directory: $(Get-Location)"

    # Check for changes
    $status = git status --porcelain

    if ([string]::IsNullOrWhiteSpace($status)) {
        $msg = "No changes to commit"
        Write-Log $msg
        
        $feishuMsg = "📋 Git Auto Commit - No Changes`n`nTime: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`nWorkspace: $WorkspacePath`n`nNo changes detected."
        Send-FeishuNotification -Message $feishuMsg
        
        Send-EmailNotification `
            -Subject "Git Auto Commit - No Changes" `
            -Body "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`nWorkspace: $WorkspacePath`n`nNo changes detected."
        
        exit 0
    }

    # Show changed files
    Write-Log "Detected changes:"
    $fileList = @()
    $status | ForEach-Object {
        Write-Log "  $_"
        $fileList += "- $_"
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
    Write-Log "Commit hash: $commitHash"

    # Push to remote (use SSH to avoid HTTPS proxy issues)
    Write-Log "Pushing to remote..."
    
    # Update yxzx submodule remote to SSH
    if (Test-Path "$WorkspacePath\yxzx\.git") {
        $yxzxConfig = "$WorkspacePath\yxzx\.git\config"
        if (Test-Path $yxzxConfig) {
            (Get-Content $yxzxConfig) -replace 'https://github.com/', 'git@github.com:' | Set-Content $yxzxConfig
        }
    }
    
    # Temporarily disable URL rewrite and use SSH
    git config --global --unset url.https://github.com/.insteadof 2>$null
    git remote set-url origin git@github.com:haiyongchen/yxzx.git
    
    $pushOutput = git push origin master 2>&1
    $pushOutput | ForEach-Object { Write-Log "  $_" }
    
    # Restore global config
    git config --global --add url.https://github.com/.insteadof git@github.com: 2>$null
    
    # Check push result
    if ($LASTEXITCODE -ne 0) {
        throw "Git push failed with exit code $LASTEXITCODE"
    }
    
    $pushStatus = "Successfully pushed to git@github.com:haiyongchen/yxzx.git"
    Write-Log $pushStatus

    $endTime = Get-Date
    $duration = $endTime - $startTime

    $fileListStr = $fileList -join "`n"

    # Send Feishu notification
    $feishuSuccessMsg = @"
✅ Git Auto Commit Success

📌 Commit Info:
• Commit hash: $commitHash
• Commit message: $CommitMessage
• Changed files: $($fileList.Count)
• Push status: Success

⏱️ Execution Time:
• Start: $($startTime.ToString("yyyy-MM-dd HH:mm:ss"))
• End: $($endTime.ToString("yyyy-MM-dd HH:mm:ss"))
• Duration: $([math]::Round($duration.TotalSeconds, 2)) seconds

📁 Changed Files:
$fileListStr
"@
    Send-FeishuNotification -Message $feishuSuccessMsg

    $successBody = @"
Git Auto Commit and Push Success

Commit Info:
- Commit hash: $commitHash
- Commit message: $CommitMessage
- Changed files: $($fileList.Count)
- Push status: $pushStatus

Execution Time:
- Start: $($startTime.ToString("yyyy-MM-dd HH:mm:ss"))
- End: $($endTime.ToString("yyyy-MM-dd HH:mm:ss"))
- Duration: $($duration.TotalSeconds) seconds

Changed Files:
$fileListStr

---
This email was sent automatically by Git Auto Commit Task
"@

    Write-Log "Commit and push successful: $commitHash"
    
    # Send email notification
    Send-EmailNotification `
        -Subject "Git Auto Commit Success - $commitHash" `
        -Body $successBody

    Write-Log "Task completed successfully"
    exit 0
}
catch {
    $endTime = Get-Date
    $duration = $endTime - $startTime
    
    # Send Feishu error notification
    $feishuErrorMsg = @"
❌ Git Auto Commit Failed

⚠️ Error Message:
$($_.Exception.Message)

⏱️ Failed Time: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
⏱️ Duration: $([math]::Round($duration.TotalSeconds, 2)) seconds

Workspace: $WorkspacePath
"@
    Send-FeishuNotification -Message $feishuErrorMsg
    
    $errorBody = @"
Git Auto Commit Failed

Workspace: $WorkspacePath

Error Message:
$($_.Exception.Message)

Failed Time: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

---
This email was sent automatically by Git Auto Commit Task
"@

    Write-Log "Error: $($_.Exception.Message)"
    
    # Send error email notification
    Send-EmailNotification `
        -Subject "Git Auto Commit Failed" `
        -Body $errorBody

    exit 1
}
