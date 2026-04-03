# Test script for Feishu notification
$startTime = Get-Date

Write-Output "Test started at: $startTime"

# Simulate some work
Start-Sleep -Seconds 2

$endTime = Get-Date
$duration = $endTime - $startTime

$result = @{
    status = "success"
    message = "Test notification from OpenClaw cron job"
    startTime = $startTime.ToString("yyyy-MM-dd HH:mm:ss")
    endTime = $endTime.ToString("yyyy-MM-dd HH:mm:ss")
    duration = "$($duration.TotalSeconds) seconds"
}

Write-Output ($result | ConvertTo-Json)
Write-Output "Test completed!"
