import os

with open('js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Localizar a função buildCardHtml
fn_start = code.find('function buildCardHtml(item, idx) {')
if fn_start == -1:
    print("ERRO: buildCardHtml não encontrada!")
    exit(1)

# Encontrar o fechamento de buildCardHtml
fn_end = code.find('\n  // Divisão balanceada em 2 colunas', fn_start)
if fn_end == -1:
    fn_end = code.find('const colLeft = [];', fn_start)

print(f"Substituindo buildCardHtml de {fn_start} até {fn_end}")

new_build_card_html = """function buildCardHtml(item, idx) {
    const ratio = item.video ? '3 / 4' : ASPECT_RATIOS[idx % ASPECT_RATIOS.length];
    const linkHref = isPagesDir ? `produto-${item.id}.html` : `pages/produto-${item.id}.html`;
    
    const parts = (item.preco || '19,90').split(',');
    const precoInt = parts[0];
    const precoCent = parts[1] || '00';

    const badge1111Html = item.is1111 ? `
      <span class="badge-1111" style="background:linear-gradient(135deg, #ff004f, #fe2c55); color:#fff; font-size:9.5px; font-weight:800; padding:1.5px 5px; border-radius:3px; margin-right:4px; vertical-align:middle; display:inline-block; line-height:1.2; letter-spacing:-0.2px;">11.11</span>
    ` : '';

    let badgesHtml = '';
    if (item.badgeTipo === 'relampago') {
      badgesHtml = `
        <span style="background:#fff2e8; color:#ff5722; font-size:10px; font-weight:700; padding:1.5px 5px; border-radius:2px; display:inline-flex; align-items:center; gap:2.5px;">
          <svg width="9" height="9" viewBox="0 0 24 24" fill="currentColor"><path d="M13 2L3 14h8l-1 8 11-12h-8l1-8z"/></svg> Oferta Relâmpago
        </span>
      `;
    } else {
      badgesHtml = `
        <span style="background:#fff0f3; color:#fe2c55; font-size:10px; font-weight:700; padding:1.5px 5px; border-radius:2px; display:inline-flex; align-items:center; gap:2px;">
          <svg width="8" height="8" viewBox="0 0 24 24" fill="currentColor"><path d="M12.7 2.3c-.4-.4-1-.4-1.4 0l-9 9c-.4.4-.4 1 0 1.4l9 9c.4.4 1 .4 1.4 0l9-9c.4-.4.4-1 0-1.4l-9-9z"/></svg> ${item.descOff || '60% OFF'}
        </span>
        <span style="background:#e8f7f5; color:#00a699; font-size:10px; font-weight:600; padding:1.5px 5px; border-radius:2px;">Frete grátis</span>
      `;
    }

    return `
      <a class="related-card" href="${linkHref}" style="background:#fff; border-radius:8px; overflow:hidden; border:none; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-decoration:none; color:inherit; display:flex; flex-direction:column; width:100%; box-sizing:border-box; position:relative; margin-bottom:8px;">
        <div class="related-img-wrapper" style="position:relative; width:100%; aspect-ratio:${ratio}; overflow:hidden; background:#000;">
          ${item.video ? `
            <video class="related-card-video" src="${item.video}" poster="${item.poster || ''}" autoplay muted loop playsinline style="width:100%; height:100%; object-fit:cover; display:block;"></video>
            <!-- BADGE DE PLAY/PAUSE E TEMPO 1:1 TIKTOK SHOP OFICIAL -->
            <div class="tt-feed-video-badge" style="position:absolute; top:8px; left:8px; background:rgba(0,0,0,0.45); color:#fff; font-size:11px; font-weight:600; padding:2px 7.5px; border-radius:12px; display:inline-flex; align-items:center; gap:4.5px; backdrop-filter:blur(4px); -webkit-backdrop-filter:blur(4px); z-index:3; font-family:-apple-system,BlinkMacSystemFont,'Plus Jakarta Sans',sans-serif; letter-spacing:0.2px;">
              <!-- Ícone de Pause ❚❚ oficial (indicando reprodução contínua) -->
              <span style="display:inline-flex; align-items:center; gap:2px; height:9px;">
                <span style="width:2.5px; height:9px; background:#ffffff; border-radius:0.8px;"></span>
                <span style="width:2.5px; height:9px; background:#ffffff; border-radius:0.8px;"></span>
              </span>
              <span>${item.duracao || '00:28'}</span>
            </div>
            <!-- CRIADOR: AVATAR + NOME OFICIAL -->
            <div style="position:absolute; bottom:8px; left:8px; display:flex; align-items:center; gap:5.5px; z-index:3;">
              <img src="${item.avatar}" style="width:20px; height:20px; border-radius:50%; object-fit:cover; border:1px solid #ffffff; box-shadow:0 1px 3px rgba(0,0,0,0.4);" alt="">
              <span style="color:#ffffff; font-size:11px; font-weight:600; text-shadow:0 1px 3px rgba(0,0,0,0.85); letter-spacing:-0.1px;">${item.name}</span>
            </div>
          ` : `
            <img src="${item.img}" alt="${item.title}" loading="lazy" style="width:100%; height:100%; object-fit:cover; display:block;">
          `}
        </div>
        <div class="related-card-info" style="padding:7px 8px 10px; display:flex; flex-direction:column; gap:4px; flex:1;">
          <!-- LINHA DO TÍTULO COM MINI-THUMBNAIL DO PRODUTO (PARIDADE 1:1 TIKTOK SHOP) -->
          <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:6px;">
            <h4 class="related-card-title" style="font-size:12px; font-weight:400; line-height:1.35; color:#161823; margin:0; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; flex:1; min-width:0;">
              ${badge1111Html}${item.title}
            </h4>
            ${item.video ? `
              <!-- QUADRADINHO DO PRODUTO (THUMBNAIL OFICIAL) -->
              <img src="${item.img}" alt="${item.title}" style="width:38px; height:38px; min-width:38px; border-radius:4px; object-fit:cover; border:1px solid #f0f0f0; margin-top:1px; flex-shrink:0;" loading="lazy">
            ` : ''}
          </div>

          <div style="display:flex; align-items:baseline; gap:4px; margin-top:2px;">
            <div style="color:#fe2c55; font-size:11px; font-weight:700;">
              R$ <span style="font-size:15px; font-weight:800;">${precoInt}</span><span style="font-size:11px; font-weight:700;">,${precoCent}</span>
            </div>
            <span style="color:#8a8b91; font-size:10px; text-decoration:line-through;">R$ ${item.precoOrig}</span>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:3px; margin-top:1px;">
            ${badgesHtml}
          </div>
          <div style="display:flex; align-items:center; gap:4px; margin-top:2px; font-size:10px; color:#73747b;">
            <span style="color:#ff8c00; font-weight:700; display:inline-flex; align-items:center; gap:1.5px;">
              ★ ${item.rating}
            </span>
            <span>|</span>
            <span>${item.vendidos}</span>
          </div>
        </div>
      </a>
    `;
  }
"""

new_code = code[:fn_start] + new_build_card_html + '\n' + code[fn_end:]
with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("✅ js/app.js: buildCardHtml atualizado com paridade 1:1 ao TikTok Shop!")
