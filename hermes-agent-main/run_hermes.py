# -*- coding: utf-8 -*-
"""
Hermes Agent Launcher with Bailian Configuration
"""
import os
import sys

# Set environment variables for Bailian
os.environ['OPENAI_API_KEY'] = 'sk-sp-896d84d6b8d946cea3d7e45d48c196dd'
os.environ['OPENAI_BASE_URL'] = 'https://coding.dashscope.aliyuncs.com/v1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Change to Hermes directory
os.chdir(r'D:\openclaw-workspace\hermes-agent-main')

# Import and run Hermes
from hermes_cli.main import main

if __name__ == '__main__':
    sys.argv = ['hermes'] + sys.argv[1:]
    main()
