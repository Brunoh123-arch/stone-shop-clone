import os
import glob
import re
from collections import Counter

def fix_page_duplicate_reviews(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the reviews section
    # We want to deduplicate images inside review cards.
    # A review card is <div class="review-card" ... > ... </div>
    # In some pages, duplicate review cards were appended or duplicate photos were put inside cards.
    
    # Let's split by <div class="review-card"
    splits = html.split('<div class="review-card"')
    if len(splits) <= 1:
        # maybe class='review-card'
        splits = re.split(r'<div[^>]*class=["\'][^"\']*review-card[^"\']*["\']', html)
        if len(splits) <= 1:
            return 0

    prefix = splits[0]
    raw_cards = splits[1:]

    seen_images = set()
    new_cards = []
    removed_count = 0

    for raw_card in raw_cards:
        card_content = '<div class="review-card"' + raw_card
        
        # Find all unboxing/review images in this card (exclude avatars, stars, logos, icons)
        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', card_content)
        cleaned_card = card_content
        card_has_visible_content = True

        for img_src in imgs:
            src_lower = img_src.lower()
            if any(k in src_lower for k in ['avatar', 'star', 'estrela', 'icon', 'logo', 'badge', 'check', 'arrow', 'bandeira']):
                continue
            
            if img_src in seen_images:
                # Duplicate! Remove this img tag
                # Pattern to remove the specific img tag
                pattern = rf'<img[^>]+src=["\']{re.escape(img_src)}["\'][^>]*\/?>'
                cleaned_card = re.sub(pattern, '', cleaned_card)
                removed_count += 1
            else:
                seen_images.add(img_src)
        
        # Also clean empty review-photos containers: <div class="review-photos">\s*</div>
        cleaned_card = re.sub(r'<div[^>]*class=["\'][^"\']*review-photos[^"\']*["\'][^>]*>\s*</div>', '', cleaned_card)

        # Remove the leading '<div class="review-card"' that we prefixed
        if cleaned_card.startswith('<div class="review-card"'):
            cleaned_card = cleaned_card[len('<div class="review-card"'):]
        new_cards.append(cleaned_card)

    if removed_count > 0:
        new_html = prefix + '<div class="review-card"' + '<div class="review-card"'.join(new_cards)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"[*] {file_path}: Removed {removed_count} duplicate review photos.")
        return removed_count

    return 0

pages = sorted(glob.glob('pages/produto-*.html'), key=lambda p: int(re.search(r'produto-(\d+)\.html', p).group(1)))
total_removed = 0
fixed_files = 0

for p in pages:
    cnt = fix_page_duplicate_reviews(p)
    if cnt > 0:
        total_removed += cnt
        fixed_files += 1

print(f"\n[SUMMARY] Fixed {fixed_files} pages, removed {total_removed} duplicate review image instances.")
