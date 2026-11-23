import json, os, glob

sub_ids = [
    '39eb5aaf-c0f5-4b2e-b02e-39f8b28b8a1b',
    '9863e877-151b-4bef-9d8d-196e1fbe404f',
    'ad3ce293-a462-491d-8281-15dda2e4f40f',
    '01ad477f-4c11-4de5-b3f6-4041272af14f',
    '101f674b-1f1c-40a3-8caf-49ff711c0a3d'
]

for i, sid in enumerate(sub_ids, 1):
    path = f'C:/Users/Dell/.gemini/antigravity/brain/{sid}/.system_generated/logs/transcript.jsonl'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # find invoked workers
    import re
    invoked = re.findall(r'"conversationId":\s*"([a-f0-9\-]+)"', content)
    for wid in set(invoked):
        wpath = f'C:/Users/Dell/.gemini/antigravity/brain/{wid}/.system_generated/logs/transcript.jsonl'
        if os.path.exists(wpath):
            with open(wpath, 'r', encoding='utf-8') as wf:
                wlines = [l.strip() for l in wf if l.strip()]
            if wlines:
                wlast = json.loads(wlines[-1])
                print(f"Shard {i} Worker ({wid[:8]}): step {wlast.get('step_index')}, action: {wlast.get('tool_calls', [{}])[0].get('name') if wlast.get('tool_calls') else 'thinking'}")
