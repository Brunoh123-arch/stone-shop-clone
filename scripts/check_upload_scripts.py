import glob
import os

scripts = glob.glob('scripts/*catbox*') + glob.glob('scripts/*upload*')
print('Upload/Catbox scripts:', scripts)
for s in scripts:
    print(f'=== {s} ===')
    with open(s, 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read()[:600])
