import os

matches = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in dirs: dirs.remove('node_modules')
    if '.git' in dirs: dirs.remove('.git')
    for f in files:
        if f.endswith(('.json', '.py', '.txt', '.js')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    txt = fp.read()
                if 'bluey' in txt.lower():
                    matches.append(p)
            except:
                pass

print(f"Files mentioning bluey: {len(matches)}")
for m in matches:
    print(m)
