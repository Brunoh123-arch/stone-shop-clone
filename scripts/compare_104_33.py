import re

with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    p104 = f.read()

with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    p33 = f.read()

print(f"Size p104: {len(p104)} chars | Size p33: {len(p33)} chars")

# Check major DOM sections in 104 vs 33
sections_to_check = [
    'header',
    'image-slider',
    'product-info',
    'product-title',
    'product-price',
    'protecao-cliente',
    'creators-section',
    'reviews-section',
    'seller-profile-card',
    'product-description',
    'product-details',
    'bottom-bar',
    'sku-modal',
    'size-guide-modal'
]

print("\n--- PRESENCE OF MAJOR SECTIONS ---")
for sec in sections_to_check:
    in_104 = sec in p104
    in_33 = sec in p33
    status = "OK" if in_104 == in_33 else f"MISMATCH (104: {in_104}, 33: {in_33})"
    print(f"[{status}] {sec}")

# Check review structure
reviews_104 = len(re.findall(r'class="review-card"', p104))
reviews_33 = len(re.findall(r'class="review-card"', p33))
print(f"\nReview cards count: P104={reviews_104}, P33={reviews_33}")

# Check unboxing photos count
unboxing_104 = len(re.findall(r'class="review-photo"', p104))
unboxing_33 = len(re.findall(r'class="review-photo"', p33))
print(f"Review photos count: P104={unboxing_104}, P33={unboxing_33}")

# Check creators count badge or title in 104 vs 33
creators_104_badge = re.findall(r'Vídeos de criadores \((.*?)\)', p104)
creators_33_badge = re.findall(r'Vídeos de criadores \((.*?)\)', p33)
print(f"Creators badge in HTML: P104={creators_104_badge}, P33={creators_33_badge}")
