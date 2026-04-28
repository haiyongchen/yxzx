@echo off
chcp 65001 >nul 2>&1
title Hermes Agent - 百炼

echo ========================================
echo   Hermes Agent - Starting...
echo ========================================
echo.
echo API: 阿里云百炼
echo Model: qwen3.5-plus
echo.

set OPENAI_API_KEY=sk-sp-896d84d6b8d946cea3d7e45d48c196dd
set OPENAI_BASE_URL=https://coding.dashscope.aliyuncs.com/v1
set PYTHONIOENCODING=utf-8

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

echo [信息] Python 已就绪
echo [信息] 启动 Hermes Agent...
echo.

REM 切换到 Hermes 目录
cd /d "%~dp0"

REM 启动 Hermes
python hermes %*

echo.
echo [错误] Hermes 已退出，按任意键关闭...
pause >nul
