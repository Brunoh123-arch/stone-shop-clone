import json

data = json.load(open('audit_results.json', encoding='utf-8'))

# 1. Slider suspicious
slider_bad = [d for d in data if d['slider_suspicious']]
print(f"=== 1. SLIDER SUSPICIOUS / PRINTS DE VIDEO: {len(slider_bad)} ===")
for d in slider_bad:
    print(f"  P{d['pid']} ({d['title']}): {d['slider_suspicious']}")

# 2. Few reviews or few unbox photos
few_reviews = [d for d in data if d['review_cards_count'] < 10]
few_unbox = [d for d in data if d['unbox_photos_count'] < 10]
rev_suspicious = [d for d in data if d['rev_photo_suspicious']]

print(f"\n=== 2A. PRODUTOS COM MENOS DE 10 REVIEWS / APENAS 3 REVIEWS: {len(few_reviews)} ===")
for d in few_reviews:
    print(f"  P{d['pid']} ({d['title'][:35]}): {d['review_cards_count']} reviews ({d['unbox_photos_count']} unbox photos)")

print(f"\n=== 2B. PRODUTOS COM MENOS DE 10 FOTOS DE UNBOXING: {len(few_unbox)} / {len(data)} ===")
print(f"Lista de PIDs com < 10 fotos unbox: {[d['pid'] for d in few_unbox]}")

print(f"\n=== 2C. REVIEWS COM FRAMES/VIDEOS SUSPEITOS: {len(rev_suspicious)} ===")
for d in rev_suspicious:
    print(f"  P{d['pid']}: {d['rev_photo_suspicious']}")

# 3. Creators videos < 10
few_creators = [d for d in data if d['creators_vids'] < 10]
print(f"\n=== 3. PRODUTOS COM MENOS DE 10 VIDEOS DE CRIADORES NO CARROSSEL: {len(few_creators)} ===")
for d in few_creators:
    print(f"  P{d['pid']} ({d['title'][:30]}): {d['creators_vids']} videos (dataset: {d['creators_dataset']})")

# 4. Description video issues
bad_desc_video = [d for d in data if not d['has_desc_video'] or not d['desc_video_src'] or not d['has_video_wrapper']]
print(f"\n=== 4. VIDEO DESCRICAO AUSENTE/SEM SRC/SEM WRAPPER: {len(bad_desc_video)} ===")
for d in bad_desc_video:
    print(f"  P{d['pid']}: has_desc={d['has_desc_video']}, src={d['desc_video_src']}")
