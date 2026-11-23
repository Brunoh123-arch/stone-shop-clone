import os, glob, re

pages = glob.glob('pages/produto-*.html')

data = []
for p in pages:
    pid = int(re.search(r'produto-(\d+)\.html', p).group(1))
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Title
    tm = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE)
    title = tm.group(1).replace(' - Stone Shop', '').strip() if tm else 'No Title'
    
    # Video in description
    m = re.search(r'<video[^>]+id=["\']tt-product-video["\'][^>]*src=["\']([^"\']+)["\']', c)
    if not m:
        m = re.search(r'<video[^>]*src=["\']([^"\']+)["\'][^>]+id=["\']tt-product-video["\']', c)
    if not m:
        m = re.search(r'class=["\']tiktok-video-card["\'].*?<video[^>]*src=["\']([^"\']+)["\']', c, re.DOTALL)
    
    src = m.group(1) if m else None
    if src:
        data.append({'pid': pid, 'title': title, 'src': src})

print(f"{'PID':<4} | {'Src':<35} | {'Title'}")
print("-" * 80)
for d in sorted(data, key=lambda x: x['pid']):
    print(f"{d['pid']:<4} | {d['src']:<35} | {d['title'][:40]}")
