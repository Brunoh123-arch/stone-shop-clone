import re

with open("pages/produto-35.html", "r", encoding="utf-8") as f:
    c = f.read()

avatars = re.findall(r'<div class="review-avatar"><img[^>]*src="([^"]+)"', c)
print(f"Total de avatares em P35: {len(avatars)}")
for av in avatars[:10]:
    print(" ", av)
