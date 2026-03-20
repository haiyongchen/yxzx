#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ Email Sender Skill
Send emails using QQ email SMTP server
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json

# Default configuration
DEFAULT_CONFIG = {
    "smtp_server": "smtp.qq.com",
    "smtp_port": 465,
    "sender_email": "631115784@qq.com",
    "sender_password": "jmxrfcsmhxzabfec",  # Authorization code
    "receiver_email": "631115784@qq.com"
}


def load_config():
    """Load configuration from config.json if exists"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_CONFIG


def send_email(subject, body, config=None):
    """
    Send an email using QQ SMTP server
    
    Args:
        subject (str): Email subject
        body (str): Email body content
        config (dict, optional): Custom configuration. If None, uses default.
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    cfg = config or load_config()
    
    smtp_server = cfg.get('smtp_server', DEFAULT_CONFIG['smtp_server'])
    smtp_port = cfg.get('smtp_port', DEFAULT_CONFIG['smtp_port'])
    sender_email = cfg.get('sender_email', DEFAULT_CONFIG['sender_email'])
    sender_password = cfg.get('sender_password', DEFAULT_CONFIG['sender_password'])
    receiver_email = cfg.get('receiver_email', DEFAULT_CONFIG['receiver_email'])
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        
        # Attach body
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Send email
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        
        return True
        
    except Exception as e:
        print(f"[Email Error] {e}")
        return False


# Convenience function for zone data notifications
def send_zone_notification(status, details=""):
    """
    Send a zone data synchronization notification
    
    Args:
        status (str): Status message (e.g., "完成", "失败")
        details (str): Additional details
    """
    subject = f"[专区数据同步任务执行] {status}"
    
    if not details:
        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        details = f"执行时间: {current_time}\n任务状态: {status}"
    
    return send_email(subject, details)


if __name__ == "__main__":
    # Test
    print("Testing QQ Email Sender...")
    result = send_email("[测试] QQ邮件发送功能", "这是一封测试邮件，验证功能是否正常。")
    print(f"Result: {'成功' if result else '失败'}")
