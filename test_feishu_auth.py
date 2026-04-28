# -*- coding: utf-8 -*-
"""Test Feishu credentials"""
import aiohttp
import asyncio
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

APP_ID = 'cli_a968bd97987bdcbd'
APP_SECRET = 'Fkrq2ArMDmHo2zm4Dpyxtd6lwXWlo6SE'

async def test():
    print("=" * 60)
    print("  测试飞书凭证")
    print("=" * 60)
    print(f"App ID: {APP_ID}")
    print(f"Secret: {APP_SECRET[:20]}...")
    print()
    
    # 获取 Tenant Access Token
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    
    print("正在获取 Tenant Access Token...")
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            result = await resp.json()
            
            if result.get('code') == 0:
                print("✅ 认证成功！")
                print(f"Token: {result.get('tenant_access_token', '')[:50]}...")
                print()
                print("凭证有效！可以在 Hermes 中使用。")
            else:
                print("❌ 认证失败！")
                print(f"错误码：{result.get('code')}")
                print(f"错误信息：{result.get('msg')}")
                print()
                print("请检查：")
                print("1. App ID 是否正确")
                print("2. App Secret 是否正确（重新生成）")
                print("3. 应用是否已发布")

if __name__ == '__main__':
    asyncio.run(test())
