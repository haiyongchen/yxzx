#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FINAL Gateway Launcher - Forces Feishu + Bailian
"""
import os
import sys
import io
import asyncio

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ===== HARDCODE CREDENTIALS =====
API_KEY = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
BASE_URL = 'https://coding.dashscope.aliyuncs.com/v1'
FEISHU_APP_ID = 'cli_a968bd97987bdcbd'
FEISHU_APP_SECRET = 'Vt5tzOx4R9F6Aa7YhIQWRbV6ND1b0uQ0'
# ================================

os.environ['OPENAI_API_KEY'] = API_KEY
os.environ['OPENAI_BASE_URL'] = BASE_URL
os.environ['GATEWAY_ALLOW_ALL_USERS'] = 'true'
os.environ['PYTHONIOENCODING'] = 'utf-8'

print("=" * 70)
print("  Hermes Agent - Feishu Gateway")
print("=" * 70)
print(f"  App ID:     {FEISHU_APP_ID}")
print(f"  Model:      qwen3.5-plus (AliBailian)")
print(f"  Port:       18789")
print(f"  API Key:    {API_KEY[:15]}...")
print("=" * 70)
print()

# Force config override
import hermes_cli
hermes_cli._config_cache = {
    'model': {'default': 'qwen3.5-plus'},
    'providers': {
        'openai': {
            'enabled': True,
            'api_key': API_KEY,
            'base_url': BASE_URL
        }
    },
    'gateway': {
        'enabled': True,
        'feishu': {
            'enabled': True,
            'app_id': FEISHU_APP_ID,
            'app_secret': FEISHU_APP_SECRET
        }
    },
    'gateway_allow_all_users': True
}

# Import gateway
sys.path.insert(0, os.getcwd())
from gateway import run

async def main():
    try:
        await run.start_gateway(replace=True, verbosity=2)
    except KeyboardInterrupt:
        print("\n\n[INFO] Stopped by user")
    except Exception as e:
        print(f"\n\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())
