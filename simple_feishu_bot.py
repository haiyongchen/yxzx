#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Feishu Bot with Bailian qwen3.5-plus
Direct implementation without Hermes complexity
"""
import os
import sys
import json
import aiohttp
import asyncio
from openai import OpenAI

# ===== Configuration =====
FEISHU_APP_ID = 'cli_a968bd97987bdcbd'
FEISHU_APP_SECRET = 'Vt5tzOx4R9F6Aa7YhIQWRbV6ND1b0uQ0'

BAILOAN_API_KEY = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
BAILOAN_BASE_URL = 'https://coding.dashscope.aliyuncs.com/v1'
# =========================

client = OpenAI(api_key=BAILOAN_API_KEY, base_url=BAILOAN_BASE_URL)

print("=" * 70)
print("  Simple Feishu Bot - Bailian qwen3.5-plus")
print("=" * 70)
print(f"  App ID:  {FEISHU_APP_ID}")
print(f"  Model:   qwen3.5-plus")
print("=" * 70)
print()

async def get_tenant_access_token():
    """Get Feishu tenant access token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            result = await resp.json()
            if result.get('code') == 0:
                return result['tenant_access_token']
            else:
                print(f"[ERROR] Get token failed: {result}")
                return None

async def reply_message(token, msg_id, content):
    """Reply to a Feishu message"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "msg_type": "text",
        "content": json.dumps({"text": content}),
        "reply_id": msg_id
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            result = await resp.json()
            return result.get('code') == 0

async def chat_with_bailian(user_message):
    """Chat with Bailian qwen3.5-plus"""
    try:
        response = client.chat.completions.create(
            model="qwen3.5-plus",
            messages=[
                {"role": "system", "content": "你是 Hermes Agent，一个友好的 AI 助手"},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Error] {e}"

async def main_loop():
    """Main bot loop - polling for messages"""
    print("[INFO] Bot started. Polling for messages...")
    print("[INFO] Press Ctrl+C to stop\n")
    
    token = await get_tenant_access_token()
    if not token:
        print("[ERROR] Failed to get access token. Exiting.")
        return
    
    print(f"[OK] Got tenant access token")
    
    # Simple polling (in production, use webhook instead)
    last_msg_id = None
    
    while True:
        try:
            await asyncio.sleep(5)  # Poll every 5 seconds
            
            # TODO: Implement message polling or use webhook
            # For now, this is a placeholder
            # In production, you would:
            # 1. Use Feishu webhook to receive messages
            # 2. Call chat_with_bailian() to get response
            # 3. Call reply_message() to send response
            
        except KeyboardInterrupt:
            print("\n[INFO] Stopped by user")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            await asyncio.sleep(5)

if __name__ == '__main__':
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\nStopped")
