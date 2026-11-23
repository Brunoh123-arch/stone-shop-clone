import os

res = []
for root, dirs, files in os.walk('videosprodutos'):
    for f in files:
        fp = os.path.join(root, f)
        sz = os.path.getsize(fp)
        res.append((fp, sz))

res.sort(key=lambda x: x[0])
print(f'Total files in videosprodutos: {len(res)}')
for fp, sz in res[:40]:
    print(f'{fp}: {sz / 1024:.1f} KB')
