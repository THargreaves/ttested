import os
import re
import sys
import subprocess

for file in os.listdir('.\\content'):
    if file == '.ipynb_checkpoints' or file == 'markdown_formatter.py':
        continue
    print(f"Building post {file}")
    p = subprocess.Popen(['python.exe',
                    '.\\build_page.py',
                     file])
    p.communicate()
