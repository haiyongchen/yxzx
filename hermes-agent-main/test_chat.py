# -*- coding: utf-8 -*-
"""
测试 Hermes Agent 与百炼对话
"""
import os
import sys

os.environ['OPENAI_API_KEY'] = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
os.environ['OPENAI_BASE_URL'] = 'https://coding.dashscope.aliyuncs.com/v1'

from openai import OpenAI

client = OpenAI()

print(" Hermes Agent (百炼) - 测试对话\n")
print("用户：你好，请用一句话介绍 Hermes Agent")
print()

response = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        {"role": "system", "content": "你是 Hermes Agent，一个强大的 AI 助手"},
        {"role": "user", "content": "你好，请用一句话介绍 Hermes Agent"}
    ],
    max_tokens=200
)

print(f"Hermes: {response.choices[0].message.content}\n")
print("✅ 测试成功！")
