import re

# 1. Atualizar css/style.css: remover pointer-events: none e forçar pointer-events: auto !important
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Substituir pointer-events: none por pointer-events: auto
css = css.replace('pointer-events: none;', 'pointer-events: auto !important;')

# Adicionar regras explícitas de interatividade no topo do CSS
counter_interactive_css = """
/* === INTERATIVIDADE DO CONTADOR E TOGGLE DE TAMANHO TIKTOK SHOP === */
.slider-counter,
.slider-counter-toggle,
.slider-tamanho-trigger,
.slider-pill-tab {
  pointer-events: auto !important;
  cursor: pointer !important;
  user-select: none !important;
  -webkit-user-select: none !important;
  touch-action: manipulation !important;
}
.slider-counter {
  z-index: 10 !important;
}
.slider-counter-toggle {
  z-index: 11 !important;
}
"""

if 'INTERATIVIDADE DO CONTADOR E TOGGLE DE TAMANHO' not in css:
    css = css + '\n' + counter_interactive_css

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("✓ css/style.css atualizado com pointer-events: auto !important")

# 2. Atualizar js/app.js: switchSliderTab robusto com stopPropagation e setProperty important
with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Encontrar switchSliderTab e substituir por versão blindada
old_switch_target = "window.switchSliderTab = function(tab) {"
idx_switch = js.find(old_switch_target)
if idx_switch != -1:
    idx_switch_end = js.find('};\n', idx_switch) + 2
    old_switch_block = js[idx_switch:idx_switch_end]
else:
    old_switch_block = ""

new_switch_block = """window.switchSliderTab = function(tab, e) {
  if (e) {
    if (typeof e.preventDefault === 'function') e.preventDefault();
    if (typeof e.stopPropagation === 'function') e.stopPropagation();
  }
  const guide = document.getElementById('slider-size-guide');
  const track = document.querySelector('.slider-track');
  const counterImages = document.getElementById('slider-counter-images') || document.querySelector('.slider-counter[data-has-tamanho="true"]');
  const counterSize = document.getElementById('slider-counter-size');

  if (tab === 'tamanho') {
    if (guide) {
      guide.style.setProperty('display', 'flex', 'important');
    }
    if (track) track.style.visibility = 'hidden';
    if (counterImages) counterImages.style.setProperty('display', 'none', 'important');
    if (counterSize) counterSize.style.setProperty('display', 'flex', 'important');
  } else {
    if (guide) {
      guide.style.setProperty('display', 'none', 'important');
    }
    if (track) track.style.visibility = 'visible';
    if (counterImages) counterImages.style.setProperty('display', 'flex', 'important');
    if (counterSize) counterSize.style.setProperty('display', 'none', 'important');
  }
};"""

if old_switch_block:
    js = js.replace(old_switch_block, new_switch_block)
else:
    js = new_switch_block + '\n' + js

# Atualizar o goto() para amarrar o evento de clique no counter
old_goto = """        counter.innerHTML = `<span id="slider-counter-num">${current + 1}/${imgs.length}</span> <span class="slider-tamanho-trigger" onclick="switchSliderTab('tamanho')" style="cursor:pointer; margin-left:2px; font-weight:500;">Tamanho</span>`;"""
new_goto = """        counter.innerHTML = `<span id="slider-counter-num">${current + 1}/${imgs.length}</span> <span class="slider-tamanho-trigger" onclick="switchSliderTab('tamanho', event)" style="cursor:pointer; margin-left:2px; font-weight:500; pointer-events:auto !important;">Tamanho</span>`;
        counter.onclick = function(ev) {
          if (ev.target && ev.target.classList.contains('slider-tamanho-trigger')) return;
          switchSliderTab('tamanho', ev);
        };"""

if old_goto in js:
    js = js.replace(old_goto, new_goto)

# Evitar que toques no counter disparem o drag do carrossel
old_touch = "sliderEl.addEventListener('touchstart', e => onStart(e.touches[0].clientX, e.touches[0].clientY), { passive: false });"
new_touch = """  // Não disparar drag se tocar nos botões de alternância
  sliderEl.addEventListener('touchstart', e => {
    if (e.target && (e.target.closest('.slider-counter') || e.target.closest('.slider-counter-toggle'))) return;
    onStart(e.touches[0].clientX, e.touches[0].clientY);
  }, { passive: false });"""

if old_touch in js:
    js = js.replace(old_touch, new_touch)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("✓ js/app.js atualizado com controle de eventos mobile à prova de falhas")

# 3. Atualizar pages/produto-104.html
with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Substituir o bloco do slider
old_slider_block_regex = re.compile(r'<!-- GUIA DE TAMANHOS OFICIAL TIKTOK SHOP[\s\S]*?</div>\s*</div>\s*<div class="slider-dots">', re.MULTILINE)

new_slider_block = """<!-- GUIA DE TAMANHOS OFICIAL TIKTOK SHOP (ALTERNÂNCIA 1:1 NO CARROSSEL) -->
      <div class="slider-size-guide" id="slider-size-guide" style="display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #ffffff; z-index: 5; align-items: center; justify-content: center; pointer-events: auto;">
        <img src="../img/guia-tamanhos-104.png?v=20261111" alt="Guia de tamanhos" style="width: 100%; height: 100%; object-fit: contain;">
      </div>

      <!-- BADGE 1: MODO FOTOS DO PRODUTO (1/8 Tamanho) -->
      <div class="slider-counter" id="slider-counter-images" data-has-tamanho="true" onclick="switchSliderTab('tamanho', event)" style="position: absolute; bottom: 12px; right: 12px; background: rgba(0,0,0,0.45); color: #fff; font-size: 11px; font-weight: 500; padding: 2.5px 8.5px; border-radius: 12px; backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px); z-index: 10; cursor: pointer; pointer-events: auto !important; display: flex; align-items: center; gap: 3px;">
        <span id="slider-counter-num">1/8</span>
        <span class="slider-tamanho-trigger" style="cursor: pointer; font-weight: 500;">Tamanho</span>
      </div>

      <!-- BADGE 2: MODO GUIA DE TAMANHO (Imagens | Tamanho) -->
      <div class="slider-counter-toggle" id="slider-counter-size" style="display: none; position: absolute; bottom: 12px; right: 12px; background: rgba(0, 0, 0, 0.45); border-radius: 14px; padding: 2px; backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px); z-index: 11; pointer-events: auto !important;">
        <button type="button" class="slider-pill-tab" onclick="switchSliderTab('imagens', event)" style="background: transparent; color: #ffffff; border: none; font-size: 11px; font-weight: 500; padding: 2.5px 8.5px; border-radius: 12px; cursor: pointer; pointer-events: auto !important;">Imagens</button>
        <button type="button" class="slider-pill-tab active" onclick="switchSliderTab('tamanho', event)" style="background: rgba(0, 0, 0, 0.38); color: #ffffff; border: none; font-size: 11px; font-weight: 600; padding: 2.5px 8.5px; border-radius: 12px; cursor: pointer; pointer-events: auto !important;">Tamanho</button>
      </div>
    </div>
    <div class="slider-dots">"""

html = old_slider_block_regex.sub(new_slider_block, html)

with open('pages/produto-104.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✓ pages/produto-104.html atualizado")
print("✅ SUCESSO TOTAL!")
