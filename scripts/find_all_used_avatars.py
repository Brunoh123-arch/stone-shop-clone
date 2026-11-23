import glob, re, os

used = set()
for h in glob.glob('pages/*.html'):
    with open(h, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
        for m in re.findall(r'src="([^"]+)"', c):
            if any(k in m for k in ['review', 'avatar', 'user', 'mulher', 'homem']):
                used.add((m, os.path.basename(h)))

print(f"Total de referencias: {len(used)}")
# Agrupar por pasta de imagem
from collections import defaultdict
folders = defaultdict(list)
for src, page in used:
    d = os.path.dirname(src)
    folders[d].append((src, page))

for f, lst in sorted(folders.items()):
    print(f"Pasta: {f} ({len(lst)} refs)")
    pages = set(p for _, p in lst)
    print(f"   Exemplo: {lst[0][0]} (usado em {len(pages)} paginas)")
