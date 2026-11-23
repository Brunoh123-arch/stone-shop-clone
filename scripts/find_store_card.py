import glob, re

for f in glob.glob('pages/*.html'):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        c = fh.read()
    if 'sobre esta loja' in c.lower() or 'sobre a loja' in c.lower() or 'seller-profile-card' in c.lower() or 'mais desta loja' in c.lower():
        print("Store card found in:", f)
        # print snippet
        idx = c.lower().find('sobre esta loja')
        if idx == -1:
            idx = c.lower().find('mais desta loja')
        if idx == -1:
            idx = c.lower().find('seller-profile-card')
        if idx != -1:
            print("  -> Snippet:", c[idx-20:idx+250].replace('\n', ' '))
