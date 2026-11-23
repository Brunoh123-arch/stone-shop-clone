import os

with open('js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update openSizeGuideModal to prefer official image
old_modal_start = """function openSizeGuideModal() {
  const existing = document.getElementById('size-guide-modal-overlay');
  if (existing) existing.remove();

  const nomeProd = (typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL.nome) ? PRODUTO_ATUAL.nome.toLowerCase() : '';
  const isCalcado = nomeProd.includes('chinelo') || nomeProd.includes('sandália') || nomeProd.includes('sapato') || nomeProd.includes('tênis');

  let tableContent = '';"""

new_modal_start = """function openSizeGuideModal() {
  const existing = document.getElementById('size-guide-modal-overlay');
  if (existing) existing.remove();

  const guideImgEl = document.querySelector('#slider-size-guide img') || document.querySelector('.size-guide-image-container img') || document.querySelector('.size-guide-image-card img');
  const officialImgSrc = guideImgEl ? guideImgEl.src : '';

  const nomeProd = (typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL.nome) ? PRODUTO_ATUAL.nome.toLowerCase() : '';
  const isCalcado = nomeProd.includes('chinelo') || nomeProd.includes('sandália') || nomeProd.includes('sapato') || nomeProd.includes('tênis');

  let tableContent = '';
  if (officialImgSrc) {
    tableContent = `<div style="text-align:center; padding:6px 0;"><img src="${officialImgSrc}" alt="Guia de tamanhos oficial" style="max-width:100%; height:auto; border-radius:8px; display:block; margin:0 auto;"></div>`;
  } else"""

if old_modal_start in text:
    text = text.replace(old_modal_start, new_modal_start)
    print('Updated openSizeGuideModal!')
else:
    print('Warning: old_modal_start not found!')

# 2. Update initSlider goto counter touch trigger
old_goto_counter = """      if (hasTamanho) {
        counter.setAttribute('data-has-tamanho', 'true');
        counter.innerHTML = `<span id="slider-counter-num">${current + 1}/${imgs.length}</span> <span class="slider-tamanho-trigger" style="cursor:pointer; margin-left:2px; font-weight:500; pointer-events:auto !important;">Tamanho</span>`;
        counter.onclick = function(ev) {
          switchSliderTab('tamanho', ev);
        };
      }"""

new_goto_counter = """      if (hasTamanho) {
        counter.setAttribute('data-has-tamanho', 'true');
        counter.setAttribute('role', 'button');
        counter.setAttribute('tabindex', '0');
        counter.innerHTML = `<span id="slider-counter-num">${current + 1}/${imgs.length}</span> <span class="slider-tamanho-trigger" style="cursor:pointer; margin-left:2px; font-weight:500; pointer-events:auto !important;">Tamanho</span>`;
        const triggerTab = function(ev) {
          if (ev) {
            if (typeof ev.preventDefault === 'function') ev.preventDefault();
            if (typeof ev.stopPropagation === 'function') ev.stopPropagation();
          }
          switchSliderTab('tamanho', ev);
        };
        counter.onclick = triggerTab;
        counter.ontouchend = triggerTab;
      }"""

if old_goto_counter in text:
    text = text.replace(old_goto_counter, new_goto_counter)
    print('Updated goto counter ontouchend trigger!')
else:
    print('Warning: old_goto_counter not found!')

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('js/app.js updated successfully!')
