import re, os

targets_meta = {
    100: {"name": "L**a M.", "avatar": "../img/reviews-avatars/unique/w_7.jpg", "date": "15/10"},
    101: {"name": "R**o S.", "avatar": "../img/reviews-avatars/unique/m_3.jpg", "date": "12/10"},
    102: {"name": "F**e C.", "avatar": "../img/reviews-avatars/unique/m_4.jpg", "date": "14/10"},
    103: {"name": "C**a R.", "avatar": "../img/reviews-avatars/unique/w_8.jpg", "date": "16/10"},
    107: {"name": "M**s P.", "avatar": "../img/reviews-avatars/unique/m_5.jpg", "date": "11/10"},
    108: {"name": "B**z A.", "avatar": "../img/reviews-avatars/unique/w_9.jpg", "date": "13/10"},
    109: {"name": "J**a N.", "avatar": "../img/reviews-avatars/unique/w_10.jpg", "date": "17/10"},
    110: {"name": "T**o M.", "avatar": "../img/reviews-avatars/unique/m_6.jpg", "date": "19/10"},
    111: {"name": "P**a S.", "avatar": "../img/reviews-avatars/unique/w_11.jpg", "date": "15/10"},
    112: {"name": "M**a C.", "avatar": "../img/reviews-avatars/unique/w_12.jpg", "date": "18/10"},
    114: {"name": "A**x S.", "avatar": "../img/reviews-avatars/unique/m_7.jpg", "date": "10/10"},
    14:  {"name": "R**e G.", "avatar": "../img/reviews-avatars/unique/m_8.jpg", "date": "08/10"},
    21:  {"name": "D**o L.", "avatar": "../img/reviews-avatars/unique/m_9.jpg", "date": "14/10"},
    74:  {"name": "J**o P.", "avatar": "../img/reviews-avatars/unique/m_10.jpg", "date": "16/10"},
    96:  {"name": "E**r M.", "avatar": "../img/reviews-avatars/unique/m_11.jpg", "date": "20/10"},
    97:  {"name": "L**a B.", "avatar": "../img/reviews-avatars/unique/w_13.jpg", "date": "14/10"},
}

# 1. Process the 16 regular targets
for pid, meta in targets_meta.items():
    fn = f'pages/produto-{pid}.html'
    with open(fn, 'r', encoding='utf-8') as f:
        c = f.read()
    
    idx_summary = c.find('reviews-summary')
    if idx_summary == -1:
        print(f"ERROR: reviews-summary not found in P{pid}")
        continue
    
    m_summary = re.search(r'(<div class="reviews-summary"[^>]*>[\s\S]*?</div>\s*</div>)', c[idx_summary-20:])
    if not m_summary:
        # Try finding double </div>
        m_summary = re.search(r'(<div class="reviews-summary"[^>]*>[\s\S]*?</div>[\s\S]*?</div>)', c[idx_summary-20:])
    end_summary = idx_summary - 20 + m_summary.end()
    
    idx_comment = c.find('<p class="review-comment">', end_summary)
    if idx_comment == -1:
        idx_comment = c.find('<p class="review-text review-comment">', end_summary)
        
    if idx_comment == -1:
        print(f"ERROR: review-comment not found after summary in P{pid}")
        continue
        
    clean_header = f"""

        <div class="review-card" data-author-name="{meta['name']}" data-author-avatar="{meta['avatar']}" data-author-stars="5" data-author-date="{meta['date']}">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="{meta['avatar']}" alt="{meta['name']}">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">{meta['name']}</div>
                <div class="review-user-stars">
                  <svg fill="#ffb800" height="12" viewBox="0 0 24 24" width="12"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                  <svg fill="#ffb800" height="12" viewBox="0 0 24 24" width="12"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                  <svg fill="#ffb800" height="12" viewBox="0 0 24 24" width="12"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                  <svg fill="#ffb800" height="12" viewBox="0 0 24 24" width="12"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                  <svg fill="#ffb800" height="12" viewBox="0 0 24 24" width="12"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                </div>
                <div class="review-date">{meta['date']}</div>
              </div>
            </div>
          </div>
          """
    
    new_c = c[:end_summary] + clean_header + c[idx_comment:]
    
    opens = len(re.findall(r'<div[\s>]', new_c))
    closes = len(re.findall(r'</div>', new_c))
    diff = opens - closes
    
    has_contam = any(p in new_c for p in ['Smart TV completa', 'Custo-benefício imbatível. Perfeita', 'Controle muito prático'])
    print(f"P{pid}: diff={diff} | contam={has_contam}")
    
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(new_c)

# 2. Process P124
fn124 = 'pages/produto-124.html'
with open(fn124, 'r', encoding='utf-8') as f:
    c = f.read()

idx_summary = c.find('reviews-summary')
m_summary = re.search(r'(<div class="reviews-summary"[^>]*>[\s\S]*?</div>\s*</div>)', c[idx_summary-20:])
end_summary = idx_summary - 20 + m_summary.end()

idx_about = c.find('<!-- SEÇÃO OFICIAL: SOBRE ESTE PRODUTO -->')
if idx_about == -1:
    idx_about = c.find('class="about-product-section"')

star_svg = '<svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
five_stars = star_svg * 5

p124_reviews = f"""
        <!-- AVALIAÇÃO 1 -->
        <div class="review-card" data-author-name="M**a S." data-author-avatar="../img/reviews-avatars/unique/w_6.jpg" data-author-stars="5" data-author-date="18/10" data-author-variation="Azul">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/unique/w_6.jpg" alt="M**a S.">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">M**a S.</div>
                <div class="review-user-stars">{five_stars}</div>
                <div class="review-date">18/10 · Azul</div>
              </div>
            </div>
          </div>
          <p class="review-text review-comment">Entrega muito rápida, chegou em 3 dias bem embalado. Funciona perfeitamente com 3 pilhas palito, os botões têm ótima sensibilidade. Recomendo demais!</p>
          <div class="review-photos">
            <img src="../img/reviews/review-124-4.webp?v=1794726000" alt="Foto real de cliente do Livro Interativo Bilíngue Azul" class="review-photo" loading="lazy" onclick="openPhotoModal(this.src)">
            <img src="../img/reviews/review-124-1.webp?v=1794726000" alt="Foto real de cliente do Livro Interativo Bilíngue Amarelo" class="review-photo" loading="lazy" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- AVALIAÇÃO 2 -->
        <div class="review-card" data-author-name="C**a F." data-author-avatar="../img/reviews-avatars/unique/w_14.jpg" data-author-stars="5" data-author-date="12/10" data-author-variation="Amarelo">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/unique/w_14.jpg" alt="C**a F.">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">C**a F.</div>
                <div class="review-user-stars">{five_stars}</div>
                <div class="review-date">12/10 · Amarelo</div>
              </div>
            </div>
          </div>
          <p class="review-text review-comment">Meu filho amou! As músicas em inglês e português ajudam muito na fala e no aprendizado. Muito interativo e educativo.</p>
          <div class="review-photos">
            <img src="../img/reviews/review-124-2.webp" alt="Foto real cliente Livro Interativo" class="review-photo" loading="lazy" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- AVALIAÇÃO 3 -->
        <div class="review-card" data-author-name="R**o P." data-author-avatar="../img/reviews-avatars/unique/m_12.jpg" data-author-stars="5" data-author-date="05/10" data-author-variation="Azul">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/unique/m_12.jpg" alt="R**o P.">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">R**o P.</div>
                <div class="review-user-stars">{five_stars}</div>
                <div class="review-date">05/10 · Azul</div>
              </div>
            </div>
          </div>
          <p class="review-text review-comment">Excelente qualidade! O som sai bem nítido e a caneta interativa responde super rápido. Vale muito a pena, excelente presente.</p>
          <div class="review-photos">
            <img src="../img/reviews/review-124-3.webp" alt="Foto real cliente Livro Interativo" class="review-photo" loading="lazy" onclick="openPhotoModal(this.src)">
          </div>
        </div>
      </div>

      """

new_c = c[:end_summary] + p124_reviews + c[idx_about:]
opens = len(re.findall(r'<div[\s>]', new_c))
closes = len(re.findall(r'</div>', new_c))
diff = opens - closes
has_contam = 'Custo-benefício imbatível' in new_c
print(f"P124: diff={diff} | contam={has_contam}")

with open(fn124, 'w', encoding='utf-8') as f:
    f.write(new_c)

print("\nAll 17 contaminated products processed!")
