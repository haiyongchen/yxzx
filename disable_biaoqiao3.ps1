$ErrorActionPreference = 'SilentlyContinue'

# Try to directly overwrite the task XML file using cmd
$taskFile = "C:\Windows\System32\Tasks\BiaoQiaoWorkPlatformStartupTask"
$tempFile = "$env:TEMP\biaoqiao_task_modified.xml"

# Read and modify the XML
$xml = [xml](Get-Content $taskFile)
$ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
$ns.AddNamespace("t", "http://schemas.microsoft.com/windows/2004/02/mit/task")

# Modify trigger enabled
$triggerNodes = $xml.SelectNodes("//t:LogonTrigger/t:Enabled", $ns)
foreach ($node in $triggerNodes) {
    $node.InnerText = "false"
}

# Modify settings enabled  
$settingsEnabled = $xml.SelectNodes("//t:Settings/t:Enabled", $ns)
foreach ($node in $settingsEnabled) {
    $node.InnerText = "false"
}

# Save to temp first
$xml.Save($tempFile)
Write-Host "Saved modified XML to: $tempFile"
Write-Host "Modified content:"
Get-Content $tempFile

# Try to copy using cmd (might need admin)
Write-Host "`nTrying to overwrite task file..."
$result = cmd /c "copy /Y `"$tempFile`" `"$taskFile`"" 2>&1
Write-Host "Copy result: $result"

# Verify
if (Test-Path $taskFile) {
    $verify = [xml](Get-Content $taskFile)
    $triggerVal = $verify.SelectNodes("//t:LogonTrigger/t:Enabled", $ns)
    $settingsVal = $verify.SelectNodes("//t:Settings/t:Enabled", $ns)
    Write-Host "`nVerification - Trigger Enabled: $($triggerVal[0].InnerText)"
    Write-Host "Verification - Settings Enabled: $($settingsVal[0].InnerText)"
}
