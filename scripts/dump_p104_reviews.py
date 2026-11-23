import re

with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Dividir por class="review-card"
cards = html.split('class="review-card"')
print(f"Total blocos de review: {len(cards)-1}")

for i, card in enumerate(cards[1:], 1):
    # pegar dados
    m_name = re.search(r'class="review-user-name">([^<]+)<', card)
    m_img = re.search(r'<img[^>]+src="([^"]+)"', card)
    m_comm = re.search(r'class="review-comment">([^<]+)<', card)
    m_var = re.search(r'class="review-variation">([^<]+)<', card)
    m_date = re.search(r'class="review-date">([^<]+)<', card)
    
    name = m_name.group(1).strip() if m_name else 'SEM NOME'
    img = m_img.group(1).strip() if m_img else 'SEM IMG'
    comm = m_comm.group(1).strip() if m_comm else 'SEM COMENT'
    var = m_var.group(1).strip() if m_var else 'SEM VAR'
    date = m_date.group(1).strip() if m_date else 'SEM DATA'
    
    print(f"#{i:02d} | Nome: {name:<12} | Var: {var:<15} | Data: {date} | Img: {img}")
    print(f"     Coment: {comm[:80]}")
    print("-" * 70)
