# -*- coding: utf-8 -*-
"""
Simple Hermes-like chat using Bailian API
"""
import os
import sys

os.environ['OPENAI_API_KEY'] = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
os.environ['OPENAI_BASE_URL'] = 'https://coding.dashscope.aliyuncs.com/v1'

from openai import OpenAI

client = OpenAI()

print("=" * 50)
print("Hermes Agent (Simple) - Bailian qwen3.5-plus")
print("=" * 50)
print("Type 'quit' to exit\n")

while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        response = client.chat.completions.create(
            model="qwen3.5-plus",
            messages=[
                {"role": "system", "content": "你是 Hermes Agent，一个强大的 AI 助手"},
                {"role": "user", "content": user_input}
            ],
            max_tokens=1000
        )
        
        print(f"Hermes: {response.choices[0].message.content}\n")
    except Exception as e:
        print(f"Error: {e}\n")

print("\nGoodbye!")
