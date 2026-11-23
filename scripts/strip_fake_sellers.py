import re
import glob

files = glob.glob('pages/produto-*.html')
stripped_count = 0

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'seller-profile-card' in content:
        print(f"Stripping fake seller-profile-card from {file_path}")
        # Remove the comment and the seller-profile-card div
        cleaned = re.sub(
            r'<!--\s*CARD DA LOJA MULTI-SELLER OFICIAL TIKTOK SHOP\s*-->\s*<div class="seller-profile-card".*?</div>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        # In case the comment is different
        cleaned = re.sub(
            r'<div class="seller-profile-card".*?</div>\s*',
            '',
            cleaned,
            flags=re.DOTALL
        )
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        stripped_count += 1

print(f"Successfully stripped seller-profile-card from {stripped_count} files!")
