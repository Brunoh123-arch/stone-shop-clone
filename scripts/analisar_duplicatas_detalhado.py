import re

with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    c = f.read()

arrays = re.findall(r'const\s+([A-Z0-9_]+)\s*=\s*\[([\s\S]*?)\];', c)
duped_arrays = []

for name, body in arrays:
    if any(k in name for k in ['CREATORS', 'VIDEOS', 'MAP', 'DATASET']):
        urls = re.findall(r'https://files\.catbox\.moe/[a-zA-Z0-9_-]+\.mp4|videosprodutos/[^"\']+\.mp4', body)
        if len(urls) > len(set(urls)):
            duped_arrays.append((name, len(urls), len(set(urls))))

print(f"Total de arrays com vídeos duplicados: {len(duped_arrays)}")
for name, tot, unq in duped_arrays:
    print(f"  {name}: {tot} total -> {unq} únicos (remove {tot - unq} repetições)")
