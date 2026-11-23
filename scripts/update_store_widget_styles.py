with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's locate the else branch in renderStoreWidget
old_block_marker = '<!-- Cabeçalho Flex da Loja -->'
# We can find where 'store-widget-section' starts inside renderStoreWidget
idx_widget = content.find('function renderStoreWidget() {')
if idx_widget == -1:
    print("renderStoreWidget not found")
    exit(1)

# Find else branch
idx_else = content.find('} else {', idx_widget)
idx_end_else = content.find('reviewsSection.insertAdjacentHTML', idx_else)

old_else_content = content[idx_else:idx_end_else]
print("Old else block found, length:", len(old_else_content))

new_else_content = """} else {
      widgetHtml = `
        <div class="store-widget-section" style="background:#fff; padding:16px; margin:0; border-top:8px solid #f5f5f5; border-bottom:8px solid #f5f5f5; box-sizing:border-box; font-family:-apple-system,BlinkMacSystemFont,\\"Segoe UI\\",Roboto,Helvetica,Arial,sans-serif;">
          <!-- Cabeçalho Flex da Loja (100% Paridade com a Referência Oficial do TikTok Shop) -->
          <div class="store-widget-header" style="display:flex; align-items:center; gap:12px; margin-bottom:12px; width:100%; box-sizing:border-box;">
            <div class="store-widget-logo-wrapper" style="position:relative; width:48px; height:48px; border-radius:50%; border:1px solid #f0f0f0; overflow:hidden; flex-shrink:0; display:flex; align-items:center; justify-content:center; background:#f8f8f8;">
              <img class="store-widget-logo" src="../logo.png" onerror="this.src='https://via.placeholder.com/48'" alt="Stone Shop" style="width:100%; height:100%; object-fit:cover;">
            </div>
            <div class="store-widget-info" style="flex:1; min-width:0; display:flex; flex-direction:column; justify-content:center;">
              <div class="store-widget-name" style="font-size:16px; font-weight:600; color:#161823; letter-spacing:-0.2px; line-height:1.25; margin-bottom:2px; display:flex; align-items:center; gap:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                Stone Shop
                <svg viewBox="0 0 24 24" width="14" height="14" style="color:#0095f6; flex-shrink:0; vertical-align:middle;" fill="currentColor">
                  <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </div>
              ${window.location.pathname.includes('produto-101') ? `
              <div class="store-widget-pirelli" style="display:flex; align-items:center; gap:6px; margin-top:-1px; margin-bottom:-1px; padding:0;">
                <img src="../logopirelli/pirelli.png" alt="Pirelli" style="height:24px; object-fit:contain; vertical-align:middle; border-radius:2px;">
                <span style="color:#bbb; font-size:13px; line-height:1; font-weight:300;">|</span>
                <span style="font-size:11px; color:#555; font-weight:500; letter-spacing:0.1px;">Loja Credenciada</span>
              </div>` : ''}
              <div class="store-widget-sales" style="font-size:12.5px; color:#8a8b91; font-weight:400; margin-top:1px; line-height:1.2;">112.2K vendido(s)</div>
            </div>
            <!-- Botão Visitar Idêntico à Imagem 2 (Flat, border-radius: 18px, font-weight: 600, sem sombra) -->
            <button class="store-widget-btn-visitar" onclick="window.location.href='../index.html'" style="background:#fe2c55; color:#fff; font-size:13.5px; font-weight:600; padding:6px 18px; height:34px; border-radius:18px; border:none; cursor:pointer; flex-shrink:0; outline:none; box-shadow:none; letter-spacing:-0.2px; display:inline-flex; align-items:center; justify-content:center; -webkit-tap-highlight-color:transparent;">Visitar</button>
          </div>
          
          <!-- Estatísticas da Loja (Números 95% e 99% em #161823 font-weight:700 e textos em #8a8b91 font-weight:400) -->
          <div class="store-widget-stats" style="display:flex; align-items:center; gap:20px; margin-bottom:14px; margin-top:2px;">
            <span style="display:inline-flex; align-items:baseline; font-size:12px; color:#8a8b91; font-weight:400; letter-spacing:-0.1px;">
              <strong style="color:#161823; font-weight:700; font-size:12.5px; margin-right:3px;">95%</strong>responde em 24 horas
            </span>
            <span style="display:inline-flex; align-items:baseline; font-size:12px; color:#8a8b91; font-weight:400; letter-spacing:-0.1px;">
              <strong style="color:#161823; font-weight:700; font-size:12.5px; margin-right:3px;">99%</strong>envios pontuais
            </span>
          </div>
          
          <!-- Título Mais Desta Loja -->
          <div class="store-widget-title-row" onclick="window.location.href='../index.html'" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; cursor:pointer;">
            <span class="store-widget-section-title" style="font-size:13.5px; font-weight:700; color:#222;">Mais desta loja</span>
            <span class="store-widget-arrow" style="font-size:16px; color:#888; line-height:1; font-weight:300;">›</span>
          </div>
          
          <!-- Carrossel horizontal de produtos -->
          <div class="store-widget-products-scroll" style="display:flex; gap:10px; overflow-x:auto; padding-bottom:4px; width:100%; -webkit-overflow-scrolling:touch; box-sizing:border-box; scrollbar-width:none;">
            ${couponHtml}
            ${itemsHtml}
          </div>
        </div>
      `;
    }

    """

content = content[:idx_else] + new_else_content + content[idx_end_else:]
with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: Updated store widget to match Image 2 reference perfectly!")
