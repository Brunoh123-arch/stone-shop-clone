import re

for pid in [7, 35, 76, 82, 98]:
    fpath = f"pages/produto-{pid}.html"
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()
    
    title = re.search(r'<title>(.*?)</title>', c)
    desc_vid = re.search(r'<video[^>]*id=["\']tt-product-video["\'][^>]*src=["\']([^"\']+)["\']', c)
    if not desc_vid:
        desc_vid = re.search(r'<video[^>]*src=["\']([^"\']+)["\']', c)
    
    all_vids = re.findall(r'https?://[^\s"\'<>]+\.mp4', c)
    images = re.findall(r'(\.\./img/[^\s"\'<>]+\.(?:jpg|png|webp))', c)
    
    print(f"=== P{pid}: {title.group(1) if title else 'Sem título'} ===")
    print("  Desc video:", desc_vid.group(1) if desc_vid else "NENHUM")
    print("  All mp4s in HTML:", all_vids)
    print("  Sample images:", list(set(images))[:4])
