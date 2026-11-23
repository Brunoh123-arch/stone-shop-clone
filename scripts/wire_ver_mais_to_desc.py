import re

file_path = 'pages/produto-104.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the block from <!-- ITEM 4: GUIA DE TAMANHOS until <!-- FAIXA DIVISORA
old_guide_and_desc = re.search(r'<!-- ITEM 4: GUIA DE TAMANHOS.*?<!-- FAIXA DIVISORA', content, flags=re.DOTALL)
if not old_guide_and_desc:
    print("Could not find guide and desc block!")
    exit(1)

new_guide_and_desc = '''<!-- ITEM 4: GUIA DE TAMANHOS OFICIAL TIKTOK SHOP -->
        <div class="size-guide-block">
          <h3 class="about-subtitle">Guia de tamanhos</h3>
          <div class="size-guide-card-tt">
            <div class="size-guide-tag">
              <span>📐</span>
              <span>Tabela de Medidas – Calçados</span>
            </div>
            <div class="size-guide-pills-list">
              <div class="size-pill-item">33/34 — 23 cm</div>
              <div class="size-pill-item">35/36 — 24 cm</div>
              <div class="size-pill-item">37/38 — 25 cm</div>
              <div class="size-pill-item">39/40 — 26 cm</div>
            </div>
          </div>
          <!-- BOTÃO VER MAIS CENTRALIZADO (ABRE A DESCRIÇÃO DO PRODUTO) -->
          <button type="button" class="btn-toggle-centered" id="btn-toggle-ver-mais" onclick="toggleSobreProdutoDescricao(true)">
            <span>Ver mais</span>
            <svg class="toggle-icon-centered" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
        </div>

        <!-- ITEM 5: DESCRIÇÃO REFINADA OFICIAL TIKTOK SHOP (INICIALMENTE OCULTA / REVELADA NO VER MAIS) -->
        <div class="description-section" id="sobre-produto-desc-section" style="display: none !important;">
          <h3 class="about-subtitle">Descrição</h3>
          <div class="description-text">
            <p><strong>Descrição:</strong></p>
            <p>✨ <strong>Elegância em cada passo</strong> ✨</p>
            <p>Este chinelo feminino é perfeito para quem busca conforto e estilo. Com strass brilhante, ele adiciona um toque de luxo a qualquer look. A textura macia e leve garante um uso agradável o dia todo. Ideal para ocasiões que exigem um toque especial.</p>
            <p>• <strong>Características principais:</strong> • Strass brilhante • Textura macia • Peso leve</p>
            <p>Este chinelo combina perfeitamente com qualquer roupa, oferecendo estilo e conforto. Experimente e sinta a diferença!</p>
          </div>
          <!-- BOTÃO VER MENOS CENTRALIZADO (FECHA A DESCRIÇÃO) -->
          <button type="button" class="btn-toggle-centered" id="btn-toggle-ver-menos" onclick="toggleSobreProdutoDescricao(false)">
            <span>Ver menos</span>
            <svg class="toggle-icon-centered rotated-up" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
        </div>

        <!-- FAIXA DIVISORA'''

content = content[:old_guide_and_desc.start()] + new_guide_and_desc + content[old_guide_and_desc.end()-16:]

# Add or update the toggleSobreProdutoDescricao function in the script block
js_func = '''
window.toggleSobreProdutoDescricao = function(expand) {
  var desc = document.getElementById('sobre-produto-desc-section');
  var btnMais = document.getElementById('btn-toggle-ver-mais');
  if (!desc) return;

  if (expand) {
    desc.style.setProperty('display', 'block', 'important');
    if (btnMais) btnMais.style.display = 'none';
    desc.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } else {
    desc.style.setProperty('display', 'none', 'important');
    if (btnMais) btnMais.style.display = 'flex';
    var guide = document.querySelector('.size-guide-block');
    if (guide) guide.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
};

// Integração com a aba "Descrição" no topo
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.product-tab').forEach(function(tab) {
    tab.addEventListener('click', function() {
      var tabType = this.getAttribute('data-tab');
      if (tabType === 'descricao') {
        window.toggleSobreProdutoDescricao(true);
      }
    });
  });
});
'''

if 'window.toggleSobreProdutoDescricao' not in content:
    content = content.replace('window.toggleDescriptionText =', js_func + '\nwindow.toggleDescriptionText =')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied interactive Ver mais -> Descrição reveal to produto-104.html!")
