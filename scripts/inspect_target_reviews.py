import re
import json

pids = [14, 114, 118, 119, 120, 121, 122, 123]

for pid in pids:
    path = f"pages/produto-{pid}.html"
    txt = open(path, encoding='utf-8').read()
    
    # get variations from PRODUTO_ATUAL
    m_prod = re.search(r'window\.PRODUTO_ATUAL\s*=\s*(\{[\s\S]*?\n\s*\});', txt)
    prod_block = m_prod.group(1) if m_prod else "N/A"
    
    # get existing reviews
    cards = re.findall(r'<div class="review-card"([\s\S]*?)</div>\s*</div>\s*(?:<div class="review-photos"[\s\S]*?</div>)?\s*<div class="review-comment">([\s\S]*?)</div>', txt)
    
    print(f"=== PRODUTO {pid} ===")
    print(f"Existing reviews count: {len(re.findall(r'class=\"review-card', txt))}")
    # find all data-author-variation
    vars_found = set(re.findall(r'data-author-variation="([^"]*)"', txt))
    print(f"Variations in reviews: {vars_found}")
