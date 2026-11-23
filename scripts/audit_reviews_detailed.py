import re

ids = [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 68, 70, 72, 73, 74, 75, 76]

competitors_pattern = re.compile(r'\b(shopee|shope|aliexpress|ali express|magalu|magazine luiza|amazon|mercado livre|mercadolivre)\b', re.I)

for pid in ids:
    filepath = f"pages/produto-{pid}.html"
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    title_m = re.search(r'<title>(.*?)</title>', html, re.I)
    title = title_m.group(1).strip() if title_m else 'Sem Titulo'

    # Get review comments
    rev_cards = re.findall(r'<div class="review-card".*?</div>\s*</div>', html, re.DOTALL)
    
    flagged_comments = []
    for idx, card in enumerate(rev_cards):
        # find comment
        m_comm = re.search(r'data-author-comment=["\'](.*?)["\']', card)
        comment = m_comm.group(1) if m_comm else ''
        if not comment:
            p_comm = re.search(r'<p class="review-comment">(.*?)</p>', card)
            comment = p_comm.group(1) if p_comm else ''
            
        m_comp = competitors_pattern.findall(comment)
        if m_comp:
            flagged_comments.append((idx+1, comment, set(m_comp)))

    # Get unboxing photos
    photos = re.findall(r'<img[^>]+class=["\'][^"\']*review-photo[^"\']*["\'][^>]*src=["\']([^"\']+)["\']', html)
    if not photos:
        photos = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*review-photo[^"\']*["\']', html)

    print(f"P{pid} ({title[:30]}): {len(rev_cards)} reviews, {len(photos)} photos")
    if photos:
        print(f"   Photos: {photos[:6]}")
    if flagged_comments:
        for idx, comm, comp in flagged_comments:
            print(f"   [CONCORRENTE Card {idx}] ({comp}): \"{comm}\"")
