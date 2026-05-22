$ErrorActionPreference = 'SilentlyContinue'

# Get more details about the scheduled task
Write-Host "=== Task Details ==="
$task = Get-ScheduledTask -TaskName 'BiaoQiaoWorkPlatformStartupTask'
$task | Format-List *
$task.Actions | Format-List *
$task.Triggers | Format-List *

# Also search for the executable
Write-Host "`n=== Searching for BiaoQiao executable ==="
Get-ChildItem 'C:\','D:\' -Recurse -Depth 4 -Filter "*biaoqiao*" -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host $_.FullName
}
Get-ChildItem 'C:\','D:\' -Recurse -Depth 4 -Filter "*BiaoQiao*" -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host $_.FullName
}
