# -*- coding: utf-8 -*-
"""
Configure Feishu (Lark) Bot for Hermes Agent
"""
import os
import yaml

# Feishu Bot Configuration
FEISHU_APP_ID = "cli_a968bd97987bdcbd"
FEISHU_APP_SECRET = "Vt5tzOx4R9F6Aa7YhIQWRbV6ND1b0uQ0"

# Hermes home directory
hermes_home = os.path.expanduser("~/.hermes")

# Load existing config
config_path = os.path.join(hermes_home, "config.yaml")
if os.path.exists(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
else:
    config = {}

# Add Feishu gateway configuration
if "gateway" not in config:
    config["gateway"] = {}

config["gateway"]["feishu"] = {
    "enabled": True,
    "app_id": FEISHU_APP_ID,
    "app_secret": FEISHU_APP_SECRET,
    "domain": "feishu"
}

# Save config
with open(config_path, "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

print(f"Feishu configuration written to: {config_path}")
print("\nConfiguration:")
print(f"  App ID: {FEISHU_APP_ID}")
print(f"  App Secret: {FEISHU_APP_SECRET[:10]}...")
print(f"  Domain: feishu")
print("\nNext steps:")
print("1. In Feishu Bot console, set the webhook URL to:")
print("   http://localhost:18789/feishu/webhook")
print("2. Run: python hermes gateway run")
