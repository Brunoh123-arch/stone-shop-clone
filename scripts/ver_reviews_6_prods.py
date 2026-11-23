import re

pids = [5, 17, 18, 61, 74, 99]
for pid in pids:
    f = f"pages/produto-{pid}.html"
    c = open(f, encoding='utf-8').read()
    # achar reviews-section
    rev_cards = re.findall(r'<div class=["\']review-card["\'][^>]*>', c)
    print(f"=== P{pid} ({len(rev_cards)} review cards) ===")
    for card in rev_cards[:3]:
        m_name = re.search(r'data-author-name=["\']([^"\']+)["\']', card)
        m_comm = re.search(r'data-author-comment=["\']([^"\']+)["\']', card)
        print("  Name:", m_name.group(1) if m_name else "?")
        print("  Comm:", m_comm.group(1)[:60] if m_comm else "?")
