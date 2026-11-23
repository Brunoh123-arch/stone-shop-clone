import urllib.request
import re

url = 'https://stoneshopclone.vercel.app/pages/produto-104.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        print(f"Bytes recebidos de {url}: {len(html)}")
        
        # Procurar nomes e avatares
        cards = html.split('class="review-card"')
        print(f"Total cards remotos: {len(cards)-1}")
        for idx, c in enumerate(cards[1:], 1):
            m_name = re.search(r'class="review-user-name">([^<]+)<', c)
            m_img = re.search(r'<img[^>]+src="([^"]+)"', c)
            m_comm = re.search(r'class="review-comment">([^<]+)<', c)
            
            name = m_name.group(1).strip() if m_name else 'N/A'
            img = m_img.group(1).strip() if m_img else 'N/A'
            comm = m_comm.group(1).strip() if m_comm else 'N/A'
            
            print(f"Card #{idx:02d}: {name:<12} | {img} | {comm[:60]}")
except Exception as e:
    print("Erro:", e)
