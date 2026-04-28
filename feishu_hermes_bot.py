#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feishu Bot with Hermes + Bailian qwen3.5-plus
Standalone version - No complex Hermes config needed
"""
import os
import sys
import json
import asyncio
from aiohttp import web
from openai import OpenAI

# ===== Configuration =====
FEISHU_APP_ID = 'cli_a968bd97987bdcbd'
FEISHU_APP_SECRET = 'Vt5tzOx4R9F6Aa7YhIQWRbV6ND1b0uQ0'

BAILOAN_API_KEY = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
BAILOAN_BASE_URL = 'https://coding.dashscope.aliyuncs.com/v1'

PORT = 8080
# =========================

client = OpenAI(api_key=BAILOAN_API_KEY, base_url=BAILOAN_BASE_URL)

print("=" * 70)
print("  Feishu Bot - Hermes + Bailian qwen3.5-plus")
print("=" * 70)
print(f"  App ID:     {FEISHU_APP_ID}")
print(f"  Model:      qwen3.5-plus")
print(f"  Webhook:    http://YOUR_IP:{PORT}/feishu/webhook")
print("=" * 70)
print()

async def get_tenant_token():
    """Get Feishu tenant access token"""
    import aiohttp
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            result = await resp.json()
            return result.get('tenant_access_token')

async def reply_message(token, reply_id, text):
    """Reply to Feishu message"""
    import aiohttp
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "msg_type": "text",
        "content": json.dumps({"text": text}),
        "reply_id": reply_id
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            return await resp.json()

def chat_with_bailian(user_msg):
    """Chat with Bailian"""
    try:
        resp = client.chat.completions.create(
            model="qwen3.5-plus",
            messages=[
                {"role": "system", "content": "你是 Hermes Agent，友好的 AI 助手"},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=500
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[Error] {e}"

async def handle_webhook(request):
    """Handle Feishu webhook"""
    try:
        data = await request.json()
        print(f"[Webhook] Received: {data.get('type')}")
        
        # Challenge response for webhook verification
        if data.get('type') == 'url_verification':
            return web.json_response({'challenge': data.get('challenge')})
        
        # Handle message
        if data.get('type') == 'im.message.receive_v1':
            msg_data = data.get('event', {}).get('message', {})
            sender = msg_data.get('sender', {}).get('sender_id', {}).get('open_id')
            msg_id = msg_data.get('message_id')
            content = json.loads(msg_data.get('content', '{}'))
            text = content.get('text', '')
            
            print(f"[Message] From {sender}: {text[:50]}...")
            
            # Get AI response
            ai_response = chat_with_bailian(text)
            print(f"[AI] Response: {ai_response[:50]}...")
            
            # Reply
            token = await get_tenant_token()
            if token:
                await reply_message(token, msg_id, ai_response)
                print(f"[OK] Replied to {sender}")
        
        return web.json_response({'status': 'ok'})
    
    except Exception as e:
        print(f"[ERROR] {e}")
        return web.json_response({'status': 'error'}, status=500)

async def on_startup(app):
    print(f"\n[OK] Webhook server started on port {PORT}")
    print(f"[INFO] Configure Feishu webhook URL:")
    print(f"       http://YOUR_SERVER_IP:{PORT}/feishu/webhook")
    print(f"\n[INFO] Waiting for messages...\n")

def create_app():
    app = web.Application()
    app.router.add_post('/feishu/webhook', handle_webhook)
    app.on_startup.append(on_startup)
    return app

if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=PORT, print=None)
