import os
from PIL import Image, ImageOps, ImageDraw, ImageFont

brain_dir = r"C:\Users\Dell\.gemini\antigravity\brain\626aa811-f9a0-4dad-af48-4ab6e56722e5"
p1_dir = r"c:\Users\Dell\Downloads\ds\img"
p2_dir = r"C:\Users\Dell\Downloads\stone_shop_clone\img"

def main():
    pack = Image.open(os.path.join(brain_dir, "pack_pure_final.jpg")).convert("RGB")
    diaper = Image.open(os.path.join(brain_dir, "diaper_pure.jpg")).convert("RGB")
    lenco = Image.open(os.path.join(brain_dir, "lenco_pure.jpg")).convert("RGB")

    # 1. Slide 1: Combo
    s1 = Image.new("RGB", (1000, 1000), (255, 255, 255))
    pack_res = pack.copy()
    pack_res.thumbnail((650, 650), Image.Resampling.LANCZOS)
    s1.paste(pack_res, (20, 40))
    lenco_res = lenco.copy()
    lenco_res.thumbnail((580, 580), Image.Resampling.LANCZOS)
    s1.paste(lenco_res, (400, 460))

    # 2. Slide 2: Pack
    s2 = Image.new("RGB", (1000, 1000), (255, 255, 255))
    pack_sq = ImageOps.fit(pack, (1000, 1000), Image.Resampling.LANCZOS, centering=(0.5, 0.4))
    s2.paste(pack_sq, (0, 0))

    # 3. Slide 3: Lenços
    s3 = Image.new("RGB", (1000, 1000), (255, 255, 255))
    lenco_sq = ImageOps.fit(lenco, (1000, 1000), Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    s3.paste(lenco_sq, (0, 0))

    # 4. Slide 4: Fralda
    s4 = Image.new("RGB", (1000, 1000), (255, 255, 255))
    diaper_sq = ImageOps.fit(diaper, (1000, 1000), Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    s4.paste(diaper_sq, (0, 0))

    # 5. Slide 5: Guia
    s5 = Image.new("RGB", (1000, 1000), (255, 255, 255))
    draw = ImageDraw.Draw(s5)
    draw.rectangle([(50, 50), (950, 160)], fill=(255, 43, 86))
    sizes = [
        {"tam": "M", "peso": "5,5 kg a 9,5 kg", "desc": "Ideal para bebês de 5 a 10 meses", "bg": (255, 245, 247)},
        {"tam": "G", "peso": "9 kg a 12,5 kg", "desc": "Ideal para bebês de 9 a 18 meses", "bg": (255, 255, 255)},
        {"tam": "XG", "peso": "12 kg a 15 kg", "desc": "Ideal para bebês de 18 a 24 meses", "bg": (255, 245, 247)},
        {"tam": "XXG", "peso": "Acima de 14 kg", "desc": "Ideal para bebês a partir de 2 anos", "bg": (255, 255, 255)}
    ]
    y = 200
    for s in sizes:
        draw.rectangle([(50, y), (950, y + 150)], fill=s["bg"], outline=(230, 230, 230), width=2)
        draw.ellipse([(80, y + 25), (180, y + 125)], fill=(255, 43, 86))
        y += 180

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_badge = ImageFont.truetype("arialbd.ttf", 46)
        font_peso = ImageFont.truetype("arialbd.ttf", 32)
        font_desc = ImageFont.truetype("arial.ttf", 24)
        font_footer = ImageFont.truetype("arialbd.ttf", 26)
    except:
        font_title = font_badge = font_peso = font_desc = font_footer = ImageFont.load_default()

    draw.text((500, 105), "GUIA DE TAMANHOS & PESO OFICIAL", fill=(255, 255, 255), font=font_title, anchor="mm")
    y = 200
    for s in sizes:
        draw.text((130, y + 75), s["tam"], fill=(255, 255, 255), font=font_badge, anchor="mm")
        draw.text((220, y + 50), f"Tamanho {s['tam']}: {s['peso']}", fill=(22, 24, 35), font=font_peso)
        draw.text((220, y + 95), s["desc"], fill=(138, 139, 145), font=font_desc)
        y += 180

    draw.rectangle([(50, 910), (950, 960)], fill=(245, 245, 245))
    draw.text((500, 935), "Até 12 horas de proteção anti-vazamento · Toque macio de algodão", fill=(100, 100, 100), font=font_footer, anchor="mm")

    slides = [s1, s2, s3, s4, s5]
    for idx, s in enumerate(slides, start=1):
        fname = f"fraldas-slide-{idx}.webp"
        s.save(os.path.join(p1_dir, fname), "WEBP", quality=92)
        s.save(os.path.join(p2_dir, fname), "WEBP", quality=92)
        print(f"Successfully saved {fname}")

    # Unboxing photos for customer reviews
    otaisa_1 = Image.open(os.path.join(brain_dir, "otaisa_1.jpeg")).convert("RGB")
    otaisa_1_sq = ImageOps.fit(otaisa_1, (800, 800), Image.Resampling.LANCZOS)
    
    adria_1 = Image.open(os.path.join(brain_dir, "tt_adria_1.jpeg")).convert("RGB")
    adria_1_sq = ImageOps.fit(adria_1, (800, 800), Image.Resampling.LANCZOS)
    
    cris_1 = Image.open(os.path.join(brain_dir, "cris_1.jpeg")).convert("RGB")
    cris_1_sq = ImageOps.fit(cris_1, (800, 800), Image.Resampling.LANCZOS)
    
    otaisa_9 = Image.open(os.path.join(brain_dir, "otaisa_9.jpeg")).convert("RGB")
    otaisa_9_sq = ImageOps.fit(otaisa_9, (800, 800), Image.Resampling.LANCZOS)

    rev_photos = [
        ("review-119-1.webp", otaisa_1_sq),
        ("review-119-2.webp", adria_1_sq),
        ("review-119-3.webp", cris_1_sq),
        ("review-119-4.webp", otaisa_9_sq)
    ]
    for fname, img in rev_photos:
        img.save(os.path.join(p1_dir, "reviews", fname), "WEBP", quality=88)
        img.save(os.path.join(p2_dir, "reviews", fname), "WEBP", quality=88)
        print(f"Saved unboxing photo {fname}")

    # Authentic TikTok review avatars for 119
    avt1 = Image.open(os.path.join(brain_dir, "avatar_otaisa_1.jpeg")).convert("RGB")
    avt2 = Image.open(os.path.join(brain_dir, "avatar_vanessa_1.jpeg")).convert("RGB")
    avt3 = Image.open(os.path.join(brain_dir, "tt_avatar_luna.jpeg")).convert("RGB")
    
    avatars_119 = [
        ("review-user-119-c1.jpg", avt1),
        ("review-user-119-c2.jpg", avt2),
        ("review-user-119-c3.jpg", avt3)
    ]
    for fname, img in avatars_119:
        img.save(os.path.join(p1_dir, "reviews-avatars", fname), "JPEG", quality=95)
        img.save(os.path.join(p2_dir, "reviews-avatars", fname), "JPEG", quality=95)
        print(f"Saved review avatar {fname}")

    # Authentic review avatars for 124
    avt_124_1 = Image.open(os.path.join(brain_dir, "avatar_otaisa_2.jpeg")).convert("RGB")
    avt_124_2 = Image.open(os.path.join(brain_dir, "avatar_vanessa_2.jpeg")).convert("RGB")
    
    avatars_124 = [
        ("review-user-124-c1.jpg", avt_124_1),
        ("review-user-124-mariana.jpg", avt_124_1),
        ("review-user-124-c2.jpg", avt_124_2),
        ("review-user-124-camila.jpg", avt_124_2)
    ]
    for fname, img in avatars_124:
        img.save(os.path.join(p1_dir, "reviews-avatars", fname), "JPEG", quality=95)
        img.save(os.path.join(p2_dir, "reviews-avatars", fname), "JPEG", quality=95)
        print(f"Saved review avatar {fname}")

if __name__ == "__main__":
    main()
