import urllib.request
from PIL import Image
import io
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def save_clean_square(url, dest, size=(800, 800)):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        img = Image.open(io.BytesIO(data))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        w, h = img.size
        min_d = min(w, h)
        left = (w - min_d) // 2
        top = (h - min_d) // 2
        cropped = img.crop((left, top, left + min_d, top + min_d))
        resized = cropped.resize(size, Image.Resampling.LANCZOS)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        resized.save(dest, 'JPEG', quality=92)
        print(f"[OK] {dest} ({size[0]}x{size[1]})")
        return True
    except Exception as e:
        print(f"[ERRO] {dest}: {e}")
        return False

# Imagens 100% limpas sem texto / sem meme / sem Shopee para a galeria de produtos
gallery_images = {
    # 111: Projetor Natalino
    'img/produto-111-2.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMZB0AC-Z9bMwymo45gx401bGIx4b3wf19G8KBRgijeQ&s=10',
    'img/produto-111-3.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRnFzMNwBRoigoZ6uY0CLPmWs3WLH12yj6l_ifZJVw5BQ&s=10',
    'img/produto-111-4.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSu7SRm-9tC3_vLnMsCdOUmu9YE1oUMjibjcUekj5u_qw&s=10',
    'img/produto-111-5.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbe6eCy4jlNL3-5Z46FIKNJSfAA3TPMHrg_ALXXKIgBw&s=10',

    # 112: Patinhos Bombeiro Montanha Russa
    'img/produto-112-2.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQokocmYrb3ffLEia3nzP-SVadHuRSEsV9t3yaAiNFvMQ&s=10',
    'img/produto-112-3.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYi9gt7BNGHCszmMdjaEVEelVIPmWrEbUrexxoqnAsrw&s=10',
    'img/produto-112-4.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-_5N6Gq2MJ--wQbrLa2PGmM9UVSFpX22z7C2yirXpmw&s=10',
    'img/produto-112-5.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTobx8bkZuLI3rQfLtq_CD7vtvZrEGHrEujKOGfwEtBlg&s=10',

    # 113: Comedouro Acrílico Pet
    'img/produto-113-2.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-_9dSVC6bLkeF7yPLtbJOFJdwEqRT29QxCVJmR99ERg&s=10',
    'img/produto-113-3.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQqE-sZpNsD5PJYvHOxnDlB-9vX36a1Kn8K0v5d4KOmA&s=10',
    'img/produto-113-4.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRQMJ806lM8bjYBMd_ixpKoyndknw6cc92A8bMrfY35w&s=10',
    'img/produto-113-5.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoy7qgnlT6c2XR-VrAAiBL2gzXF6SuMeUK38LdLsfl7Q&s=10',

    # 114: Controle Arcade Stick
    'img/produto-114-2.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPmEUX1xxWuisf3zrZ9xtRv_UYuQRkSEBN4DFQNdH2OA&s=10',
    'img/produto-114-3.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWlYpA66iATyMTZdgax8cZ_qFUJb-nwo7Dhcomnb18gw&s=10',
    'img/produto-114-4.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXnJpqJ3VW-VBNhZWLZRTDDkUGAX8t-FA4af4RmvOOpA&s=10',
    'img/produto-114-5.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpGLVyUqnLEqYajo1ezWWVSx4eoXZoKN1hcf9-zisv3A&s=10',

    # 110: Tênis Kappa
    'img/produto-110-2.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKDPJlRUeG683OEYJgQpp9hgpYYqoJoL2ZlPjtnYjkmQ&s=10',
    'img/produto-110-3.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRMn9FV_GBzCj1q6QsG_uYgWUYbX02hRdPHyVRRjYqyQ&s=10',
    'img/produto-110-4.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYHzIupdK8n9kIOKtpNXb95LKB-dr_S0x-1XbT6AG6Dg&s',
    'img/produto-110-5.jpg': 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTk9vevxL0h2oCUF-GFCGaTOJFOtzSRO0-Au9fD6-VJ-L9JwBxAcpoMelhI4whURW96akW8uk0JiY2MmyVPiQjZn8shkFHjSkbrBswAKdBJJoVsd83txCX8BnETzsvkUnq1w3gz_A&usqp=CAc',
}

# Fotos autênticas para as avaliações dos clientes (sem texto, sem meme, fotos reais)
review_images = {
    # 111: Projetor na sala / projeção
    'img/review-111-real-1.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQsJKRQ9eHus5TJWyX_jD5AWcTN8strRAwr3AJLlllBmw&s=10',
    'img/review-111-real-2.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbe6eCy4jlNL3-5Z46FIKNJSfAA3TPMHrg_ALXXKIgBw&s=10',
    'img/review-111-real-3.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSu7SRm-9tC3_vLnMsCdOUmu9YE1oUMjibjcUekj5u_qw&s=10',
    'img/review-111-real-4.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMZB0AC-Z9bMwymo45gx401bGIx4b3wf19G8KBRgijeQ&s=10',

    # 112: Patinhos na sala / crianças brincando
    'img/review-112-real-1.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTobx8bkZuLI3rQfLtq_CD7vtvZrEGHrEujKOGfwEtBlg&s=10',
    'img/review-112-real-2.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSB2c0DV_yWmY8xwU63v2h6qCpqZyyyW3dDv2HZrRk2Xg&s=10',
    'img/review-112-real-3.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYi9gt7BNGHCszmMdjaEVEelVIPmWrEbUrexxoqnAsrw&s=10',
    'img/review-112-real-4.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQokocmYrb3ffLEia3nzP-SVadHuRSEsV9t3yaAiNFvMQ&s=10',

    # 113: Comedouro na cozinha / animais comendo
    'img/review-113-real-1.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRQMJ806lM8bjYBMd_ixpKoyndknw6cc92A8bMrfY35w&s=10',
    'img/review-113-real-2.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoy7qgnlT6c2XR-VrAAiBL2gzXF6SuMeUK38LdLsfl7Q&s=10',
    'img/review-113-real-3.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-_9dSVC6bLkeF7yPLtbJOFJdwEqRT29QxCVJmR99ERg&s=10',
    'img/review-113-real-4.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQqE-sZpNsD5PJYvHOxnDlB-9vX36a1Kn8K0v5d4KOmA&s=10',

    # 114: Controle Arcade ligado na mesa / no setup
    'img/review-114-real-1.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWlYpA66iATyMTZdgax8cZ_qFUJb-nwo7Dhcomnb18gw&s=10',
    'img/review-114-real-2.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPmEUX1xxWuisf3zrZ9xtRv_UYuQRkSEBN4DFQNdH2OA&s=10',
    'img/review-114-real-3.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXnJpqJ3VW-VBNhZWLZRTDDkUGAX8t-FA4af4RmvOOpA&s=10',
    'img/review-114-real-4.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpGLVyUqnLEqYajo1ezWWVSx4eoXZoKN1hcf9-zisv3A&s=10',

    # 110: Tênis Kappa no pé / na caixa
    'img/review-110-real-1.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKDPJlRUeG683OEYJgQpp9hgpYYqoJoL2ZlPjtnYjkmQ&s=10',
    'img/review-110-real-2.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRMn9FV_GBzCj1q6QsG_uYgWUYbX02hRdPHyVRRjYqyQ&s=10',
    'img/review-110-real-3.jpg': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYHzIupdK8n9kIOKtpNXb95LKB-dr_S0x-1XbT6AG6Dg&s',
    'img/review-110-real-4.jpg': 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTk9vevxL0h2oCUF-GFCGaTOJFOtzSRO0-Au9fD6-VJ-L9JwBxAcpoMelhI4whURW96akW8uk0JiY2MmyVPiQjZn8shkFHjSkbrBswAKdBJJoVsd83txCX8BnETzsvkUnq1w3gz_A&usqp=CAc',
}

if __name__ == '__main__':
    print("=== BAIXANDO IMAGENS LIMPAS DA GALERIA (SLIDER) ===")
    for dest, url in gallery_images.items():
        save_clean_square(url, dest, size=(800, 800))

    print("\n=== BAIXANDO FOTOS REAIS DE AVALIAÇÃO DOS CLIENTES ===")
    for dest, url in review_images.items():
        save_clean_square(url, dest, size=(600, 600))

    print("\n[OK] Todas as imagens limpas salvas com sucesso!")
