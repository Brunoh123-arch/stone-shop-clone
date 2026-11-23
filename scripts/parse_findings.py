import re
import json

with open('scripts/pdf_extracted.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern for product entries: P<num> · <title>
entries = re.split(r'\n(?=P\d+\s*·)', text)
print(f'Total product entries found: {len(entries) - 1}')

findings = []
for entry in entries[1:]:
    lines = entry.strip().split('\n')
    title_line = lines[0]
    p_num = re.match(r'P(\d+)', title_line).group(1)
    
    # Extract findings summary
    full_entry = '\n'.join(lines)
    findings.append({
        'prod_id': int(p_num),
        'title': title_line,
        'details': full_entry
    })

findings.sort(key=lambda x: x['prod_id'])
print(f'Parsed {len(findings)} products.')

# Save to json for analysis
with open('scripts/pdf_parsed_findings.json', 'w', encoding='utf-8') as f:
    json.dump(findings, f, ensure_ascii=False, indent=2)

print('Sample findings:')
for f in findings[:5]:
    print(f['prod_id'], f['title'])
    for line in f['details'].split('\n')[1:6]:
        print('  ', line)
