import asyncio
import os
import sys
import json

sys.path.append(os.path.dirname(__file__))
from test_p42_search import search_google

sys.stdout.reconfigure(line_buffering=True)

async def main():
    queries = [
        'site:tiktok.com/pdp "cadeira de praia"',
        'site:shop.tiktok.com/pdp "cadeira de praia"',
        'site:tiktok.com/pdp cadeira praia',
        'site:tiktok.com/view/product cadeira praia',
        'tiktok shop cadeira de praia mor site:tiktok.com'
    ]
    
    all_results = []
    for q in queries:
        print(f"\n==========================================")
        print(f">>> Buscando: {q}")
        print(f"==========================================")
        try:
            res = await search_google(q)
            all_results.extend(res)
        except Exception as e:
            print("Erro na busca:", e)
        
    print(f"\nTotal bruto de resultados: {len(all_results)}")
    unique = {}
    for href, txt in all_results:
        clean = href.split('?')[0]
        if clean not in unique:
            unique[clean] = txt
            print(f"ENCONTRADO: {clean} | {txt[:60]}")
            
    with open("scripts/data/praia_search_p42.json", "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
