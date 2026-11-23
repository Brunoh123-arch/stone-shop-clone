import re, os

urls = set()
for s in ['scripts/baixar_avatares_tiktok.py', 'scripts/baixar_avatares_tiktok_2.py', 'scripts/baixar_avatares_tiktok_3.py']:
    if os.path.exists(s):
        with open(s, 'r', encoding='utf-8') as f:
            found = re.findall(r'(https://p\d+-[^"\s]+)', f.read())
            urls.update(found)

urls = sorted(urls)
print(f"Total de URLs: {len(urls)}")
for idx in [64, 67, 69, 72, 75, 77]:
    if idx < len(urls):
        print(f"Index {idx+1} (tt_avatar_{idx+1}): {urls[idx][:80]}")
