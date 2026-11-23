import urllib.request
import urllib.parse
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Referer': 'https://shopee.com.br/'
}

def search_and_get_reviews(keyword):
    print(f"\n================ Buscando: {keyword} ================")
    url = f"https://shopee.com.br/api/v4/search/search_items?by=relevancy&keyword={urllib.parse.quote(keyword)}&limit=10&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('items', [])
            print(f"Total produtos encontrados: {len(items)}")
            
            for it in items[:6]:
                basic = it.get('item_basic', {})
                itemid = basic.get('itemid')
                shopid = basic.get('shopid')
                name = basic.get('name')
                rating_star = basic.get('item_rating', {}).get('rating_star')
                print(f"\nProduto: {name} (itemid={itemid}, shopid={shopid}, rating={rating_star})")
                
                # Fetch ratings with photos (filter=1 or filter=3)
                # filter: 0=all, 1=with media, 2=with comments
                ratings_url = f"https://shopee.com.br/api/v2/item/get_ratings?filter=1&flag=1&itemid={itemid}&limit=10&offset=0&shopid={shopid}&type=0"
                r_req = urllib.request.Request(ratings_url, headers=headers)
                try:
                    with urllib.request.urlopen(r_req, timeout=12) as r_resp:
                        r_data = json.loads(r_resp.read().decode('utf-8'))
                        ratings = r_data.get('data', {}).get('ratings', [])
                        print(f"  Avaliações com fotos encontradas: {len(ratings)}")
                        for r in ratings:
                            author = r.get('author_username', 'Cliente')
                            masked_author = author[:1] + '**' + author[-1:] if len(author) > 2 else author + '**'
                            comment = r.get('comment', '').strip()
                            images = r.get('images', [])
                            product_items = r.get('product_items', [])
                            model_name = product_items[0].get('model_name', 'Padrão') if product_items else 'Padrão'
                            m_time = r.get('mtime', 0)
                            date_str = time.strftime('%d/%m', time.localtime(m_time)) if m_time else '05/11'
                            avatar = r.get('author_portrait', '')
                            
                            if images:
                                print(f"    [BUYER] {masked_author} | Var: {model_name} | Date: {date_str}")
                                print(f"      Comentário: {comment[:80]}...")
                                print(f"      Fotos ({len(images)}): {[f'https://down-br.img.susercontent.com/file/{img}' for img in images]}")
                                if avatar:
                                    print(f"      Avatar: https://down-br.img.susercontent.com/file/{avatar}")
                except Exception as re:
                    print(f"  Erro ao puxar ratings: {re}")
    except Exception as e:
        print("Erro na busca:", e)

if __name__ == '__main__':
    search_and_get_reviews("cinta modeladora feminina alta compressao")
    search_and_get_reviews("body modelador alta compressao efeito lipo")
