@echo off
chcp 65001 >nul
title Hermes Gateway - Feishu

set OPENAI_API_KEY=sk-sp-896d84d6b8d946cea3d7e45d48c196dd
set OPENAI_BASE_URL=https://coding.dashscope.aliyuncs.com/v1
set GATEWAY_ALLOW_ALL_USERS=true
set PYTHONIOENCODING=utf-8

cd /d "%~dp0"

echo ============================================================
echo   Hermes Gateway - Feishu + Bailian
echo ============================================================
echo   App ID: cli_a968bd97987bdcbd
echo   Model: qwen3.5-plus
echo ============================================================
echo.

python hermes gateway run

pause
