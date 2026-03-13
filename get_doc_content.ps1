# 读取腾讯文档内容
$env:TENCENT_DOCS_TOKEN = "e23255dcdf51491cb208ecc9cc341e21"
$jsonArgs = '{"file_id":"DQnZoWXpYQU5HVEpz"}'
mcporter call tencent-docs.get_content --args $jsonArgs
