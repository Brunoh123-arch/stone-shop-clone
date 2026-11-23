import urllib.request
import urllib.parse
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_ml_images(query):
    url = f"https://lista.mercadolivre.com.br/{urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        # Find item links
        links = list(set(re.findall(r'https://produto\.mercadolivre\.com\.br/MLB-[^\"]+', html)))
        print(f"ML '{query}': {len(links)} links")
        if links:
            item_url = links[0].split('?')[0]
            req_item = urllib.request.Request(item_url, headers=headers)
            with urllib.request.urlopen(req_item, timeout=10) as resp_item:
                html_item = resp_item.read().decode('utf-8', errors='ignore')
            # Extract high res images
            imgs = list(dict.fromkeys(re.findall(r'https://http2\.mlstatic\.com/D_NQ_NP_[^\"]+-O\.webp', html_item)))
            if not imgs:
                imgs = list(dict.fromkeys(re.findall(r'https://http2\.mlstatic\.com/D_NQ_NP_[^\"]+-F\.webp', html_item)))
            print(f"  Fotos encontradas: {len(imgs)}")
            return imgs
    except Exception as e:
        print(f"Erro ML {query}: {e}")
    return []

if __name__ == '__main__':
    ml_arcade = get_ml_images("dobe 7 in 1 arcade fighting stick")
    ml_comedouro = get_ml_images("comedouro duplo acrilico elevado gato")
    ml_patinho = get_ml_images("brinquedo patinhos escorregador montanha russa")
    ml_kappa = get_ml_images("tenis kappa pulse rx corrida")
    ml_projetor = get_ml_images("projetor natalino led usb 6 cenas")

    res = {
        '114_arcade': ml_arcade,
        '113_comedouro': ml_comedouro,
        '112_patinho': ml_patinho,
        '110_kappa': ml_kappa,
        '111_projetor': ml_projetor
    }
    with open('scripts/ml_clean_images.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2)
    print("Salvo em scripts/ml_clean_images.json")
