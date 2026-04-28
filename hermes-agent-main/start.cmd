@echo off
title Hermes Agent - Bailian
setlocal

set OPENAI_API_KEY=sk-sp-896d84d6b8d946cea3d7e45d48c196dd
set OPENAI_BASE_URL=https://coding.dashscope.aliyuncs.com/v1
set PYTHONIOENCODING=utf-8

cd /d "%~dp0"

echo ========================================
echo   Hermes Agent - Bailian (qwen3.5-plus)
echo ========================================
echo.

python hermes %*

endlocal
pause
