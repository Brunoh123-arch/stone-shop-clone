with open('templates/produto-canonical-template.html', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    s = l.strip()
    if s.startswith('<!--') or s.startswith('<header') or '<div class="image-slider"' in s or '<div class="price-section"' in s or '<div class="product-info"' in s or '<div class="about-product-section"' in s or '<div class="bottom-bar"' in s or '<div class="creators-section"' in s or '<div class="reviews-section"' in s or '<div class="product-details-block"' in s or '<div class="product-video-block"' in s:
        print(f"Line {i+1}: {s[:90]}")
