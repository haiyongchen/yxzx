# -*- coding: utf-8 -*-
import os
import sys

os.environ['OPENAI_API_KEY'] = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
os.environ['OPENAI_BASE_URL'] = 'https://coding.dashscope.aliyuncs.com/v1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

sys.path.insert(0, 'D:/openclaw-workspace/hermes-agent-main')

from openai import OpenAI

print("Testing Hermes with Bailian...")

client = OpenAI()

response = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        {"role": "system", "content": "你是 Hermes Agent"},
        {"role": "user", "content": "你好，请用中文介绍你自己"}
    ],
    max_tokens=200
)

print(f"Response: {response.choices[0].message.content}")
print("SUCCESS!")
