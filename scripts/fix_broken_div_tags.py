import re
import glob

files = glob.glob('pages/produto-*.html')
fixed_count = 0

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for the broken pattern
    if '<div --' in content:
        print(f"Fixing broken tag in {file_path}")
        # Replace `<div --="" <!--="" card="" da="" loja="" multi-seller="" oficial="" shop="" tiktok="">` with just a clean comment
        content = re.sub(
            r'<div --=""\s*<!--=""\s*card=""\s*da=""\s*loja=""\s*multi-seller=""\s*oficial=""\s*shop=""\s*tiktok="">',
            r'<!-- CARD DA LOJA MULTI-SELLER OFICIAL TIKTOK SHOP -->',
            content
        )
        # Also clean any matching stray closing </div> before or after </section>
        content = re.sub(
            r'</section>\s*</div><!-- fim about-product-section -->',
            r'</section><!-- fim about-product-section -->',
            content
        )
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1

print(f"Fixed {fixed_count} files.")
