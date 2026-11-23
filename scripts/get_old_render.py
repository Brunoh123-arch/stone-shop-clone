import json

path = r'C:\Users\Dell\.gemini\antigravity\brain\40253795-724e-4836-a8ee-923b78213fd5\.system_generated\logs\transcript_full.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'function renderStoreReviewsFilter' in line:
            data = json.loads(line)
            calls = data.get('tool_calls', [])
            for c in calls:
                arg = c.get('args', {})
                rc = arg.get('ReplacementContent', '')
                if 'function renderStoreReviewsFilter' in rc:
                    idx = rc.find('function renderStoreReviewsFilter')
                    with open('scripts/extracted_old_render.js', 'w', encoding='utf-8') as out:
                        out.write(rc[idx:idx+3500])
                    print("WROTE scripts/extracted_old_render.js")
                    break
