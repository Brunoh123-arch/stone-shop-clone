import urllib.request, urllib.parse, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def search_shopee(keyword):
    print(f"=== Buscando: {keyword} ===")
    url = f"https://shopee.com.br/api/v4/search/search_items?by=relevancy&keyword={urllib.parse.quote(keyword)}&limit=5&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    req = urllib.request.Request(url, headers=headers)
    result_data = []
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('items', [])
            print(f"Items encontrados: {len(items)}")
            for i, it in enumerate(items[:3]):
                basic = it.get('item_basic', {})
                name = basic.get('name')
                cover = f"https://down-br.img.susercontent.com/file/{basic.get('image')}"
                imgs = [f"https://down-br.img.susercontent.com/file/{x}" for x in basic.get('images', [])]
                tiers = []
                for t in basic.get('tier_variations', []):
                    t_name = t.get('name')
                    opts = t.get('options', [])
                    t_imgs = [f"https://down-br.img.susercontent.com/file/{x}" for x in t.get('images', []) if x]
                    tiers.append({'name': t_name, 'options': opts, 'images': t_imgs})
                result_data.append({'name': name, 'cover': cover, 'images': imgs, 'tiers': tiers})
                print(f"[{i+1}] {name}")
                print(f"  Capa: {cover}")
                print(f"  Total fotos: {len(imgs)}")
    except Exception as e:
        print("Erro:", e)
    return result_data

if __name__ == '__main__':
    r1 = search_shopee('escova secadora 5 em 1 modeladora')
    r2 = search_shopee('modelador cachos automatico sem fio')
    with open('scripts/shopee_results.json', 'w', encoding='utf-8') as f:
        json.dump({'escova': r1, 'curler': r2}, f, indent=2, ensure_ascii=False)
    print("Salvo em scripts/shopee_results.json")
