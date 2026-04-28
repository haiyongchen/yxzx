#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FINAL Feishu Gateway - Direct launch with FeishuAdapter
"""
import os
import sys
import asyncio

sys.path.insert(0, 'D:/openclaw-workspace/hermes-agent-main')
sys.path.insert(0, 'D:/openclaw-workspace/hermes-agent-main/gateway')

API_KEY = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
BASE_URL = 'https://coding.dashscope.aliyuncs.com/v1'
FEISHU_APP_ID = 'cli_a968bd97987bdcbd'
FEISHU_APP_SECRET = 'Vt5tzOx4R9F6Aa7YhIQWRbV6ND1b0uQ0'

os.environ['OPENAI_API_KEY'] = API_KEY
os.environ['OPENAI_BASE_URL'] = BASE_URL

print("=" * 70)
print("  Hermes Feishu Gateway")
print("=" * 70)
print(f"  App ID:  {FEISHU_APP_ID}")
print(f"  Model:   qwen3.5-plus (Bailian)")
print("=" * 70)
print()

from gateway.platforms.feishu import FeishuAdapter, FeishuAdapterSettings

async def run():
    settings = FeishuAdapterSettings(
        app_id=FEISHU_APP_ID,
        app_secret=FEISHU_APP_SECRET
    )
    
    adapter = FeishuAdapter(settings)
    
    try:
        await adapter.connect()
        print("\n[OK] Feishu connected successfully!")
        print("[INFO] Gateway is running. Press Ctrl+C to stop.\n")
        await asyncio.Future()
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(run())
