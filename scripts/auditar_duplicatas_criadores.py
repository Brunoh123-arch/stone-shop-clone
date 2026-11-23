import re

with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    c = f.read()

# Procurar arrays
arrays = re.findall(r'const\s+([A-Z0-9_]+)\s*=\s*\[([\s\S]*?)\];', c)
print(f"Total de arrays encontrados: {len(arrays)}")

for name, body in arrays:
    if any(k in name for k in ['CREATORS', 'VIDEOS', 'MAP', 'DATASET']):
        urls = re.findall(r'https://files\.catbox\.moe/[a-zA-Z0-9_-]+\.mp4|videosprodutos/[^"\']+\.mp4', body)
        users = re.findall(r'username:\s*["\']([^"\']+)["\']', body)
        
        dupe_urls = len(urls) - len(set(urls))
        dupe_users = len(users) - len(set(users))
        
        if dupe_urls > 0 or dupe_users > 0 or len(urls) > 0:
            print(f"Array: {name}")
            print(f"  Total URLs: {len(urls)} | Únicas: {len(set(urls))} | Duplicadas: {dupe_urls}")
            if users:
                print(f"  Total Users: {len(users)} | Únicos: {len(set(users))} | Duplicados: {dupe_users}")
            if dupe_urls > 0:
                # Mostrar quais URLs repetem
                from collections import Counter
                counts = Counter(urls)
                top_dupes = [u for u, cnt in counts.items() if cnt > 1]
                print(f"  Exemplos de URLs repetidas ({len(top_dupes)}): {top_dupes[:3]}")
