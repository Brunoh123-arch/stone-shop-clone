import re
import json

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's inspect all CREATORS_* definitions
datasets = re.findall(r'(?:const|let|var)\s+(CREATORS_[A-Z0-9_]+)\s*=\s*(\[[^;]+\]);', c)
print(f"Found {len(datasets)} dataset array definitions")

for name, body in datasets:
    # count items
    vids = re.findall(r'video:\s*["\']([^"\']+)["\']', body)
    posters = re.findall(r'poster:\s*["\']([^"\']+)["\']', body)
    names = re.findall(r'name:\s*["\']([^"\']+)["\']', body)
    usernames = re.findall(r'username:\s*["\']([^"\']+)["\']', body)
    unique_vids = set(vids)
    print(f"{name}: {len(vids)} videos, {len(unique_vids)} unique videos, {len(posters)} posters")
