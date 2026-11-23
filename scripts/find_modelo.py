import os, glob, re

for md in glob.glob('*.md') + glob.glob('scripts/*.md') + glob.glob('scripts/*.txt'):
    with open(md, 'r', encoding='utf-8', errors='ignore') as f:
        txt = f.read()
    if 'produto modelo' in txt.lower() or 'página modelo' in txt.lower() or 'modelo canônico' in txt.lower():
        print("Found in:", md)
        for line in txt.splitlines():
            if any(k in line.lower() for k in ['produto modelo', 'página modelo', 'modelo canônico', 'referência']):
                print("  ->", line)
