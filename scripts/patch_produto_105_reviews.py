import re

html_path = 'pages/produto-105.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update top rating count to (4)
content = re.sub(
    r'(<span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document\.querySelector\(\'\.reviews-section\'\)\?\.scrollIntoView\(\{behavior:\'smooth\'\}\)">)\(\d+\)(</span>)',
    r'\g<1>(4)\g<2>',
    content
)

# 2. Update reviews-header to (4)
content = re.sub(
    r'<h3 class="reviews-header">Avaliações dos clientes \(\d+\)</h3>',
    r'<h3 class="reviews-header">Avaliações dos clientes (4)</h3>',
    content
)

star_svg = '<svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
five_stars = star_svg * 5

revs_105 = [
    {
        "name": "M**s S**a",
        "avatar": "../img/reviews-avatars/review-user-105-c1.jpg?v=3",
        "date": "13/08",
        "variation": "PADRÃO, BIVOLT",
        "comment": "Muito boa qualidade Clareza da lente: Muito bom Qualidade do trabalho: Muito bom",
        "photos": ["../img/review-105-c1-1.jpg?v=3", "../img/review-105-c1-2.jpg?v=3"]
    },
    {
        "name": "u**3",
        "avatar": "../img/reviews-avatars/review-user-105-c2.jpg?v=3",
        "date": "11/08",
        "variation": "PADRÃO, BIVOLT",
        "comment": "Gosteiii, comprem. Ele conecta rápido na internet e o som é okk. Ameiii",
        "photos": ["../img/review-105-c2-1.jpg?v=3", "../img/review-105-c2-2.jpg?v=3"]
    },
    {
        "name": "J**a S**🌈",
        "avatar": "../img/reviews-avatars/review-user-105-c3.jpg?v=3",
        "date": "05/08",
        "variation": "PADRÃO, BIVOLT",
        "comment": "Perfeito muito boa mesmo Qualidade do trabalho: Muito boa a qualidade muito fácil de mexer bem manual junto com a caixa chegou rápido a imagem é muito boa eu super recompraria e fiquei muito satisfeito com minha compra compensa muito",
        "photos": ["../img/review-105-c3-1.jpg?v=3", "../img/review-105-c3-2.jpg?v=3"]
    },
    {
        "name": "R**l C**a",
        "avatar": "../img/reviews-avatars/review-user-105-c4.jpg?v=3",
        "date": "08/06",
        "variation": "PADRÃO, BIVOLT",
        "comment": "Produto bom e espero q satisfaça minhas expectativas mas aparentemente e de boa qualidade e a entrega foi muito rápida, obrigada ao vendedor e a tik Tok. Clareza da lente: Sim top",
        "photos": ["../img/review-105-c4-1.jpg?v=3", "../img/review-105-c4-2.jpg?v=3"]
    }
]

cards_html = []
for idx, r in enumerate(revs_105):
    photos_html = "\n".join([
        f'            <img loading="lazy" decoding="async" class="review-photo" src="{p}" alt="Foto do cliente TikTok Shop" onclick="openPhotoModal(this.src)">'
        for p in r['photos']
    ])
    card = f"""        <!-- Avaliação {idx+1} Oficial TikTok Shop: {r['name']} ({r['variation']}) com {len(r['photos'])} fotos reais -->
        <div class="review-card" data-author-name="{r['name']}" data-author-avatar="{r['avatar']}" data-author-stars="5" data-author-variation="{r['variation']}" data-author-date="{r['date']}" data-author-comment="{r['comment']}">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="{r['avatar']}" alt="{r['name']}">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">{r['name']}</div>
                <div class="review-user-stars">{five_stars}</div>
                <div class="review-date">{r['date']} · {r['variation']}</div>
              </div>
            </div>
          </div>
          <p class="review-comment">{r['comment']}</p>
          <div class="review-photos">
{photos_html}
          </div>
        </div>"""
    cards_html.append(card)

all_cards_str = "\n\n".join(cards_html)

# Pattern: replace everything inside reviews-section between reviews-summary and the closing </div> of reviews-section
pattern = r'(<div class="reviews-summary">[\s\S]*?</div>\s*)([\s\S]*?)(\s*</div>\s*(?:<!--.*?-->\s*)?<div class="description-section")'

m = re.search(pattern, content)
if not m:
    # try alternative pattern
    pattern2 = r'(<div class="reviews-summary">[\s\S]*?</div>\s*)([\s\S]*?)(\s*</div>\s*(?:<!--.*?-->\s*)?<div class="about-product-section")'
    m = re.search(pattern2, content)

if m:
    new_content = content[:m.start(2)] + "\n" + all_cards_str + "\n      " + content[m.end(2):]
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: produto-105.html updated with 4 authentic reviews and 8 real photos!")
else:
    print("ERROR: could not find reviews replacement pattern in produto-105.html")
