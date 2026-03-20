#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件发送脚本 - 用于专区数据同步任务通知
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime


def send_zone_email(subject_content="", body_content=""):
    """
    发送专区数据同步任务邮件
    """
    
    # 邮件配置
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    sender_email = "631115784@qq.com"
    sender_password = "jmxrfcsmhxzabfec"
    receiver_email = "631115784@qq.com"
    
    # 构建邮件主题
    subject = f"[专区数据同步任务执行] {subject_content}"
    
    # 构建邮件正文
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not body_content:
        body_content = f"""
专区数据同步任务执行通知

执行时间: {current_time}
任务状态: 执行完成

处理文件:
1. 专区接入情况统计表.xlsx
2. 专区信息汇总表_按省份分类.xlsx

如有问题，请检查附件或联系管理员。

---
此邮件由系统自动发送
"""
    
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    # 添加邮件正文
    msg.attach(MIMEText(body_content, 'plain', 'utf-8'))
    
    try:
        # 连接SMTP服务器并发送
        print(f"正在连接 {smtp_server}:{smtp_port}...")
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            print("正在登录...")
            server.login(sender_email, sender_password)
            print("正在发送邮件...")
            server.sendmail(sender_email, receiver_email, msg.as_string())
        
        print("[成功] 邮件发送成功!")
        print(f"  收件人: {receiver_email}")
        print(f"  主题: {subject}")
        return True
        
    except Exception as e:
        print(f"[失败] 邮件发送失败: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    # 如果有参数，使用参数作为邮件内容
    if len(sys.argv) > 1:
        subject = sys.argv[1]
        body = sys.argv[2] if len(sys.argv) > 2 else ""
        send_zone_email(subject, body)
    else:
        # 测试发送
        print("=" * 60)
        print("测试发送邮件...")
        print("=" * 60)
        send_zone_email(
            subject_content="测试",
            body_content="这是测试邮件，验证邮件发送功能是否正常。"
        )
