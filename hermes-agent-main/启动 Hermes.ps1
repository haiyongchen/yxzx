# Hermes Agent Launcher for Windows
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$env:OPENAI_API_KEY = "sk-sp-896d84d6b8d946cea3d7e45d48c196dd"
$env:OPENAI_BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"
Set-Location -Path $PSScriptRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Hermes Agent - Starting...          " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "API: Bailian (qwen3.5-plus)" -ForegroundColor Gray
Write-Host ""

try {
    $pythonVersion = & python --version 2>&1
    Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found!" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "Starting..." -ForegroundColor Cyan
Write-Host ""

& python hermes @args
