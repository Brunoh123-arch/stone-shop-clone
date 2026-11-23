import json
import re
import os
import subprocess

def apply_piscina_13():
    urls_file = 'scripts/piscina_32_catbox_urls.json'
    if not os.path.exists(urls_file):
        print(f"Error: {urls_file} not found.")
        return False
        
    uploaded = json.load(open(urls_file, encoding='utf-8'))
    print(f"Loaded {len(uploaded)} pool videos from {urls_file}")
    
    avatar_pool = [
        "../img/reviews-avatars/review-user-104-vanessa.jpg",
        "../img/reviews-avatars/review-user-104-juliana.jpg",
        "../img/reviews-avatars/review-user-104-renata.jpg",
        "../img/reviews-avatars/review-user-104-c4.jpg",
        "../img/reviews-avatars/review-user-1.jpg",
        "../img/reviews-avatars/review-user-2.jpg",
        "../img/reviews-avatars/review-user-3.jpg",
        "../img/reviews-avatars/review-user-4.jpg",
        "../img/reviews-avatars/review-user-5.jpg",
        "../img/reviews-avatars/review-user-6.jpg",
        "../img/reviews-avatars/review-user-7.jpg",
        "../img/reviews-avatars/review-user-8.jpg",
        "../img/reviews-avatars/review-user-9.jpg",
        "../img/reviews-avatars/review-user-10.jpg",
        "../img/reviews-avatars/review-user-11.jpg",
        "../img/reviews-avatars/review-user-12.jpg"
    ]
    
    # 1. Montar array de 32 criadores
    creators_list = []
    keys = sorted(uploaded.keys())
    
    likes_seed = [18400, 24100, 15300, 9800, 31200, 12400, 28500, 42100, 19600, 14700, 22300, 17800, 35400, 26900, 18900, 13200, 29100, 16400, 38700, 21500, 27300, 33800, 19100, 14800, 25600, 18200, 22900, 31400, 20700, 16900, 28400, 45200]
    
    for i, k in enumerate(keys[:32]):
        item = uploaded[k]
        cat_url = item.get('catbox')
        title = item.get('title', 'Piscina Inflável 1000L Pixlar Lazer')
        channel = item.get('channel', f'Criador {i+1}')
        poster = item.get('poster', f'../img/posters-piscina/poster-piscina-{i+1:02d}.jpg')
        avatar = avatar_pool[i % len(avatar_pool)]
        
        # Clean channel name to handle
        username = re.sub(r'[^a-zA-Z0-9_.]', '', channel.lower().replace(' ', '.'))[:18]
        if not username:
            username = f"criador.piscina.{i+1}"
            
        c_obj = {
            "name": channel[:22],
            "username": username,
            "avatar": avatar,
            "poster": poster,
            "video": cat_url,
            "localVideo": f"../videosprodutos/piscina_32/{k}.mp4",
            "startTime": 0.2,
            "likes": likes_seed[i % len(likes_seed)],
            "comments": 45 + (i * 7) % 300,
            "shares": 120 + (i * 15) % 600,
            "saves": 350 + (i * 25) % 1500,
            "title": f"{title} 💦☀️ Perfeita pro calor no quintal de casa! #piscina #verao #lazer #mor #pixlar"
        }
        creators_list.append(c_obj)
        
    print(f"Generated {len(creators_list)} creator objects for js/videos-criadores.js")
    
    # 2. Atualizar js/videos-criadores.js
    with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
        
    pattern = r"const CREATORS_PISCINA_PIXLAR_13\s*=\s*\[[\s\S]*?\];"
    new_js_decl = f"const CREATORS_PISCINA_PIXLAR_13 = {json.dumps(creators_list, ensure_ascii=False, indent=2)};"
    
    if not re.search(pattern, js_code):
        print("Error: Could not find CREATORS_PISCINA_PIXLAR_13 declaration in js/videos-criadores.js")
        return False
        
    js_code_updated = re.sub(pattern, new_js_decl, js_code, count=1)
    with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
        f.write(js_code_updated)
        
    print("Updated js/videos-criadores.js successfully!")
    
    # 3. Atualizar reviews em pages/produto-13.html
    reviews_data = [
        {"name": "M**a S.", "avatar": "../img/reviews-avatars/review-user-104-vanessa.jpg", "date": "12/10", "var": "Azul 1000L - Borda Inflável", "comment": "A piscina é ótima! O tamanho de 1000 litros é perfeito pro meu quintal que é pequeno. Inflou a borda em 2 minutos e encheu rapidinho com a mangueira."},
        {"name": "C**s E.", "avatar": "../img/reviews-avatars/review-user-104-juliana.jpg", "date": "08/10", "var": "Azul 1000L - Borda Inflável", "comment": "Meus filhos de 3 e 6 anos amaram demais! A borda inflável é super macia, não tem perigo de baterem em ferro duro. Segurança total."},
        {"name": "R**o P.", "avatar": "../img/reviews-avatars/review-user-104-renata.jpg", "date": "04/10", "var": "Azul 1000L - Borda Inflável", "comment": "Material da lona é bem resistente, PVC reforçado de três camadas. Veio com kit reparo caso fure. Excelente custo benefício pro calor!"},
        {"name": "A**a O.", "avatar": "../img/reviews-avatars/review-user-1.jpg", "date": "28/09", "var": "Azul 1000L - Borda Inflável", "comment": "Chegou antes do prazo e muito bem embalada pela Stone Shop. Fácil de montar e esvaziar pela válvula no fundo. Recomendo!"},
        {"name": "F**e B.", "avatar": "../img/reviews-avatars/review-user-2.jpg", "date": "25/09", "var": "Azul 1000L - Borda Inflável", "comment": "Muito prática! Quando termina o fim de semana é só desinflar a borda que seca rápido e dobra pequenininha pra guardar na caixa."},
        {"name": "J**a L.", "avatar": "../img/reviews-avatars/review-user-3.jpg", "date": "19/09", "var": "Azul 1000L - Borda Inflável", "comment": "Melhor aquisição pro verão da criançada. Cabe duas crianças e dois adultos sentados tranquilamente curtindo uma água gelada."},
        {"name": "T**o M.", "avatar": "../img/reviews-avatars/review-user-4.jpg", "date": "15/09", "var": "Azul 1000L - Borda Inflável", "comment": "A lona é grossa e resistente. Coloquei uma lona embaixo no chão pra proteger e ficou perfeita. Diversão garantida pra família toda!"},
        {"name": "V**a D.", "avatar": "../img/reviews-avatars/review-user-5.jpg", "date": "10/09", "var": "Azul 1000L - Borda Inflável", "comment": "Super recomendo a loja, envio no mesmo dia e produto 100% original com nota fiscal e garantia. Atendimento nota 10."},
        {"name": "B**z R.", "avatar": "../img/reviews-avatars/review-user-6.jpg", "date": "05/09", "var": "Azul 1000L - Borda Inflável", "comment": "Piscina maravilhosa! Cor azul brilhante muito bonita e tamanho ideal pra quem tem pouco espaço no quintal ou laje."},
        {"name": "G**l S.", "avatar": "../img/reviews-avatars/review-user-7.jpg", "date": "01/09", "var": "Azul 1000L - Borda Inflável", "comment": "Enche rápido e não gasta tanta água quanto as piscinas gigantes. Dá pra trocar e manter sempre limpinha gastando pouco."},
        {"name": "L**s F.", "avatar": "../img/reviews-avatars/review-user-8.jpg", "date": "28/08", "var": "Azul 1000L - Borda Inflável", "comment": "Comprei na oferta e valeu muito a pena. As crianças não saem de dentro nesse calorão!"},
        {"name": "P**a N.", "avatar": "../img/reviews-avatars/review-user-9.jpg", "date": "24/08", "var": "Azul 1000L - Borda Inflável", "comment": "Excelente qualidade do PVC. A borda segura a água perfeitamente conforme vai enchendo, sem vazar nada."},
        {"name": "D**o R.", "avatar": "../img/reviews-avatars/review-user-10.jpg", "date": "18/08", "var": "Azul 1000L - Borda Inflável", "comment": "Chegou certinho em São Paulo em 3 dias. Montagem nota 10 de tão fácil, só inflar o anel e ligar a mangueira."},
        {"name": "I**a F.", "avatar": "../img/reviews-avatars/review-user-11.jpg", "date": "12/08", "var": "Azul 1000L - Borda Inflável", "comment": "Muito boa! Dá pra curtir um dia de sol relaxando no quintal com os pés na água fresca."},
        {"name": "M**o P.", "avatar": "../img/reviews-avatars/review-user-12.jpg", "date": "05/08", "var": "Azul 1000L - Borda Inflável", "comment": "Perfeita, material reforçado e muito confiável. Valeu cada centavo, nota 5 estrelas!"}
    ]
    
    star_svg = '<svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
    stars_5 = star_svg * 5
    
    review_cards_html = []
    for r in reviews_data:
        card = f'''        <div class="review-card" data-author-name="{r['name']}" data-author-avatar="{r['avatar']}" data-author-stars="5" data-author-variation="{r['var']}" data-author-date="{r['date']}" data-author-comment="{r['comment']}">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="{r['avatar']}" alt="{r['name']}">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">{r['name']}</div>
                <div class="review-user-stars">{stars_5}</div>
                <div class="review-date">{r['date']} · {r['var']}</div>
              </div>
            </div>
          </div>
          <p class="review-comment">{r['comment']}</p>
        </div>'''
        review_cards_html.append(card)
        
    all_reviews_joined = "\n".join(review_cards_html)
    
    with open('pages/produto-13.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    rev_pattern = r'(<div class="reviews-section">[\s\S]*?<div class="reviews-summary">[\s\S]*?</div>\s*</div>)([\s\S]*?)(<button class="view-more-reviews"|<div class="seller-profile-card"|<div class="product-description")'
    
    match = re.search(rev_pattern, html)
    if match:
        prefix = match.group(1)
        suffix = match.group(3)
        html = html[:match.start()] + prefix + "\n\n" + all_reviews_joined + "\n\n      " + suffix + html[match.end():]
        print("Replaced review section in pages/produto-13.html")
    else:
        print("Warning: Could not match exact reviews-section regex, trying fallback")
        card_pattern = r'(<div class="review-card"[\s\S]*?)(?=<button class="view-more-reviews"|<div class="seller-profile-card"|<div class="product-description")'
        html = re.sub(card_pattern, all_reviews_joined + "\n\n      ", html, count=1)
        
    with open('pages/produto-13.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Updated pages/produto-13.html successfully!")
    return True

if __name__ == '__main__':
    apply_piscina_13()
