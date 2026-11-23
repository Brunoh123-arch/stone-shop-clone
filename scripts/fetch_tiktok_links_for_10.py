from playwright.sync_api import sync_playwright
import urllib.parse
import json
import time

products = [
    {
        "id": 9,
        "name": "Ar Condicionado Portatil HQ 8500",
        "queries": [
            'site:tiktok.com "ar condicionado portatil" hq',
            'site:tiktok.com ar condicionado portatil unboxing',
            'site:tiktok.com ar condicionado portatil testando'
        ]
    },
    {
        "id": 10,
        "name": "Ar-Condicionado Portatil Hisense 12000",
        "queries": [
            'site:tiktok.com "ar condicionado" hisense portatil',
            'site:tiktok.com "hisense" ar condicionado portatil',
            'site:tiktok.com ar condicionado portatil 12000'
        ]
    },
    {
        "id": 11,
        "name": "Climatizador de Ar Oster 4 em 1",
        "queries": [
            'site:tiktok.com "climatizador" oster',
            'site:tiktok.com climatizador oster 4 em 1',
            'site:tiktok.com climatizador de ar oster'
        ]
    },
    {
        "id": 13,
        "name": "Piscina Borda Inflavel Pixlar 1000L",
        "queries": [
            'site:tiktok.com "piscina" inflavel 1000 litros',
            'site:tiktok.com piscina inflavel 1000l',
            'site:tiktok.com montando piscina inflavel 1000'
        ]
    },
    {
        "id": 14,
        "name": "Churrasqueira Eletrica Arke Vitta Smart",
        "queries": [
            'site:tiktok.com "churrasqueira arke"',
            'site:tiktok.com churrasqueira rotativa arke',
            'site:tiktok.com "arke vitta smart"'
        ]
    },
    {
        "id": 15,
        "name": "Churrasqueira Biscuitt Steak Master",
        "queries": [
            'site:tiktok.com "churrasqueira biscuitt"',
            'site:tiktok.com churrasqueira portatil carvão biscuitt',
            'site:tiktok.com churrasqueira steak master'
        ]
    },
    {
        "id": 17,
        "name": "Kit Cadeiras de Praia Mor",
        "queries": [
            'site:tiktok.com cadeira de praia mor',
            'site:tiktok.com kit cadeira de praia mor',
            'site:tiktok.com cadeira praia mor unboxing'
        ]
    },
    {
        "id": 18,
        "name": "Kit Praia Carrinho Guarda Sol Mor",
        "queries": [
            'site:tiktok.com kit praia carrinho guarda sol',
            'site:tiktok.com carrinho de praia mor cooler',
            'site:tiktok.com mesa praia guarda sol mor'
        ]
    },
    {
        "id": 21,
        "name": "Bola De Futebol De Campo Penalty Bravo",
        "queries": [
            'site:tiktok.com "penalty bravo"',
            'site:tiktok.com bola penalty bravo campo',
            'site:tiktok.com unboxing bola penalty'
        ]
    },
    {
        "id": 22,
        "name": "Colchão Inflável Casal Bestway Camping",
        "queries": [
            'site:tiktok.com "colchão inflavel" bestway',
            'site:tiktok.com colchão inflavel casal unboxing',
            'site:tiktok.com enchendo colchao inflavel bestway'
        ]
    }
]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        headless=True
    )
    page = browser.new_page(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    )
    
    for prod in products:
        pid = prod["id"]
        print(f"\n==========================================")
        print(f"Buscando links para Produto {pid}: {prod['name']}")
        print(f"==========================================")
        
        found_links = set()
        for q in prod["queries"]:
            url = f"https://www.google.com/search?q={urllib.parse.quote(q)}"
            print(f"  Query: {q}")
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=15000)
                page.wait_for_timeout(1500)
                hrefs = page.eval_on_selector_all('a[href]', 'elements => elements.map(e => e.href)')
                for h in hrefs:
                    if 'tiktok.com/@' in h and '/video/' in h:
                        clean = h.split('?')[0]
                        found_links.add(clean)
                        print(f"    -> Encontrado: {clean}")
            except Exception as e:
                print(f"    -> Erro na query: {e}")
            if len(found_links) >= 5:
                break
        
        results[pid] = list(found_links)
        print(f"Total coletado para Produto {pid}: {len(found_links)} links")
        time.sleep(1)
        
    browser.close()

with open('scripts/batch_10_tiktok_links.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nBusca de todos os 10 produtos concluida com sucesso!")
