# Export the task XML, modify it to disable, and reimport
$xmlPath = "C:\Users\63111\AppData\Local\Temp\biaoqiao_task.xml"
schtasks /Query /TN "BiaoQiaoWorkPlatformStartupTask" /XML ONE > $xmlPath 2>&1
Write-Host "Exported XML:"
Get-Content $xmlPath
