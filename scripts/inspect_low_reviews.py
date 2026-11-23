import re

pids = [14, 114, 118, 119, 120, 121, 122, 123]
for pid in pids:
    txt = open(f'pages/produto-{pid}.html', encoding='utf-8').read()
    m_name = re.search(r'nome:\s*["\']([^"\']+)["\']', txt)
    name = m_name.group(1) if m_name else 'N/A'
    reviews = re.findall(r'class="review-card\b', txt)
    photos = re.findall(r'<img[^>]+class=["\'][^"\']*review-img[^"\']*["\']', txt)
    variations = re.findall(r'data-author-variation="([^"]*)"', txt)
    print(f"P{pid}: {name[:60]} | Reviews: {len(reviews)} | Photos: {len(photos)} | Sample Vars: {list(set(variations))[:3]}")
