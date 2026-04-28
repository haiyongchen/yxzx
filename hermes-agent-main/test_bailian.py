# -*- coding: utf-8 -*-
import os
import sys

# 设置环境变量
os.environ['OPENAI_API_KEY'] = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
os.environ['OPENAI_BASE_URL'] = 'https://coding.dashscope.aliyuncs.com/v1'

from openai import OpenAI

print("Testing Bailian API...")
print(f"API Key: {os.environ['OPENAI_API_KEY'][:10]}...")
print(f"Base URL: {os.environ['OPENAI_BASE_URL']}")
print()

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
    base_url=os.environ['OPENAI_BASE_URL']
)

try:
    response = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=[
            {"role": "user", "content": "你好，测试"}
        ],
        max_tokens=50
    )
    print("SUCCESS!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)
