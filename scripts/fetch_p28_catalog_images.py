# -*- coding: utf-8 -*-
"""
Busca imagens oficiais de catalogo do Kit Mochila Rebecca Bonbon (Costas, Frente, Detalhes, Cores)
para preencher o slider do P28 com 6 a 8 fotos de alta resolucao.
"""
import urllib.request
import json
import re
import os

# Vamos buscar fotos de catalogo no ML via API pública ou scrap limpo de imagens
# Anuncio oficial do ML: MLB63115237 ou similar
url = "https://api.mercadolibre.com/items/MLB63115237"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req, timeout=10) as res:
        data = json.loads(res.read().decode('utf-8'))
        pictures = data.get('pictures', [])
        print(f"API ML retornou {len(pictures)} fotos oficiais!")
        for idx, p in enumerate(pictures, 1):
            secure_url = p.get('secure_url') or p.get('url')
            size = p.get('size')
            print(f"  [{idx}] {secure_url} ({size})")
except Exception as e:
    print(f"Erro na API direta do item MLB63115237: {e}")

# Busca geral de itens de mochila rebecca bonbon kit no ML API
search_url = "https://api.mercadolibre.com/sites/MLB/search?q=mochila%20rebecca%20bonbon%20kit&limit=5"
try:
    req2 = urllib.request.Request(search_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req2, timeout=10) as res2:
        sdata = json.loads(res2.read().decode('utf-8'))
        results = sdata.get('results', [])
        print(f"\nBusca ML retornou {len(results)} itens:")
        for r in results:
            print(f"  Item: {r.get('id')} - {r.get('title')[:60]} - Thumbnail: {r.get('thumbnail')}")
            # Pega detalhes do primeiro item com varias fotos
            item_url = f"https://api.mercadolibre.com/items/{r.get('id')}"
            try:
                with urllib.request.urlopen(urllib.request.Request(item_url, headers={"User-Agent": "Mozilla/5.0"}), timeout=5) as ires:
                    idata = json.loads(ires.read().decode('utf-8'))
                    ipics = idata.get('pictures', [])
                    print(f"    -> {len(ipics)} fotos oficiais encontradas neste item!")
                    if len(ipics) >= 6:
                        with open('scripts/data/p28_catalog_pics.json', 'w', encoding='utf-8') as pf:
                            json.dump(ipics, pf, indent=2, ensure_ascii=False)
                        print("    [+] Salvo em scripts/data/p28_catalog_pics.json!")
                        break
            except Exception as ex:
                pass
except Exception as e:
    print(f"Erro na busca: {e}")
