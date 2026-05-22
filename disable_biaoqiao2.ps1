$ErrorActionPreference = 'SilentlyContinue'

# Check the task XML file directly
$taskFile = "C:\Windows\System32\Tasks\BiaoQiaoWorkPlatformStartupTask"
if (Test-Path $taskFile) {
    Write-Host "Task file found: $taskFile"
    $xml = [xml](Get-Content $taskFile)
    Write-Host "`nCurrent XML:"
    $xml.OuterXml
    
    # Try to modify the Enabled field in Triggers
    $ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
    $ns.AddNamespace("t", "http://schemas.microsoft.com/windows/2004/02/mit/task")
    
    $triggerNodes = $xml.SelectNodes("//t:LogonTrigger/t:Enabled", $ns)
    foreach ($node in $triggerNodes) {
        Write-Host "`nCurrent trigger Enabled: $($node.InnerText)"
        $node.InnerText = "false"
        Write-Host "Changed to: $($node.InnerText)"
    }
    
    # Also check Settings Enabled
    $settingsEnabled = $xml.SelectNodes("//t:Settings/t:Enabled", $ns)
    foreach ($node in $settingsEnabled) {
        Write-Host "`nCurrent settings Enabled: $($node.InnerText)"
    }
    
    # Save the modified XML
    $xml.Save($taskFile)
    Write-Host "`nModified XML saved successfully!"
    
    # Verify the change
    $xml2 = [xml](Get-Content $taskFile)
    Write-Host "`nVerified XML after save:"
    $xml2.OuterXml
} else {
    Write-Host "Task file not found at $taskFile"
}

# Also check the program directory for settings
Write-Host "`n=== Checking program directory ==="
$progDir = "D:\Epoint"
if (Test-Path $progDir) {
    Get-ChildItem $progDir -Recurse -Depth 3 -ErrorAction SilentlyContinue | Where-Object {
        $_.Name -match 'config|setting|ini|xml|json' -and $_.Name -match 'biaoqiao|EpLauncher|Epoint'
    } | ForEach-Object {
        Write-Host "Config file: $($_.FullName)"
    }
    
    # Also list the main directory
    Write-Host "`nEpoint directory contents:"
    Get-ChildItem $progDir -Depth 1 | ForEach-Object {
        Write-Host $_.FullName
    }
}
