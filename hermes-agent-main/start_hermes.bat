@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set OPENAI_API_KEY=sk-sp-896d84d6b8d946cea3d7e45d48c196dd
set OPENAI_BASE_URL=https://coding.dashscope.aliyuncs.com/v1
echo Starting Hermes Agent with Bailian (阿里云百炼)...
echo.
python hermes %*
