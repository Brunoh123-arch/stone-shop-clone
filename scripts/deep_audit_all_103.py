import glob
import re
import os
import json

pages = sorted(glob.glob('pages/produto-*.html'), key=lambda p: int(re.search(r'produto-(\d+)\.html', p).group(1)))

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# 1. Parse dataset sizes from js/videos-criadores.js
dataset_sizes = {}
for m in re.finditer(r'const\s+([A-Za-z0-9_]+)\s*=\s*\[([\s\S]*?)\];', js_content):
    name = m.group(1)
    body = m.group(2)
    # Count items by { username: or { name: or { video: or strings
    items = re.findall(r'\{\s*(?:name|username|video):', body)
    if not items:
        items = re.findall(r'https?://[^\s,"\'<>]+', body)
    if items:
        dataset_sizes[name] = len(items)

# Maps / aliases
for m in re.finditer(r'const\s+([A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9_]+)\.map', js_content):
    t, s = m.group(1), m.group(2)
    if s in dataset_sizes: dataset_sizes[t] = dataset_sizes[s]

for m in re.finditer(r'const\s+([A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9_]+);', js_content):
    t, s = m.group(1), m.group(2)
    if s in dataset_sizes: dataset_sizes[t] = dataset_sizes[s]

# Switch cases
case_dataset_map = {}
switch_match = re.search(r'switch\s*\(prodId\)\s*\{([\s\S]*?default:[\s\S]*?)\}', js_content)
switch_code = switch_match.group(1) if switch_match else ""

current_cases = []
for line in switch_code.split('\n'):
    m_case = re.search(r'case\s+[\'"]?(\d+)[\'"]?\s*:', line)
    if m_case:
        current_cases.append(int(m_case.group(1)))
    m_ds = re.search(r'activeDataset\s*=\s*(?:buildNichePool\s*\(\s*)?([A-Za-z0-9_]+)', line)
    if m_ds:
        ds_name = m_ds.group(1)
        for c in current_cases:
            case_dataset_map[c] = ds_name
        current_cases = []

results = []

for p in pages:
    pid = int(re.search(r'produto-(\d+)\.html', p).group(1))
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # Title
    t_m = re.search(r'<title>(.*?)</title>', html)
    title = t_m.group(1).replace(' - Stone Shop', '').strip() if t_m else f"Produto {pid}"

    # --- CRITERION 1: SLIDER IMAGES ---
    # Find slider track images
    track_m = re.search(r'<div class=[\'"]slider-track[\'"]>([\s\S]*?)</div>\s*<div class=[\'"]slider-counter', html)
    slider_imgs = []
    if track_m:
        slider_imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', track_m.group(1))
    else:
        slider_imgs = re.findall(r'<img[^>]+class=[\'"][^\'"]*slider-img[^\'"]*[\'"][^>]+src=[\'"]([^\'"]+)[\'"]', html)

    # Check for creator video frames or bad images in slider
    # Signs of video frames: 'review', 'criador', 'creator', 'temp_', 'poster', 'frame', 'vid', or known cut images
    slider_suspicious = []
    for s in slider_imgs:
        sl = s.lower()
        if any(k in sl for k in ['review', 'criador', 'creator', 'temp_', 'poster', 'frame', 'vid']):
            slider_suspicious.append(s)
    # Special check for p121 and products with video frames in slider
    if pid == 121:
        slider_suspicious.append("travesseiro-slide-*.webp (marcado pelo usuário como frames de vídeo)")

    # --- CRITERION 2: REVIEWS & UNBOXING PHOTOS ---
    rev_start = -1
    for marker in ['class="reviews-section"', "class='reviews-section'", 'id="customer-reviews"', 'id="avaliacoes"']:
        pos = html.find(marker)
        if pos != -1:
            rev_start = pos
            break
    
    rev_html = html[rev_start:] if rev_start != -1 else html
    for end_m in ['<script', '<footer', 'class="bottom-bar"']:
        pos = rev_html.find(end_m)
        if pos != -1: rev_html = rev_html[:pos]

    cards = re.split(r'<div[^>]*class=[\'"]review-card[\'"]', rev_html)
    review_cards_count = len(cards) - 1 if len(cards) > 1 else 0

    rev_photos = []
    rev_photo_suspicious = []
    for card in cards[1:]:
        imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', card)
        for img in imgs:
            il = img.lower()
            if any(k in il for k in ['avatar', 'star', 'estrela', 'icon', 'logo', 'badge', 'check', 'arrow', 'bandeira']):
                continue
            rev_photos.append(img)
            if any(k in il for k in ['vid', 'creator', 'poster', 'frame']):
                rev_photo_suspicious.append(img)

    # Products that have only 3 reviews with 3 or 4 photos (like 118-123)
    has_few_reviews = review_cards_count < 10
    has_few_unbox = len(rev_photos) < 10

    # --- CRITERION 3: CREATORS VIDEOS (< 10) ---
    ds_name = case_dataset_map.get(pid, 'DEFAULT')
    vids_count = dataset_sizes.get(ds_name, 0)
    has_few_creators = vids_count < 10

    # --- CRITERION 4: DESCRIPTION VIDEO & PLAY CLICK ---
    has_desc_video = 'tt-product-video' in html
    desc_video_src_match = re.search(r'<video[^>]+id=[\'"]tt-product-video[\'"][^>]+src=[\'"]([^\'"]+)[\'"]', html)
    desc_video_src = desc_video_src_match.group(1) if desc_video_src_match else ""
    # Check if video has play button / wrapper
    has_video_wrapper = 'tt-product-video-wrapper' in html
    has_play_btn = 'tt-btn-play' in html

    results.append({
        'pid': pid,
        'title': title,
        'slider_count': len(slider_imgs),
        'slider_suspicious': slider_suspicious,
        'review_cards_count': review_cards_count,
        'unbox_photos_count': len(rev_photos),
        'rev_photo_suspicious': rev_photo_suspicious,
        'creators_vids': vids_count,
        'creators_dataset': ds_name,
        'has_desc_video': has_desc_video,
        'desc_video_src': desc_video_src,
        'has_video_wrapper': has_video_wrapper,
        'has_play_btn': has_play_btn
    })

with open('audit_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Audit completed for {len(results)} products. Saved to audit_results.json.")
