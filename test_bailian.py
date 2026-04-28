# -*- coding: utf-8 -*-
"""
测试百炼 API 是否可用
"""
import os
import sys

# 设置 UTF-8 编码
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI

# 百炼配置
api_key = "sk-sp-896d84d6b8d946cea3d7e45d48c196dd"
base_url = "https://coding.dashscope.aliyuncs.com/v1"

client = OpenAI(api_key=api_key, base_url=base_url)

try:
    print("正在测试百炼 API...")
    response = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=[
            {"role": "user", "content": "你好，请用一句话介绍你自己"}
        ],
        max_tokens=50
    )
    print(f"✅ 百炼 API 正常！")
    print(f"回复：{response.choices[0].message.content}")
except Exception as e:
    print(f"❌ 百炼 API 测试失败：{e}")
