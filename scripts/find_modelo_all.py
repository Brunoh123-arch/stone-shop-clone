import os, glob, re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.md'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
                txt = fh.read()
            if 'produto modelo' in txt.lower() or 'página modelo' in txt.lower() or 'modelo canônico' in txt.lower() or 'referência canônica' in txt.lower():
                print("Found in:", p)
                for line in txt.splitlines():
                    if any(k in line.lower() for k in ['produto modelo', 'página modelo', 'modelo canônico', 'referência canônica']):
                        print("  ->", line[:100])
