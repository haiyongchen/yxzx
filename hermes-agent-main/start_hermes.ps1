# Hermes Agent Startup Script with Bailian Configuration
$env:PYTHONIOENCODING = "utf-8"
$env:OPENAI_API_KEY = "sk-sp-896d84d6b8d946cea3d7e45d48c196dd"
$env:OPENAI_BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Hermes Agent - Starting with Bailian  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "API Key: sk-sp-***" -ForegroundColor Gray
Write-Host "Base URL: https://coding.dashscope.aliyuncs.com/v1" -ForegroundColor Gray
Write-Host "Model: qwen3.5-plus" -ForegroundColor Gray
Write-Host ""

python hermes @args
