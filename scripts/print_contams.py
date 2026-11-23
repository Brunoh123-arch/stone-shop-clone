import re

targets = [100, 101, 102, 103, 107, 108, 109, 110, 111, 112, 114, 124, 14, 21, 74, 96, 97]

for pid in targets:
    fn = f'pages/produto-{pid}.html'
    c = open(fn, encoding='utf-8', errors='ignore').read()
    
    # We want to see from reviews-summary to the first valid review after contamination
    idx_summary = c.find('reviews-summary')
    if idx_summary == -1:
        print(f"P{pid}: NO reviews-summary")
        continue
    
    # Let's see the first 1500 chars after reviews-summary
    snippet = c[idx_summary:idx_summary+1500]
    print(f"==================== P{pid} ====================")
    print(snippet[:1200])
