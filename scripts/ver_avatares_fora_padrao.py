import re

for pid in [118, 119, 120, 121, 122, 123]:
    f = f'pages/produto-{pid}.html'
    c = open(f, encoding='utf-8').read()
    cards = re.findall(r'<div class=["\']review-card["\'][^>]*>', c)
    print(f'=== P{pid} ({len(cards)} cards) ===')
    for card in cards:
        m_name = re.search(r'data-author-name=["\']([^"\']+)["\']', card)
        m_av = re.search(r'data-author-avatar=["\']([^"\']+)["\']', card)
        name = m_name.group(1) if m_name else '?'
        av = m_av.group(1) if m_av else '?'
        if 'tiktok_real/tt_avatar_' not in av and 'mulheres_validadas' not in av:
            print(f'  Nome: {name} -> Avatar: {av}')
