import glob, os, re

html_files = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'\d+', x).group()))

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    idx_content = f.read()

index_ids = set(int(x) for x in re.findall(r'produto-(\d+)\.html', idx_content))

not_in_index = []
for h in html_files:
    num = int(re.search(r'\d+', os.path.basename(h)).group())
    if num not in index_ids:
        with open(h, 'r', encoding='utf-8', errors='ignore') as fp:
            m = re.search(r'<title>([^<]+)</title>', fp.read())
            t = m.group(1).strip() if m else 'N/A'
            t = re.sub(r'\s*-\s*Stone\s*Shop.*$', '', t, flags=re.I)
        not_in_index.append((num, t))

print(f"Total produtos com HTML que NAO estao no index.html: {len(not_in_index)}")
for num, title in not_in_index:
    print(f"  P#{num:03d} -> {title}")
