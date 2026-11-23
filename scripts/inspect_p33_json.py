import json, os

if os.path.exists('scripts/p33_videos_result.json'):
    with open('scripts/p33_videos_result.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("p33_videos_result has", len(data), "items:")
    for i, d in enumerate(data):
        print(f"Item {i+1}: user={d['username']}, catbox={d.get('catbox')}, desc={d.get('desc')[:50]}")
else:
    print("p33_videos_result.json not found!")
