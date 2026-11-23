import re

prods_with_catalog = [21, 74, 99]

for pid in prods_with_catalog:
    filepath = f'pages/produto-{pid}.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remove review-image blocks that contain the catalog mockup images
    # e.g., review-21-c3-1.jpg, review-74-real-*.jpg, review-99-real-*.jpg
    cleaned = re.sub(r'<div class="review-image[^"]*">\s*<img[^>]+(?:review-21-c3-1|review-74-real|review-99-real)[^>]+>\s*</div>', '', html)
    
    if cleaned != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f'Removed catalog images from review cards in P{pid}')
    else:
        print(f'No direct match in P{pid}')
