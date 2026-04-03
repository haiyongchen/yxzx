#!/usr/bin/env python3
import subprocess
import sys

script_path = r"D:\openclaw-workspace\scripts\epoint_data_processor.py"
print(f"Running: {script_path}")
print("="*60)

process = subprocess.Popen(
    [sys.executable, script_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

for line in process.stdout:
    print(line, end='')

process.wait()
print("="*60)
print(f"Exit code: {process.returncode}")
