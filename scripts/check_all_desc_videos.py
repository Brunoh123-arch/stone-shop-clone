import re
import glob
import urllib.request
import concurrent.futures

html_files = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'produto-(\d+)', x).group(1)))
print(f'Checking description videos across {len(html_files)} product pages...')

desc_videos = {}
for h in html_files:
    pid = int(re.search(r'produto-(\d+)', h).group(1))
    with open(h, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find video inside .product-video-block or with id="tt-product-video"
    m = re.findall(r'<video[^>]+src=["\']([^"\']+)["\']', content)
    if m:
        desc_videos[pid] = m[0]
    else:
        desc_videos[pid] = None

print(f'Products with description video: {len([k for k, v in desc_videos.items() if v])}')
print(f'Products without description video: {len([k for k, v in desc_videos.items() if not v])}')

# Check remote catbox URLs in description videos
catbox_desc = [(pid, url) for pid, url in desc_videos.items() if url and url.startswith('http')]
print(f'Total remote description videos: {len(catbox_desc)}')

def test_url(item):
    pid, u = item
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-10'})
        with urllib.request.urlopen(req, timeout=5) as r:
            cr = r.headers.get('Content-Range', '')
            cl = int(r.headers.get('Content-Length', '0'))
            if (r.status == 206 and cl > 0) or (r.status == 200 and cl > 0):
                return pid, u, True, cl, cr
            return pid, u, False, cl, cr
    except Exception as e:
        return pid, u, False, 0, str(e)

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=15) as ex:
    for fut in concurrent.futures.as_completed([ex.submit(test_url, item) for item in catbox_desc]):
        results.append(fut.result())

broken_desc = [r for r in results if not r[2]]
working_desc = [r for r in results if r[2]]

print(f'Working description videos: {len(working_desc)}')
print(f'Broken / 0-byte description videos: {len(broken_desc)}')

for pid, u, ok, cl, cr in broken_desc:
    print(f'  P{pid}: {u} (size={cl}, range={cr})')
