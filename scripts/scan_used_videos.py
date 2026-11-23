import os
import re

used_videos = set()
pattern = re.compile(r'["\'`]([^"\'`\s<>]+\.(?:mp4|webm|mov))["\'`]', re.IGNORECASE)

for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.vercel', 'scripts']):
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.css', '.json')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                    content = fl.read()
                    matches = pattern.findall(content)
                    for m in matches:
                        clean = m.split('?')[0].split('#')[0].replace('\\', '/')
                        used_videos.add((clean, os.path.basename(clean), p))
            except Exception as e:
                pass

print(f"Total de referencias achadas: {len(used_videos)}")
# Group by basename
by_base = {}
for full, base, src in used_videos:
    if base not in by_base:
        by_base[base] = []
    by_base[base].append((full, src))

print(f"Arquivos unicos de video referenciados no codigo: {len(by_base)}")
for base, refs in sorted(by_base.items()):
    print(f"\n[VIDEO] {base}")
    for full, src in refs[:3]:
        print(f"  ref: '{full}' em {src}")
