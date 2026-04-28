# -*- coding: utf-8 -*-
import os
os.environ['OPENAI_API_KEY'] = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
os.environ['OPENAI_BASE_URL'] = 'https://coding.dashscope.aliyuncs.com/v1'

from openai import OpenAI
client = OpenAI()

print("Hermes Agent - Bailian Test")
print("=" * 40)

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ['quit', 'exit', 'q']:
        break
    
    response = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=[
            {"role": "system", "content": "You are Hermes Agent, a helpful AI assistant."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=500
    )
    
    print(f"Hermes: {response.choices[0].message.content}")

print("\nGoodbye!")
