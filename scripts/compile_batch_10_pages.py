import os
import json
import re
from bs4 import BeautifulSoup

DATA_DIR = 'scripts/data'
PIDS = [9, 10, 11, 13, 14, 15, 17, 18, 21, 22]

def update_videos_criadores_js(all_prod_data):
    with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
        content = f.read()

    for pdata in all_prod_data:
        pid = pdata["id"]
        slug = pdata["slug"]
        const_name = f"CREATORS_{slug}"
        creators_json = json.dumps(pdata["creators"], ensure_ascii=False, indent=2)
        const_def = f"const {const_name} = {creators_json};\n"

        if f"const {const_name} =" in content:
            pattern = re.compile(rf"const {const_name}\s*=\s*\[.*?\];\n", re.DOTALL)
            content = pattern.sub(const_def, content)
            print(f"Substituído {const_name} em js/videos-criadores.js")
        else:
            idx = content.find("const CREATOR_SETS")
            if idx != -1:
                content = content[:idx] + const_def + "\n" + content[idx:]
                print(f"Injetado {const_name} antes de CREATOR_SETS")
            else:
                content += "\n" + const_def

        map_entry = f"{pid}: {const_name},"
        if map_entry not in content:
            m = re.search(r"const CREATOR_SETS\s*=\s*\{", content)
            if m:
                insert_idx = m.end()
                content = content[:insert_idx] + f"\n  {map_entry}" + content[insert_idx:]
                print(f"Mapeado {pid}: {const_name} em CREATOR_SETS")

    with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("js/videos-criadores.js atualizado com sucesso!")

def build_review_card(idx, comment, pid):
    author_names = [
        "mariana_silva", "carlos.eduardo", "lucas_martins", "patricia.alves",
        "fernando_costa", "camila_rocha", "rodrigo.santos", "amanda_oliveira",
        "gabriel_souza", "juliana_lima", "felipe_barreto", "vanessa_dias",
        "thiago_melo", "beatriz_ramos", "ricardo_nogueira"
    ]
    dates = [
        "12 out. 2025 · Padrão", "08 out. 2025 · Padrão", "02 out. 2025 · Padrão",
        "28 set. 2025 · Padrão", "22 set. 2025 · Padrão", "17 set. 2025 · Padrão",
        "11 set. 2025 · Padrão", "05 set. 2025 · Padrão", "30 ago. 2025 · Padrão",
        "24 ago. 2025 · Padrão", "18 ago. 2025 · Padrão", "12 ago. 2025 · Padrão",
        "05 ago. 2025 · Padrão", "29 jul. 2025 · Padrão", "21 jul. 2025 · Padrão"
    ]
    name = author_names[idx % len(author_names)]
    date = dates[idx % len(dates)]
    avatar_id = (idx % 28) + 1

    photo_html = f'''
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/reviews-avatars/review-user-{avatar_id}.jpg" alt="Foto da avaliação" onerror="this.style.display='none'" onclick="openPhotoModal && openPhotoModal(this.src)">
          </div>''' if idx in [1, 2, 4, 6, 8, 10, 13] else ''

    return f'''        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-{avatar_id}.jpg" alt="{name}" onerror="this.outerHTML='<div class=\\'review-avatar-placeholder\\'>'+(this.alt||'U')[0].toUpperCase()+'</div>'">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">{name}</div>
                <div class="review-user-stars">★★★★★</div>
                <div class="review-date">{date}</div>
              </div>
            </div>
          </div>
          <p class="review-comment">{comment}</p>{photo_html}
        </div>'''

def update_product_page(pdata):
    pid = pdata["id"]
    page_path = f"pages/produto-{pid}.html"
    if not os.path.exists(page_path):
        print(f"Página {page_path} não encontrada!")
        return

    with open(page_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Proibição absoluta de tabelas HTML (Regra GEMINI.md)
    if '<table' in html:
        html = re.sub(r'<table.*?>.*?</table>', '', html, flags=re.DOTALL)
        print(f"Removidas tabelas HTML em {page_path}")

    # 2. Constrói novo bloco de reviews limpo
    reviews_cards_html = "\n".join([build_review_card(i, comm, pid) for i, comm in enumerate(pdata["reviews"])])
    
    new_reviews_section = f'''    <!-- AVALIAÇÕES DOS CLIENTES OFICIAL TIKTOK SHOP -->
    <section class="reviews-section" style="padding: 16px; background: #ffffff; margin-top: 8px;">
      <div class="reviews-header" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
        <h3 style="font-size: 15px; font-weight: 700; color: #161823; margin: 0;">Avaliações dos clientes (15)</h3>
        <span style="font-size: 12.5px; color: #4364db; font-weight: 500; cursor: pointer;" onclick="window.abrirTelaAvaliacoesCompletas && window.abrirTelaAvaliacoesCompletas()">Ver mais &gt;</span>
      </div>
      <div class="reviews-summary" style="display: flex; align-items: center; gap: 6px; margin-bottom: 14px;">
        <span class="review-avg" style="font-size: 20px; font-weight: 800; color: #161823;">4.9</span>
        <span class="review-avg-total" style="font-size: 13px; color: #73747b;">/5</span>
        <span style="color: #f5a623; font-size: 14px;">★★★★★</span>
      </div>
      <div class="reviews-list">
{reviews_cards_html}
      </div>
    </section>'''

    # Usamos BeautifulSoup para substituir exatamente o elemento de reviews
    soup = BeautifulSoup(html, 'html.parser')
    
    rev_target = soup.select_one('.reviews-section, .customer-reviews-section, section.reviews-section')
    if rev_target:
        new_soup = BeautifulSoup(new_reviews_section, 'html.parser')
        rev_target.replace_with(new_soup)
    else:
        print(f"Alerta: elemento de reviews não encontrado em {page_path}")

    # Garante container de criadores
    if not soup.select_one('#creators-section'):
        rev_el = soup.select_one('.reviews-section')
        if rev_el:
            c_div = soup.new_tag('div', id='creators-section', attrs={'class': 'creators-section'})
            rev_el.insert_before(c_div)

    # Garante seller profile card
    if not soup.select_one('.seller-profile-card'):
        seller_html = f'''<div class="seller-profile-card" style="display: flex; align-items: center; justify-content: space-between; padding: 14px 16px; margin: 12px 0 16px 0; background: #ffffff; border-top: 1px solid #f2f2f2; border-bottom: 1px solid #f2f2f2;">
      <div style="display: flex; align-items: center; gap: 12px;">
        <img src="{pdata['seller_logo']}" alt="{pdata['brand']}" style="width: 48px; height: 48px; border-radius: 50%; object-fit: cover; border: 1px solid #eee;" onerror="this.src='../img/seller-default.png'">
        <div style="display: flex; flex-direction: column; gap: 2px;">
          <span style="font-size: 15px; font-weight: 700; color: #161823;">{pdata['brand']}</span>
          <span style="font-size: 11.5px; color: #73747b;">{pdata['seller_metrics']}</span>
        </div>
      </div>
      <button type="button" style="background: #fe2c55; color: #ffffff; font-size: 13px; font-weight: 600; border-radius: 18px; padding: 6px 18px; border: none; cursor: pointer;">Visitar</button>
    </div>'''
        about_el = soup.select_one('.about-product-section')
        if about_el:
            s_soup = BeautifulSoup(seller_html, 'html.parser')
            about_el.insert_before(s_soup)

    final_html = str(soup)
    
    # Atualiza rating link azul #4364db
    final_html = re.sub(
        r'(\(\d+(?:\.\d+)?[kK]?\))',
        r'<span style="color:#4364db; cursor:pointer;" onclick="window.abrirTelaAvaliacoesCompletas && window.abrirTelaAvaliacoesCompletas()">\1</span>',
        final_html,
        count=1
    )

    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Página {page_path} compilada com sucesso!")

def run_compiler():
    all_data = []
    for pid in PIDS:
        json_file = f"{DATA_DIR}/produto_{pid}.json"
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                all_data.append(json.load(f))
        else:
            print(f"Aviso: {json_file} ainda não gerado.")

    print(f"\nCompilando {len(all_data)} produtos finalizados...")
    if all_data:
        update_videos_criadores_js(all_data)
        for pdata in all_data:
            update_product_page(pdata)
    print("Compilação concluída!")

if __name__ == '__main__':
    run_compiler()
