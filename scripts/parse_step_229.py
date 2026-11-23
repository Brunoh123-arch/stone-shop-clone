import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:/Users/Dell/.gemini/antigravity/brain/159cffd6-dd72-43b4-9cee-2b2d87e06523/.system_generated/steps/229/output.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove '### Result\n'
if text.startswith('### Result\n'):
    text = text[len('### Result\n'):]
idx = text.rfind('### Ran Playwright code')
if idx != -1:
    text = text[:idx].strip()

data = json.loads(text)
print("Title:", data.get('title'))
rd = data.get('reviewsData', {})
snippets = rd.get('reviewSnippets', [])
print(f"Total snippets: {len(snippets)}")
for i, s in enumerate(snippets):
    print(f"\n--- Snippet {i+1} ---")
    print(s)

print("\n--- ibyteImgs ---")
for img in rd.get('ibyteImgs', []):
    print(img)
