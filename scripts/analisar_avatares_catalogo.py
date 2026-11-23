import glob
import re
from collections import Counter

avatars = Counter()
files_per_avatar = {}

for f in glob.glob('pages/*.html'):
    with open(f, 'r', encoding='utf-8') as fp:
        html = fp.read()
    # Encontrar todas as tags img com classe review-avatar ou dentro de .review-avatar
    found = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*review-avatar', html)
    found += re.findall(r'<div class=["\']review-avatar["\']><img[^>]+src=["\']([^"\']+)["\']', html)
    found += re.findall(r'class=["\']review-avatar["\'][^>]*>\s*<img[^>]+src=["\']([^"\']+)["\']', html)
    for a in set(found):
        clean = a.split('?')[0]
        avatars[clean] += 1
        if clean not in files_per_avatar:
            files_per_avatar[clean] = []
        files_per_avatar[clean].append(f)

print(f"Total de arquivos analisados: {len(glob.glob('pages/*.html'))}")
print(f"Total de avatares distintos encontrados: {len(avatars)}")
print("\nTop 30 avatares mais repetidos entre páginas:")
for a, c in avatars.most_common(30):
    print(f"  {c:3d} páginas usam: {a}")
