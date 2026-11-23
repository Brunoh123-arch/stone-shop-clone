import glob, re, os

# Identificar todos os produtos femininos do catalogo
female_keywords = ['vestido', 'calça mom', 'alfaiataria', 'body modelador', 'cinta', 'chinelo feminino', 'sandália', 'lattafa yara', 'secador', 'prancha', 'escova secadora', 'modelador de cachos', 'mochila rebecca']

# Mapear produtos
pages = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'\d+', x).group()))

female_pages = []
for p in pages:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
        title = re.search(r'<title>([^<]+)</title>', c)
        t_text = title.group(1).lower() if title else ''
        if any(k in t_text for k in ['chinelo', 'sandália', 'vestido', 'calça mom', 'alfaiataria', 'body', 'cinta', 'yara', 'prancha', 'escova secadora', 'modelador de cachos', 'rebecca bonbon']):
            female_pages.append((p, t_text))

print(f"Total produtos femininos identificados: {len(female_pages)}")
for p, t in female_pages:
    print(f"  {p}: {t[:60]}")
