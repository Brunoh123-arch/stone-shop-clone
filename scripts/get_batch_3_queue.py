import json, re

with open('js/catalogo.js', 'r', encoding='utf-8') as f:
    c = f.read()
items = re.findall(r'id:\s*(\d+),\s*nome:\s*[\'"](.*?)[\'"]', c)

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    vc = f.read()

m = re.search(r'const CREATOR_SETS\s*=\s*\{(.*?)\};', vc, re.DOTALL)
mapped_ids = set()
if m:
    for line in m.group(1).splitlines():
        line = line.strip()
        m_id = re.match(r'(\d+)\s*:', line)
        if m_id:
            mapped_ids.add(int(m_id.group(1)))

print(f'Total catalog products: {len(items)}')
print(f'Already mapped in CREATOR_SETS: {len(mapped_ids)}')

queue = []
for pid_str, name in items:
    pid = int(pid_str)
    if pid not in mapped_ids:
        queue.append((pid, name))

print(f'Queue remaining: {len(queue)}')
print('\nNext 10 for Batch 3:')
for pid, name in queue[:10]:
    print(f'  - ID {pid}: {name}')
