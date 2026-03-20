---
name: qq-email-sender
description: Send emails using QQ email SMTP server. Supports sending notifications with customizable subject and body content.
metadata:
  {
    "openclaw": {
      "emoji": "📧",
      "user-invocable": true,
      "requires": { "bins": ["python"] }
    }
  }
---

# QQ Email Sender Skill

Send emails using QQ email SMTP server (smtp.qq.com:465).

## Configuration

The skill uses the following default configuration:
- **SMTP Server**: smtp.qq.com
- **Port**: 465 (SSL)
- **Sender**: 631115784@qq.com
- **Receiver**: 631115784@qq.com

To use a different QQ email account, modify the configuration in `config.json`.

## Usage

### Send a simple notification email

```python
from skills.qq_email_sender import send_email

send_email(
    subject="任务完成",
    body="您的数据处理任务已成功完成。"
)
```

### Send with detailed content

```python
from skills.qq_email_sender import send_email

send_email(
    subject="专区数据同步完成",
    body="""
执行时间: 2026-03-20 08:30:00
处理文件: 2个
成功: 357条
失败: 16条
    """
)
```

## Python API

### `send_email(subject, body)`

Send an email notification.

**Parameters:**
- `subject` (str): Email subject line
- `body` (str): Email body content (plain text)

**Returns:**
- `bool`: True if sent successfully, False otherwise

**Example:**
```python
from skills.qq_email_sender import send_email

success = send_email(
    subject="[专区数据] 同步完成",
    body="任务执行成功，共处理357条记录。"
)

if success:
    print("邮件发送成功")
else:
    print("邮件发送失败")
```

## Command Line Usage

```bash
# Send test email
python skills/qq-email-sender/scripts/send_email.py "测试" "这是一封测试邮件"

# Send with custom content
python skills/qq-email-sender/scripts/send_email.py "任务完成" "数据处理已完成"
```

## Notes

1. Requires QQ email authorization code (not login password)
2. Uses SSL connection on port 465
3. Supports UTF-8 encoding for Chinese content
4. Default sender and receiver are the same email address
