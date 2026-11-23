import re

reviews_data = [
    {"name": "M**a S.", "avatar": "../img/reviews-avatars/review-user-1.jpg", "date": "12/10", "var": "Azul 1000L - Borda Inflável", "comment": "A piscina é ótima! O tamanho de 1000 litros é perfeito pro meu quintal que é pequeno. Inflou a borda em 2 minutos e encheu rapidinho com a mangueira."},
    {"name": "C**s E.", "avatar": "../img/reviews-avatars/review-user-2.jpg", "date": "08/10", "var": "Azul 1000L - Borda Inflável", "comment": "Meus filhos de 3 e 6 anos amaram demais! A borda inflável é super macia, não tem perigo de baterem em ferro duro. Segurança total."},
    {"name": "R**o P.", "avatar": "../img/reviews-avatars/review-user-3.jpg", "date": "04/10", "var": "Azul 1000L - Borda Inflável", "comment": "Material da lona é bem resistente, PVC reforçado de três camadas. Veio com kit reparo caso fure. Excelente custo benefício pro calor!"},
    {"name": "A**a O.", "avatar": "../img/reviews-avatars/review-user-4.jpg", "date": "28/09", "var": "Azul 1000L - Borda Inflável", "comment": "Chegou antes do prazo e muito bem embalada pela Stone Shop. Fácil de montar e esvaziar pela válvula no fundo. Recomendo!"},
    {"name": "F**e B.", "avatar": "../img/reviews-avatars/review-user-5.jpg", "date": "25/09", "var": "Azul 1000L - Borda Inflável", "comment": "Muito prática! Quando termina o fim de semana é só desinflar a borda que seca rápido e dobra pequenininha pra guardar na caixa."},
    {"name": "J**a L.", "avatar": "../img/reviews-avatars/review-user-6.jpg", "date": "19/09", "var": "Azul 1000L - Borda Inflável", "comment": "Melhor aquisição pro verão da criançada. Cabe duas crianças e dois adultos sentados tranquilamente curtindo uma água gelada."},
    {"name": "T**o M.", "avatar": "../img/reviews-avatars/review-user-7.jpg", "date": "15/09", "var": "Azul 1000L - Borda Inflável", "comment": "A lona é grossa e resistente. Coloquei uma lona embaixo no chão pra proteger e ficou perfeita. Diversão garantida pra família toda!"},
    {"name": "V**a D.", "avatar": "../img/reviews-avatars/review-user-8.jpg", "date": "10/09", "var": "Azul 1000L - Borda Inflável", "comment": "Super recomendo a loja, envio no mesmo dia e produto 100% original com nota fiscal e garantia. Atendimento nota 10."},
    {"name": "B**z R.", "avatar": "../img/reviews-avatars/review-user-9.jpg", "date": "05/09", "var": "Azul 1000L - Borda Inflável", "comment": "Piscina maravilhosa! Cor azul brilhante muito bonita e tamanho ideal pra quem tem pouco espaço no quintal ou laje."},
    {"name": "G**l S.", "avatar": "../img/reviews-avatars/review-user-10.jpg", "date": "01/09", "var": "Azul 1000L - Borda Inflável", "comment": "Enche rápido e não gasta tanta água quanto as piscinas gigantes. Dá pra trocar e manter sempre limpinha gastando pouco."},
    {"name": "L**s F.", "avatar": "../img/reviews-avatars/review-user-11.jpg", "date": "28/08", "var": "Azul 1000L - Borda Inflável", "comment": "Comprei na oferta e valeu muito a pena. As crianças não saem de dentro nesse calorão!"},
    {"name": "P**a N.", "avatar": "../img/reviews-avatars/review-user-12.jpg", "date": "24/08", "var": "Azul 1000L - Borda Inflável", "comment": "Excelente qualidade do PVC. A borda segura a água perfeitamente conforme vai enchendo, sem vazar nada."},
    {"name": "D**o R.", "avatar": "../img/reviews-avatars/review-user-1.jpg", "date": "18/08", "var": "Azul 1000L - Borda Inflável", "comment": "Chegou certinho em São Paulo em 3 dias. Montagem nota 10 de tão fácil, só inflar o anel e ligar a mangueira."},
    {"name": "I**a F.", "avatar": "../img/reviews-avatars/review-user-2.jpg", "date": "12/08", "var": "Azul 1000L - Borda Inflável", "comment": "Muito boa! Dá pra curtir um dia de sol relaxando no quintal com os pés na água fresca."},
    {"name": "M**o P.", "avatar": "../img/reviews-avatars/review-user-3.jpg", "date": "05/08", "var": "Azul 1000L - Borda Inflável", "comment": "Perfeita, material reforçado e muito confiável. Valeu cada centavo, nota 5 estrelas!"}
]

star_svg = '<svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
stars_5 = star_svg * 5

cards = []
for r in reviews_data:
    c = f'''      <div class="review-card" data-author-name="{r['name']}" data-author-avatar="{r['avatar']}" data-author-stars="5" data-author-variation="{r['var']}" data-author-date="{r['date']}" data-author-comment="{r['comment']}">
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
    cards.append(c)

cards_html = "\n".join(cards)

new_section = f'''<!-- AVALIAÇÕES DOS CLIENTES OFICIAL TIKTOK SHOP -->
    <section class="reviews-section" style="padding: 16px; background: #ffffff; margin-top: 8px;">
      <div class="reviews-header" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
        <h3 style="font-size: 15px; font-weight: 700; color: #161823; margin: 0;">Avaliações dos clientes (15)</h3>
        <span onclick="window.abrirTelaAvaliacoesCompletas && window.abrirTelaAvaliacoesCompletas()" style="font-size: 12.5px; color: #4364db; font-weight: 500; cursor: pointer;">Ver mais &gt;</span>
      </div>
      <div class="reviews-summary" style="display: flex; align-items: center; gap: 6px; margin-bottom: 14px;">
        <span class="review-avg" style="font-size: 20px; font-weight: 800; color: #161823;">4.9</span>
        <span class="review-avg-total" style="font-size: 13px; color: #73747b;">/5</span>
        <div class="review-stars">{stars_5}</div>
      </div>
      <div class="reviews-list">
{cards_html}
      </div>
    </section>'''

with open('pages/produto-13.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'<section class="reviews-section"[\s\S]*?</section>'
if re.search(pattern, html):
    html = re.sub(pattern, new_section, html, count=1)
    with open('pages/produto-13.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully replaced reviews section in pages/produto-13.html!")
else:
    print("Error: Could not find <section class=\"reviews-section\"> in pages/produto-13.html")
