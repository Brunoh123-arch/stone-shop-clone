import re

ids = [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 68, 70, 72, 73, 74, 75, 76]

# Words that indicate mismatch
# We can print the first 3 reviews of each product and check them
for pid in ids:
    filepath = f"pages/produto-{pid}.html"
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    title_m = re.search(r'<title>(.*?)</title>', html, re.I)
    title = title_m.group(1).strip() if title_m else 'Sem Titulo'

    rev_cards = re.findall(r'<div class="review-card".*?</div>\s*</div>', html, re.DOTALL)
    print(f"\n==========================================")
    print(f"P{pid} ({title[:50]}) - {len(rev_cards)} reviews")
    print(f"==========================================")
    for idx, card in enumerate(rev_cards[:4]):
        m_comm = re.search(r'data-author-comment=["\'](.*?)["\']', card)
        comment = m_comm.group(1) if m_comm else ''
        if not comment:
            p_comm = re.search(r'<p class="review-comment">(.*?)</p>', card)
            comment = p_comm.group(1) if p_comm else ''
            
        m_var = re.search(r'<div class="review-date">(.*?)</div>', card)
        var = m_var.group(1) if m_var else ''
        
        photos = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*review-photo[^"\']*["\']', card)
        if not photos:
            photos = re.findall(r'<img[^>]+class=["\'][^"\']*review-photo[^"\']*["\'][^>]*src=["\']([^"\']+)["\']', card)
            
        print(f"  [R{idx+1}] ({var}): \"{comment[:90]}...\" | Photos: {photos}")
