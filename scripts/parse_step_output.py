with open(r'C:\Users\Dell\.gemini\antigravity\brain\626aa811-f9a0-4dad-af48-4ab6e56722e5\.system_generated\steps\34379\output.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
urls = re.findall(r'"(https?://[^"]+)"', text)
print(f"Total de URLs: {len(urls)}")
review_imgs = [u for u in set(urls) if any(k in u for k in ['-O.', '-F.', 'D_NQ_NP_2X', 'D_NQ_NP']) and not any(x in u for x in ['cockade', 'star', 'logo', 'profile'])]
print(f"Total review images: {len(review_imgs)}")
for u in sorted(review_imgs)[:25]:
    print(" ", u)
