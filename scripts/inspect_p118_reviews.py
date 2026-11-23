txt = open('pages/produto-118.html', encoding='utf-8').read()
import re
reviews_block = re.search(r'(<div class="reviews-section"[\s\S]*?)(<div class="faq-section"|<div class="footer"|<footer|$)', txt)
if reviews_block:
    print(reviews_block.group(1)[:2000])
else:
    print("Section not found by regex")
