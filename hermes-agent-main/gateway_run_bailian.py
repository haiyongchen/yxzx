# -*- coding: utf-8 -*-
"""Direct gateway launch with Bailian - bypassing Hermes config system"""
import os
import sys
import io
import asyncio

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Hardcode credentials
API_KEY = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
BASE_URL = 'https://coding.dashscope.aliyuncs.com/v1'
FEISHU_APP_ID = 'cli_a968bd97987bdcbd'
FEISHU_APP_SECRET = 'Vt5tzOx4R9F6Aa7YhIQWRbV6ND1b0uQ0'

os.environ['OPENAI_API_KEY'] = API_KEY
os.environ['OPENAI_BASE_URL'] = BASE_URL
os.environ['GATEWAY_ALLOW_ALL_USERS'] = 'true'

print("=" * 60)
print("Hermes Gateway - Direct Bailian + Feishu")
print("=" * 60)
print(f"App ID: {FEISHU_APP_ID}")
print(f"Model: qwen3.5-plus")
print(f"Port: 18789")
print("=" * 60)
print()

# Import and configure gateway directly
from gateway.run import start_gateway

async def run():
    # Set up minimal config
    from hermes_cli import config as hconfig
    hconfig.get_config = lambda: {
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
    
    try:
        await start_gateway(replace=True, verbosity=1)
    except KeyboardInterrupt:
        print("\nStopped")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(run())
