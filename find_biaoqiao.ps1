$ErrorActionPreference = 'SilentlyContinue'

# Search for startup entries related to biaoqiao
Write-Host "=== Searching for BiaoQiao startup entries ==="

# Check registry Run keys
$paths = @(
    'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run',
    'HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce',
    'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run',
    'HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce',
    'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run'
)

foreach ($path in $paths) {
    $props = Get-ItemProperty -Path $path
    if ($props) {
        $props.PSObject.Properties | Where-Object { $_.Name -notmatch '^PS' } | ForEach-Object {
            if ($_.Value -match 'biaoqiao|BiaoQiao|标桥') {
                Write-Host "FOUND in $path : $($_.Name) = $($_.Value)"
            }
        }
    }
}

# Search for the program on disk
Write-Host "`n=== Searching for BiaoQiao on disk ==="
$drives = @('C:\', 'D:\')
foreach ($drive in $drives) {
    if (Test-Path $drive) {
        Get-ChildItem $drive -Directory -Depth 2 -ErrorAction SilentlyContinue | Where-Object {
            $_.Name -match 'biaoqiao|BiaoQiao|标桥'
        } | ForEach-Object {
            Write-Host "Found directory: $($_.FullName)"
        }
    }
}

# Check startup folders
Write-Host "`n=== Checking startup folders ==="
$startupPaths = @(
    "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup",
    "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
)
foreach ($sp in $startupPaths) {
    if (Test-Path $sp) {
        Get-ChildItem $sp -ErrorAction SilentlyContinue | Where-Object {
            $_.Name -match 'biaoqiao|BiaoQiao|标桥'
        } | ForEach-Object {
            Write-Host "Found in startup folder: $($_.FullName)"
        }
    }
}

# Check scheduled tasks
Write-Host "`n=== Checking scheduled tasks ==="
Get-ScheduledTask 2>$null | Where-Object {
    $_.TaskName -match 'biaoqiao|BiaoQiao' -or $_.TaskPath -match 'biaoqiao|BiaoQiao'
} | ForEach-Object {
    Write-Host "Scheduled task: $($_.TaskName) at $($_.TaskPath) - State: $($_.State)"
}

# Search registry more broadly
Write-Host "`n=== Searching registry for BiaoQiao ==="
$regPaths = @(
    'HKCU:\Software\Microsoft\Windows\CurrentVersion',
    'HKLM:\Software\Microsoft\Windows\CurrentVersion'
)
foreach ($rp in $regPaths) {
    Get-ChildItem $rp -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
        $props = Get-ItemProperty -Path $_.PSPath -ErrorAction SilentlyContinue
        if ($props) {
            $props.PSObject.Properties | ForEach-Object {
                if ($_.Value -is [string] -and $_.Value -match 'biaoqiao|BiaoQiao|标桥') {
                    Write-Host "Registry: $($_.Name) = $($_.Value) in $($_.PSPath)"
                }
            }
        }
    }
}
