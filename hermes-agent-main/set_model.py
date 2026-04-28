# -*- coding: utf-8 -*-
import os
import json
import yaml

# 设置配置
config = {
    "model": {
        "default": "qwen3.5-plus"
    },
    "providers": {
        "openai": {
            "enabled": True,
            "api_key": "sk-sp-896d84d6b8d946cea3d7e45d48c196dd",
            "base_url": "https://coding.dashscope.aliyuncs.com/v1"
        }
    },
    "agent": {
        "name": "Hermes",
        "temperature": 0.7
    }
}

# 写入 config.yaml
hermes_home = os.path.expanduser("~/.hermes")
config_path = os.path.join(hermes_home, "config.yaml")

with open(config_path, "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

print(f"Config written to: {config_path}")
print("Config content:")
print(yaml.dump(config, allow_unicode=True))
