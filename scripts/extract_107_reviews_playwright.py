import os
import json
import re
import time
import urllib.request
from playwright.sync_api import sync_playwright

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

def download_file(url, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"Already exists: {out_path}")
        return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(out_path, 'wb') as f:
                f.write(data)
            print(f"Downloaded ({len(data)}b): {out_path}")
            return True
    except Exception as e:
        print(f"Error downloading {url} -> {out_path}: {e}")
        return False

def run():
    pdp_urls = [
        'https://shop.tiktok.com/br/pdp/aspirador-de-po-sem-fio-portatil-usb-bivolt-leve-e-pratico-limpeza-profunda/1734454382398113247',
        'https://shop.tiktok.com/br/pdp/mini-aspirador-3-em-1-portatil-recarregavel-para-casa-e-carro/1734041227283236599',
        'https://shop.tiktok.com/br/pdp/1732873703398016709',
        'https://shop.tiktok.com/br/c/usb-vacuums/803856'
    ]

    all_reviews = []
    intercepted_jsons = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel='chrome',
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
        )
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 800},
            locale='pt-BR'
        )
        page = context.new_page()

        def on_response(response):
            try:
                ct = response.headers.get('content-type', '')
                if 'application/json' in ct:
                    url = response.url
                    if any(k in url for k in ['review', 'pdp_desktop', 'page_data', 'rating', 'feedback', 'comment']):
                        text = response.text()
                        data = json.loads(text)
                        intercepted_jsons.append({'url': url, 'data': data})
                        print(f"[API Intercepted] {url[:80]}... ({len(text)} chars)")
            except Exception:
                pass

        page.on('response', on_response)

        for pdp_url in pdp_urls:
            print(f"\n>>> Navigating: {pdp_url}")
            try:
                page.goto(pdp_url, wait_until='networkidle', timeout=25000)
            except Exception as e:
                print(f"Nav error / timeout: {e}")

            time.sleep(3)

            # Rolar suavemente para baixo para carregar componentes lazy
            page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            time.sleep(2)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)

            # Se for página de categoria, extrair links de outros aspiradores
            if '/c/' in pdp_url:
                cat_links = page.evaluate("""() => {
                    return Array.from(document.querySelectorAll('a[href*="/pdp/"]'))
                        .map(a => a.href)
                        .filter((v, i, arr) => arr.indexOf(v) === i);
                }""")
                print(f"Found {len(cat_links)} PDP links in category:")
                for cl in cat_links[:5]:
                    print("  Category PDP:", cl)
                continue

            # Tentar clicar no botão de "Ver todas as fotos" ou fotos de avaliações se houver
            try:
                btn_photos = page.locator("text='Ver todas as fotos'")
                if btn_photos.count() > 0:
                    print("Clicking 'Ver todas as fotos'...")
                    btn_photos.first.click(timeout=3000)
                    time.sleep(2)
            except Exception as e:
                print("Could not click 'Ver todas as fotos':", e)

            # Tentar clicar no filtro "Inclui imagens ou vídeos"
            try:
                filter_img = page.locator("text='Inclui imagens ou vídeos'")
                if filter_img.count() > 0:
                    print("Clicking 'Inclui imagens ou vídeos'...")
                    filter_img.first.click(timeout=3000)
                    time.sleep(2)
            except Exception as e:
                print("Could not click 'Inclui imagens ou vídeos':", e)

            # Extrair avaliações diretamente do DOM
            dom_reviews = page.evaluate("""() => {
                const results = [];
                // Procurar containers de avaliação
                const cards = document.querySelectorAll('[class*="review"], [class*="Review"], [class*="comment"]');
                
                // Extrair todos os elementos de comprador
                // No TikTok Shop padrão:
                const allElements = document.querySelectorAll('*');
                const verifiedBadges = Array.from(allElements).filter(el => el.innerText && el.innerText.trim() === 'Compras verificadas');
                
                verifiedBadges.forEach((badge, idx) => {
                    const parent = badge.closest('[class*="item"], [class*="card"], [class*="review"], [class*="wrap"], div') || badge.parentElement.parentElement;
                    if (!parent) return;

                    // Nome
                    const textLines = parent.innerText.split('\\n').map(t => t.trim()).filter(Boolean);
                    let name = 'Cliente';
                    for (let line of textLines) {
                        if (line.includes('*') && line.length < 25) {
                            name = line;
                            break;
                        }
                    }

                    // Avatar
                    const avatarImg = parent.querySelector('img[src*="tiktokcdn"], img[src*="avatar"]');
                    const avatarUrl = avatarImg ? avatarImg.src : null;

                    // Imagens da avaliação (ibyteimg)
                    const imgs = Array.from(parent.querySelectorAll('img'))
                        .map(i => i.src)
                        .filter(src => src.includes('ibyteimg.com') && !src.includes('avatar') && !src.includes('logo'));

                    // Comentário
                    let comment = '';
                    const p = parent.querySelector('p');
                    if (p) {
                        comment = p.innerText.trim();
                    } else {
                        // pegar linha longa
                        const longLines = textLines.filter(l => l.length > 15 && !l.includes('Compras') && !l.includes('Item:'));
                        if (longLines.length > 0) comment = longLines[0];
                    }

                    // Variação / Item
                    let variation = 'Padrão Bivolt';
                    const itemIdx = textLines.findIndex(l => l === 'Item:' || l.startsWith('Item:'));
                    if (itemIdx !== -1 && textLines[itemIdx + 1]) {
                        variation = textLines[itemIdx + 1];
                    }

                    // Data
                    let date = 'Recente';
                    const dateMatch = parent.innerText.match(/\\d{4}-\\d{2}-\\d{2}/) || parent.innerText.match(/\\d{2}\\/\\d{2}/);
                    if (dateMatch) date = dateMatch[0];

                    results.push({
                        name,
                        avatarUrl,
                        variation,
                        date,
                        comment,
                        photos: imgs,
                        rawText: textLines.slice(0, 10).join(' | ')
                    });
                });

                return results;
            }""")

            print(f"Extracted {len(dom_reviews)} review items from DOM on {pdp_url}")
            for r in dom_reviews:
                if len(r['photos']) > 0 or len(r['comment']) > 10:
                    all_reviews.append(r)

        browser.close()

    # Salvar dados interceptados
    with open("scripts/intercepted_tiktok_data.json", "w", encoding="utf-8") as f:
        json.dump(intercepted_jsons, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(intercepted_jsons)} intercepted JSON responses to scripts/intercepted_tiktok_data.json")

    # Salvar avaliações do DOM
    with open("scripts/dom_reviews_extracted.json", "w", encoding="utf-8") as f:
        json.dump(all_reviews, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_reviews)} reviews to scripts/dom_reviews_extracted.json")

if __name__ == '__main__':
    run()
