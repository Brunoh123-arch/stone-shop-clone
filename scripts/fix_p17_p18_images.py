import os, glob

# Rename shopee-asset-17 and 18 to stone-asset-17 and 18
for f in glob.glob('img/shopee-asset-17-*.jpg'):
    new_name = f.replace('shopee-asset-17-', 'stone-asset-17-')
    os.rename(f, new_name)
    print(f"Renamed {f} -> {new_name}")

for f in glob.glob('img/shopee-asset-18-*.jpg'):
    new_name = f.replace('shopee-asset-18-', 'stone-asset-18-')
    os.rename(f, new_name)
    print(f"Renamed {f} -> {new_name}")

# Now update pages/produto-17.html and pages/produto-18.html
with open('pages/produto-17.html', 'r', encoding='utf-8') as f:
    c17 = f.read()

c17_new = c17.replace('Stone Shop-asset-17-', 'stone-asset-17-').replace('shopee-asset-17-', 'stone-asset-17-')
with open('pages/produto-17.html', 'w', encoding='utf-8') as f:
    f.write(c17_new)
print('pages/produto-17.html atualizado!')

with open('pages/produto-18.html', 'r', encoding='utf-8') as f:
    c18 = f.read()

c18_new = c18.replace('Stone Shop-asset-18-', 'stone-asset-18-').replace('shopee-asset-18-', 'stone-asset-18-')
with open('pages/produto-18.html', 'w', encoding='utf-8') as f:
    f.write(c18_new)
print('pages/produto-18.html atualizado!')
