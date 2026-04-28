@echo off
chcp 65001 >nul
set TENCENT_DOCS_TOKEN=e23255dcdf51491cb208ecc9cc341e21

echo 🚀 创建腾讯文档...

mcporter call tencent-docs create_smartcanvas_by_mdx --title "OA 邮件分析报表 -20260419" --mdx "# 📧 OA 邮件分析报表^

^

**分析时间**: 2026-04-19^

**时间范围**: 最近 7 天^

**邮件总数**: 15 封"
