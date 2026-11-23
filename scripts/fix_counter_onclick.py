with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Substituir o trecho bugado do if no onclick
old_part = """        counter.innerHTML = `<span id="slider-counter-num">${current + 1}/${imgs.length}</span> <span class="slider-tamanho-trigger" onclick="switchSliderTab('tamanho', event)" style="cursor:pointer; margin-left:2px; font-weight:500; pointer-events:auto !important;">Tamanho</span>`;
        counter.onclick = function(ev) {
          if (ev.target && ev.target.classList.contains('slider-tamanho-trigger')) return;
          switchSliderTab('tamanho', ev);
        };"""

new_part = """        counter.innerHTML = `<span id="slider-counter-num">${current + 1}/${imgs.length}</span> <span class="slider-tamanho-trigger" style="cursor:pointer; margin-left:2px; font-weight:500; pointer-events:auto !important;">Tamanho</span>`;
        counter.onclick = function(ev) {
          switchSliderTab('tamanho', ev);
        };"""

if old_part in js:
    js = js.replace(old_part, new_part)
    print("✓ Removido if que bloqueava o clique em slider-tamanho-trigger")
else:
    print("AVISO: old_part não bateu exato!")

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("✅ js/app.js corrigido!")
