import re

# 1. Atualizar pages/produto-104.html
with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_slider_counter = '<div class="slider-counter" data-has-tamanho="true">1/8 Tamanho</div>'

new_slider_elements = """      <!-- GUIA DE TAMANHOS OFICIAL TIKTOK SHOP (ALTERNÂNCIA 1:1 NO CARROSSEL) -->
      <div class="slider-size-guide" id="slider-size-guide" style="display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #ffffff; z-index: 5; align-items: center; justify-content: center;">
        <img src="../img/guia-tamanhos-104.png?v=20261111" alt="Guia de tamanhos" style="width: 100%; height: 100%; object-fit: contain;">
      </div>

      <!-- BADGE 1: MODO FOTOS DO PRODUTO (1/8 Tamanho) -->
      <div class="slider-counter" id="slider-counter-images" data-has-tamanho="true" style="cursor: pointer;">
        <span id="slider-counter-num">1/8</span> <span class="slider-tamanho-trigger" onclick="switchSliderTab('tamanho')" style="cursor: pointer; margin-left: 2px; font-weight: 500;">Tamanho</span>
      </div>

      <!-- BADGE 2: MODO GUIA DE TAMANHO (Imagens | Tamanho) -->
      <div class="slider-counter-toggle" id="slider-counter-size" style="display: none; position: absolute; bottom: 12px; right: 12px; background: rgba(0, 0, 0, 0.45); border-radius: 14px; padding: 2px; backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px); z-index: 10;">
        <button type="button" class="slider-pill-tab" onclick="switchSliderTab('imagens')" style="background: transparent; color: #ffffff; border: none; font-size: 11px; font-weight: 500; padding: 2.5px 8.5px; border-radius: 12px; cursor: pointer;">Imagens</button>
        <button type="button" class="slider-pill-tab active" style="background: rgba(0, 0, 0, 0.38); color: #ffffff; border: none; font-size: 11px; font-weight: 600; padding: 2.5px 8.5px; border-radius: 12px; cursor: pointer;">Tamanho</button>
      </div>"""

if old_slider_counter in html:
    html = html.replace(old_slider_counter, new_slider_elements)
    with open('pages/produto-104.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ pages/produto-104.html atualizado com slider-size-guide e badges alternáveis!")
else:
    print("AVISO: old_slider_counter não encontrado em produto-104.html")

# 2. Atualizar js/app.js para suportar switchSliderTab e preservar botões no goto()
with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Substituir o trecho do goto() no initSlider
old_goto_counter = """      const hasTamanho = counter.getAttribute('data-has-tamanho') || counter.textContent.includes('Tamanho');
      if (hasTamanho) {
        counter.setAttribute('data-has-tamanho', 'true');
        counter.textContent = `${current + 1}/${imgs.length} Tamanho`;
      } else {
        counter.textContent = `${current + 1}/${imgs.length}`;
      }"""

new_goto_counter = """      const hasTamanho = counter.getAttribute('data-has-tamanho') || counter.textContent.includes('Tamanho');
      if (hasTamanho) {
        counter.setAttribute('data-has-tamanho', 'true');
        counter.innerHTML = `<span id="slider-counter-num">${current + 1}/${imgs.length}</span> <span class="slider-tamanho-trigger" onclick="switchSliderTab('tamanho')" style="cursor:pointer; margin-left:2px; font-weight:500;">Tamanho</span>`;
      } else {
        counter.textContent = `${current + 1}/${imgs.length}`;
      }"""

if old_goto_counter in js:
    js = js.replace(old_goto_counter, new_goto_counter)
    print("✓ js/app.js: initSlider goto() atualizado para manter o botão Tamanho interativo")
else:
    print("AVISO: old_goto_counter não encontrado em js/app.js")

# Injetar a função global switchSliderTab no window
switch_slider_fn = """// === TIKTOK SHOP OFICIAL: TOGGLE CARROSSEL IMAGENS <-> GUIA DE TAMANHOS ===
window.switchSliderTab = function(tab) {
  const guide = document.getElementById('slider-size-guide');
  const track = document.querySelector('.slider-track');
  const counterImages = document.getElementById('slider-counter-images') || document.querySelector('.slider-counter[data-has-tamanho="true"]');
  const counterSize = document.getElementById('slider-counter-size');

  if (tab === 'tamanho') {
    if (guide) guide.style.display = 'flex';
    if (track) track.style.visibility = 'hidden';
    if (counterImages) counterImages.style.display = 'none';
    if (counterSize) counterSize.style.display = 'flex';
  } else {
    if (guide) guide.style.display = 'none';
    if (track) track.style.visibility = 'visible';
    if (counterImages) counterImages.style.display = 'flex';
    if (counterSize) counterSize.style.display = 'none';
  }
};
"""

if 'window.switchSliderTab =' not in js:
    js = switch_slider_fn + '\n' + js
    print("✓ js/app.js: window.switchSliderTab injetado")

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("✅ Todos os arquivos sincronizados com a alternância nativa Imagens/Tamanho!")
