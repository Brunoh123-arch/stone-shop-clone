import urllib.request
import json
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
search_url = 'https://lista.mercadolivre.com.br/travesseiro-cervical-ortopedico-ergonomico'
req = urllib.request.Request(search_url, headers=headers)

try:
    html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
    # Buscar os links de produtos com seus IDs MLB
    items = re.findall(r'href="(https://[a-z\.]*mercadolivre\.com\.br/[^"]*MLB-?(\d+)[^"]*)"', html)
    print(f"Total itens encontrados: {len(items)}")
    unique_mlbs = []
    for url, mlb in items:
        if mlb not in unique_mlbs:
            unique_mlbs.append(mlb)
            print(f"MLB: {mlb} -> {url[:80]}")
            if len(unique_mlbs) >= 5:
                break
except Exception as e:
    print("Erro:", e)
