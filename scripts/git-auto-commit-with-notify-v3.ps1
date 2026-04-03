# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    Git auto commit script with email notification v3
.DESCRIPTION
    Execute git commit, push to remote, and send email notification
#>

param(
    [string]$WorkspacePath = "D:\work\运营中心\yxzx",
    [string]$CommitMessage = "Auto commit daily backup",
    [string]$EmailScriptPath = "D:\openclaw-workspace\skills\qq-email-sender\scripts\send_email.py"
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

# Main execution
Write-Log "=========================================="
Write-Log "Git auto commit task started (v3)"
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

    # Push to remote
    Write-Log "Pushing to remote..."
    $pushOutput = git push origin main 2>&1
    $pushOutput | ForEach-Object { Write-Log "  $_" }
    
    # Check push result
    if ($LASTEXITCODE -ne 0) {
        throw "Git push failed with exit code $LASTEXITCODE"
    }
    
    $pushStatus = "Successfully pushed to https://github.com/haiyongchen/yxzx"
    Write-Log $pushStatus

    $endTime = Get-Date
    $duration = $endTime - $startTime

    $fileListStr = $fileList -join "`n"

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
