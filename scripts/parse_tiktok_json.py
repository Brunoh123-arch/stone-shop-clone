import json
import re

with open('scripts/temp_script_9.txt', 'r', encoding='utf-8') as f:
    content = f.read()

print('Length:', len(content))
print('Prefix:', content[:150])

# Search for review keys
review_matches = re.findall(r'"([a-zA-Z0-9_]*review[a-zA-Z0-9_]*)"', content, re.IGNORECASE)
print('Review keys found:', set(review_matches))

# Let's search for image urls inside temp_script_9.txt
imgs = re.findall(r'https://[^"\'\s]+ibyteimg\.com/[^"\'\s]+', content)
print(f'Total ibyteimg URLs in script 9: {len(imgs)}')
unique_imgs = list(dict.fromkeys(imgs))
print(f'Unique ibyteimg URLs: {len(unique_imgs)}')
for im in unique_imgs[:15]:
    print('  IMG:', im)

# Let's search for reviewer or comment or rating structures
# Look for json objects containing "comment" or "content" or "feedback"
comments = re.findall(r'"(comment|content|feedback|text)":\s*"([^"]{10,200})"', content)
print(f'Found {len(comments)} comment matches:')
for c in comments[:10]:
    print('  ', c)
