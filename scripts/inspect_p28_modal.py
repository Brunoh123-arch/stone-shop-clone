# -*- coding: utf-8 -*-
with open('pages/produto-28.html', 'r', encoding='utf-8') as f:
    txt = f.read()

import re
# Procura seletor de SKU / modal de compra
idx = txt.find('sku-modal')
if idx == -1:
    idx = txt.find('modal-content')
if idx == -1:
    idx = txt.find('variation')
if idx != -1:
    print("Trecho de variacoes / modal de compra:")
    print(txt[idx:idx+1500])
else:
    print("Nao achou sku-modal nem modal-content!")
    # Procura onde tem 'Compre' ou 'Adicionar'
    btn_idx = txt.find('btn-buy')
    if btn_idx != -1:
        print(txt[btn_idx-200:btn_idx+400])
