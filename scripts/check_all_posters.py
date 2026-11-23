# -*- coding: utf-8 -*-
import re
import os

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Captura todos os posters
matches = re.findall(r'poster:\s*(?:\(isPagesDir\s*\?\s*["\']\.\./["\']\s*:\s*["\']["\']\)\s*\+\s*)?["\'](?:\.\./)?([^"\']+)["\']', text)
unique_posters = sorted(list(set(matches)))

missing = []
for p in unique_posters:
    # Remove ../ se houver
    clean_p = p.lstrip('./').replace('\\', '/')
    if not os.path.exists(clean_p) and not os.path.exists(p):
        missing.append(p)

print(f"Total de posters unicos referenciados: {len(unique_posters)}")
print(f"Posters inexistentes no disco: {len(missing)}")
if missing:
    for m in missing:
        print(f"  [-] Inexistente: {m}")
