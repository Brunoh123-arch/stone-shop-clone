import glob
import re
import os

TT_AVATARS = [f"../img/reviews-avatars/tiktok_real/{f}" for f in sorted(os.listdir("img/reviews-avatars/tiktok_real")) if f.endswith(".jpg")]
print(f"Total de avatares reais do TikTok CDN prontos para uso: {len(TT_AVATARS)}")

def run():
    # 1. Atualizar produto-35.html
    with open("pages/produto-35.html", "r", encoding="utf-8") as f:
        p35 = f.read()

    tt_idx = 0
    def rep_avatar_tt(match):
        nonlocal tt_idx
        av = TT_AVATARS[tt_idx % len(TT_AVATARS)]
        tt_idx += 1
        return f'<div class="review-avatar"><img loading="lazy" decoding="async" src="{av}" alt="Cliente">'

    p35 = re.sub(r'<div class="review-avatar"><img[^>]*src="[^"]*"[^>]*>', rep_avatar_tt, p35)

    with open("pages/produto-35.html", "w", encoding="utf-8") as f:
        f.write(p35)
    print(f"P35: Todas as {tt_idx} avaliações agora usam 100% avatares reais do TikTok CDN!")

    # 2. Distribuir nos produtos principais
    few_ids = [14, 15, 20, 21, 22, 56, 74, 96, 97, 98, 99, 100, 101, 102, 103, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 118, 120, 124]

    for pid in few_ids:
        fpath = f"pages/produto-{pid}.html"
        with open(fpath, "r", encoding="utf-8") as f:
            html = f.read()
            
        local_idx = pid * 3
        def rep_card_avatar(match):
            nonlocal local_idx
            av = TT_AVATARS[local_idx % len(TT_AVATARS)]
            local_idx += 1
            return f'<div class="review-avatar"><img loading="lazy" decoding="async" src="{av}" alt="Cliente">'
            
        html = re.sub(r'<div class="review-avatar"><img[^>]*src="[^"]*"[^>]*>', rep_card_avatar, html)
        
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
            
    print("Avatares reais do TikTok distribuídos com sucesso nos produtos principais!")

if __name__ == "__main__":
    run()
