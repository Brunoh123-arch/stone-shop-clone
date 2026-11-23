import re

with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    c = f.read()

matches = list(re.finditer(r'const\s+([A-Z0-9_]+)\s*=\s*\[', c))
dupes_found = 0

for m in matches:
    name = m.group(1)
    if not any(k in name for k in ['CREATORS', 'VIDEOS', 'MAP', 'DATASET']):
        continue
    start = m.end()
    end = c.find('];', start)
    if end != -1:
        block = c[start:end]
        urls = re.findall(r'https://files\.catbox\.moe/[a-zA-Z0-9_-]+\.mp4|videosprodutos/[^"\']+\.mp4', block)
        if len(urls) > len(set(urls)):
            dupes_found += 1
            print(f"DUPLICATA REAL em {name}: {len(urls)} total, {len(set(urls))} únicos!")

print(f"\nTotal de arrays de criadores com vídeos repetidos: {dupes_found}")
if dupes_found == 0:
    print("PERFEITO! ZERO ARRAYS COM VÍDEOS REPETIDOS EM JS/VIDEOS-CRIADORES.JS!")
