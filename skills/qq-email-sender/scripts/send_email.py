#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command line script for sending emails
Usage: python send_email.py "subject" "body"
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import directly from __init__.py
import importlib.util
spec = importlib.util.spec_from_file_location("qq_email_sender", os.path.join(parent_dir, "__init__.py"))
qq_email_sender = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qq_email_sender)
send_email = qq_email_sender.send_email


def main():
    if len(sys.argv) < 2:
        print("Usage: python send_email.py \"subject\" [\"body\"]")
        print("Example: python send_email.py \"任务完成\" \"数据处理已完成\"")
        sys.exit(1)
    
    subject = sys.argv[1]
    body = sys.argv[2] if len(sys.argv) > 2 else ""
    
    print(f"Sending email...")
    print(f"Subject: {subject}")
    
    result = send_email(subject, body)
    
    if result:
        print("[成功] 邮件发送成功")
    else:
        print("[失败] 邮件发送失败")
    
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
