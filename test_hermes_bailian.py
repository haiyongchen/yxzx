# -*- coding: utf-8 -*-
"""
测试 Hermes Agent 使用百炼 API
"""
import os
import sys

# 设置环境变量
os.environ['OPENAI_API_KEY'] = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
os.environ['OPENAI_BASE_URL'] = 'https://coding.dashscope.aliyuncs.com/v1'

# 设置 UTF-8 编码
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI

# 从环境变量读取配置
client = OpenAI()

try:
    print("正在通过 Hermes Agent 配置测试百炼 API...")
    print(f"API Key: {os.environ.get('OPENAI_API_KEY', 'NOT SET')[:10]}...")
    print(f"Base URL: {os.environ.get('OPENAI_BASE_URL', 'NOT SET')}")
    print()
    
    response = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=[
            {"role": "user", "content": "你好，Hermes Agent 正在使用百炼 API，请用一句话确认"}
        ],
        max_tokens=100
    )
    
    print("✅ Hermes Agent + 百炼 API 配置成功！")
    print(f"模型：qwen3.5-plus")
    print(f"回复：{response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ 测试失败：{e}")
