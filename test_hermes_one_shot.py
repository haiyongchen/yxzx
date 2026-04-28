# -*- coding: utf-8 -*-
import os
os.environ['OPENAI_API_KEY'] = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
os.environ['OPENAI_BASE_URL'] = 'https://coding.dashscope.aliyuncs.com/v1'

from openai import OpenAI
client = OpenAI()

print("Testing Hermes Agent with Bailian API...")
print("=" * 50)

test_message = "你好，请用中文介绍 Hermes Agent 是什么"
print(f"\nUser: {test_message}\n")

response = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        {"role": "system", "content": "你是 Hermes Agent，一个强大的 AI 助手"},
        {"role": "user", "content": test_message}
    ],
    max_tokens=300
)

print(f"Hermes: {response.choices[0].message.content}")
print("\n" + "=" * 50)
print("SUCCESS! Bailian API is working!")
