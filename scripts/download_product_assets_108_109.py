import urllib.request
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def download_img(url, dest):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) > 3000:
                with open(dest, 'wb') as f:
                    f.write(data)
                print(f"[OK] Saved {dest} ({len(data)} bytes)")
                return True
    except Exception as e:
        print(f"[ERROR] Error {dest}: {e}")
    return False

# Imagens Escova 5 em 1
escova_urls = [
    ("img/produto-108-1.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%2Fid%2FOIP.PYwW2KYiN-Ck4RhdWRJL_AHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=58bd40d718b7b9cc38b6e68994cf692d412411a5ac98d12a36f7863e17ec3956&ipo=images"),
    ("img/produto-108-2.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%2Fid%2FOIP.ZwlMKhN_2qaSJxDdXWesPAHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=819c5f1dadf0cf2209f74ad6dfd9701e57ad7f1faf76a852179d311fde443894&ipo=images"),
    ("img/produto-108-3.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.NmHm41x_l8L-dQymZV6iBwHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=b95c7ed25ed80cf0a9faad8070518547c122af6d753e00ab15988fc099fc0b40&ipo=images"),
    ("img/produto-108-4.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%2Fid%2FOIP._h1DogSKwWuiZtA9OLM2pAHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=918c113e76d80158eb19b6d3530c3a3d53d7d434320fd5b31526fda66ed47b1e&ipo=images"),
    ("img/produto-108-5.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%2Fid%2FOIP.zah1i583q_kt2_kZPhAa2gHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=5be950f3428153e913a873354546bdbebb11499c8ad193a405b222d0ff15d374&ipo=images"),
    ("img/review-108-1.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%2Fid%2FOIP.N07VtRAdvS2VTya31mG6AwHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=7f1482872c06e66fe2d25f796d390562823c4573340cd32b82af24b6b4605c56&ipo=images"),
    ("img/review-108-2.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%2Fid%2FOIP.e5ZiJEjrAuRPor03DTIP5AHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=6d2161acdb02090cb014e1c713b755ac5b395d4d92b0bc2f163b8d3e826dc9ae&ipo=images"),
    ("img/review-108-3.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%2Fid%2FOIP.6ND7JUKByXAwHt7hEdZA7QHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=e435011e3bfe04b8c48b0f9e33305dfe439d47690d6a57b82df994acd89071e7&ipo=images"),
]

# Imagens Modelador de Cachos
curler_urls = [
    ("img/produto-109-1.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.gADzX5E4JJoyTUyPF2ePlAHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=6cf02e3e9fc5a2810972321603f736a6bccc732a7e72768ff4b009ac7f1bb423&ipo=images"),
    ("img/produto-109-2.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP._GBq9ZUyqWvJ-9AOIPwq6QHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=0378631a85a34978971e0e2e8c377bea3793b3c9c3cc8d9e589d6ee4bf853155&ipo=images"),
    ("img/produto-109-3.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%2Fid%2FOIP.Xk3Icf0m5_t8nSrPIy6WVAHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=1babcfb62ec91b3531548251fc52521e74908892c81fb5d5d44a42ecc4fff09b&ipo=images"),
    ("img/produto-109-4.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.ySWRQsokWQ7e9y8u9-A3kQHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=f7354a68e1f9bd5cc8ed9ad77db07835453e7edcf1bd5a05f5b52496a0633a94&ipo=images"),
    ("img/produto-109-5.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%2Fid%2FOIP._Bk0Lmd2nrbzlFkl0yHEawHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=3b7971c2682836891e9a624c77fefabb83a7a9cf14cf3bec34e3642648080de9&ipo=images"),
    ("img/review-109-1.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.sClm6Ff4xcPP775BAxcUaQHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=91460181435ec8f45d6e2acf694edbbaaf8e3c56edeefc841977d2cf1ca02f25&ipo=images"),
    ("img/review-109-2.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%2Fid%2FOIP.J8JzpGz0CiLVJ03QRiJX8gHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=7d4bc5026755650e7001fd5d85ba7aca0d131bca387a4134963591af99bcecdb&ipo=images"),
    ("img/review-109-3.jpg", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%2Fid%2FOIP.D-dVPObaCl4ssavrEhthNQHaHa%3Fr%3D0%26pid%3DApi&f=1&ipt=e1509cef3f2ba5c7dfb3a1a4f9aa231a92cf329afc562a46f3277b54cbc889a7&ipo=images"),
]

for dest, url in escova_urls + curler_urls:
    download_img(url, dest)
