import re, os, sys

sys.stdout.reconfigure(encoding='utf-8')

files = [
    os.path.expandvars(r'%APPDATA%\EpointMsg\mergedMsgFiles\34683854.html'),
    os.path.expandvars(r'%APPDATA%\EpointMsg\mergedMsgFiles\1778747294638.html')
]

output = []

for fpath in files:
    output.append(f'=== {os.path.basename(fpath)} ===')
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    blocks = html.split('rong-message ')
    for block in blocks:
        name_m = re.search(r"userName'>(.*?)</span>", block)
        time_m = re.search(r"sendTime'>(.*?)</span>", block)
        text_m = re.search(r"rongcloud-message-entry'>(.*?)</pre>", block)
        file_m = re.search(r'<div>([^<]+)</div><div>(\d+[\.\d]* [KMG]?B)', block)
        combine_m = re.search(r"rong-combine-title'>(.*?)</div>", block)
        
        if name_m and time_m:
            name = name_m.group(1)
            time = time_m.group(1)
            if text_m:
                content = text_m.group(1)
            elif file_m:
                content = f'[文件] {file_m.group(1)} ({file_m.group(2)})'
            elif combine_m:
                content = f'[合并转发] {combine_m.group(1)}'
            else:
                content = '[其他消息类型]'
            output.append(f'[{time}] {name} : {content}')
    output.append('')

with open(r'D:\openclaw-workspace\chat_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print('Done')
