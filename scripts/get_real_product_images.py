import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def get_ml_product_images(query):
    print(f"\n--- Buscando no Mercado Livre: {query} ---")
    url = f"https://lista.mercadolivre.com.br/{query}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            # Find item links
            item_links = list(set(re.findall(r'https://produto\.mercadolivre\.com\.br/MLB-[^\"]+', html)))
            print(f"Links de produtos encontrados: {len(item_links)}")
            if item_links:
                first_link = item_links[0]
                print(f"Acessando primeiro produto: {first_link}")
                req_prod = urllib.request.Request(first_link, headers=headers)
                with urllib.request.urlopen(req_prod) as resp_prod:
                    html_prod = resp_prod.read().decode('utf-8')
                    # Find high res images
                    hires_imgs = list(dict.fromkeys(re.findall(r'https://http2\.mlstatic\.com/D_NQ_NP_[^\"]+-O\.webp', html_prod)))
                    if not hires_imgs:
                        hires_imgs = list(dict.fromkeys(re.findall(r'https://http2\.mlstatic\.com/D_NQ_NP_[^\"]+-F\.webp', html_prod)))
                    print(f"Fotos de alta resolucao encontradas: {len(hires_imgs)}")
                    for img in hires_imgs[:8]:
                        print(" ", img)
                    return hires_imgs[:8]
    except Exception as e:
        print("Erro ML:", e)
    return []

if __name__ == '__main__':
    imgs_body = get_ml_product_images("body-modelador-cinta-alta-compressao-efeito-lipo")
    imgs_asp = get_ml_product_images("mini-aspirador-portatil-sem-fio-2-em-1-soprador")
