import os
import re

files_to_clean = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.vercel', 'scripts_archive', 'scratch']):
        continue
    for f in files:
        if f.endswith('.html'):
            files_to_clean.append(os.path.join(root, f))

pattern = re.compile(r'(\s*Compartilhe isso com amigos para ganhar comissões nas compras deles\s*</div>)', re.MULTILINE)
pattern2 = re.compile(r'\s*<!-- TOOLTIP CIANO OFICIAL TIKTOK SHOP -->[\s\S]*?</div>', re.MULTILINE)
pattern3 = re.compile(r'<div id="share-tooltip-bubble"[\s\S]*?</div>', re.MULTILINE)

cleaned_count = 0
for fpath in files_to_clean:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        with open(fpath, 'r', encoding='latin-1') as f:
            content = f.read()
    
    new_content = pattern.sub('', content)
    new_content = pattern2.sub('', new_content)
    new_content = pattern3.sub('', new_content)

    # Também remover quaisquer resquícios do script do tooltip
    new_content = re.sub(r'<script>\s*// Tooltip de Compartilhamento TikTok Shop[\s\S]*?initShareTooltip\(\);\s*\}\);\s*</script>', '', new_content)

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        cleaned_count += 1
        print(f"Purged tooltip residue from {fpath}")

print(f"Total files cleaned: {cleaned_count}")
