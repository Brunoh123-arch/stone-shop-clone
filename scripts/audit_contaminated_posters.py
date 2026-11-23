# -*- coding: utf-8 -*-
"""
Audita se posters de outros produtos sao clones dos posters do chinelo (P104)
ou se ha posters apontando para arquivos de outros nichos.
"""
import re
import os
import hashlib

def get_hash(path):
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    vc_text = f.read()

# Coleta hashes dos posters do chinelo (P104)
chinelo_posters = re.findall(r'poster:\s*\(isPagesDir\s*\?\s*["\']\.\./["\']\s*:\s*["\']["\']\)\s*\+\s*["\']([^"\']+)["\']', vc_text)
# Posters gerais
all_poster_refs = re.findall(r'poster:\s*(?:\(isPagesDir\s*\?\s*["\']\.\./["\']\s*:\s*["\']["\']\)\s*\+\s*)?["\'](?:\.\./)?([^"\']+)["\']', vc_text)

print(f"Total de referencias a posters encontradas: {len(all_poster_refs)}")

# Pega os posters conhecidos do chinelo
chinelo_hashes = set()
for p in all_poster_refs:
    if 'chinelo' in p or 'sandalia' in p or '104' in p:
        h = get_hash(p)
        if h:
            chinelo_hashes.add(h)

print(f"Hashes unicos de posters do chinelo P104: {len(chinelo_hashes)}")

# Verifica quais produtos usam posters cujo hash bate com chinelo_hashes
contaminated = []
for p in set(all_poster_refs):
    if 'chinelo' not in p and 'sandalia' not in p and '104' not in p:
        h = get_hash(p)
        if h and h in chinelo_hashes:
            contaminated.append(p)

print("\n[!] POSTERS CONTAMINADOS COM A FOTO DO CHINELO:")
for c in sorted(contaminated):
    print(f"  [-] {c}")
