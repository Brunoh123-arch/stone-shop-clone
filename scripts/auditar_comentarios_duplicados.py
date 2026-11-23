import glob
import re
from collections import Counter

files = sorted(glob.glob("pages/produto-*.html"), key=lambda x: int(re.search(r'produto-(\d+)', x).group(1)))
all_comments = []
product_comments = {}

for f in files:
    pid = int(re.search(r'produto-(\d+)', f).group(1))
    with open(f, "r", encoding="utf-8") as fp:
        c = fp.read()
    comments = re.findall(r'<p class="review-comment">([^<]+)</p>', c)
    clean_comments = [c.strip() for c in comments if len(c.strip()) > 5]
    all_comments.extend(clean_comments)
    product_comments[pid] = clean_comments
    
    # Checar se no mesmo produto tem comentário repetido
    dupes_inside = [item for item, count in Counter(clean_comments).items() if count > 1]
    if dupes_inside:
        print(f"Produto {pid} tem {len(dupes_inside)} comentários repetidos DENTRO DELE MESMO: {dupes_inside[:2]}")

counts = Counter(all_comments)
dupes = {text: cnt for text, cnt in counts.items() if cnt > 1}
print(f"\nTotal de comentários únicos: {len(set(all_comments))} / Total geral: {len(all_comments)}")
print(f"Comentários repetidos entre produtos: {len(dupes)}")
for text, cnt in sorted(dupes.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  ({cnt}x): {text[:70]}...")
