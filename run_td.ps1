$content = Get-Content "D:\openclaw-workspace\oa_mail_for_upload_20260419_161246.md" -Raw -Encoding UTF8
$title = "OA 邮件分析报表-$(Get-Date -Format 'yyyyMMdd')"

& D:\openclaw-workspace\create_td.ps1 -Title $title -Mdx $content
