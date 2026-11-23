# -*- coding: utf-8 -*-
html = open('pages/produto-87.html', 'r', encoding='utf-8').read()

# Imprime o bloco da descrição com a tabela/guia
idx = html.find('Guia de Tamanhos')
if idx != -1:
    print("=== BLOCO NA DESCRIÇÃO ===")
    print(html[idx-100:idx+400])

# Imprime o botão do seletor
idx2 = html.find('Tabela de medidas')
if idx2 == -1:
    idx2 = html.find('Guia de tamanhos')
if idx2 != -1:
    print("\n=== BLOCO NO SELETOR ===")
    print(html[idx2-100:idx2+300])
