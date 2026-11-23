import os, re, glob

print("=== 1. AUDIT OF CREATORS SECTION IN HTML FILES ===")
html_files = sorted(glob.glob("pages/produto-*.html"), key=lambda x: int(re.search(r'\d+', x).group()))

missing_creators_section = []
wrong_position_creators = []
has_creators_section = []

for fpath in html_files:
    prod_id = int(re.search(r'produto-(\d+)\.html', fpath).group(1))
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()
    
    pos_prot = c.find('info-row-item-protection')
    pos_creat = c.find('creators-section')
    pos_rev = c.find('reviews-section')
    
    if pos_creat == -1:
        missing_creators_section.append((prod_id, fpath))
    else:
        has_creators_section.append((prod_id, fpath))
        if pos_prot != -1 and pos_rev != -1:
            if not (pos_prot < pos_creat < pos_rev):
                wrong_position_creators.append((prod_id, fpath, pos_prot, pos_creat, pos_rev))

print(f"Total HTML files: {len(html_files)}")
print(f"Has creators-section: {len(has_creators_section)}")
print(f"Missing creators-section: {len(missing_creators_section)}")
if missing_creators_section:
    print("Files missing creators-section:", [p[0] for p in missing_creators_section])

print(f"Wrong position creators: {len(wrong_position_creators)}")
if wrong_position_creators:
    for item in wrong_position_creators:
        print(f"P{item[0]}: prot={item[2]}, creat={item[3]}, rev={item[4]}")

print("\n=== 2. AUDIT OF VIDEOS-CRIADORES.JS ROUTING & VIDEO COUNTS ===")
with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc_content = f.read()

# Let's inspect getCreatorsForProduct or switch(prodId)
print("Length of videos-criadores.js:", len(vc_content))

# Let's check how getCreatorsForProduct or equivalent maps prodId
match = re.search(r'function getCreatorsForProduct\(.*?\)\s*\{(.*?)\n  \}', vc_content, re.DOTALL)
if match:
    fn_body = match.group(1)
    print("Found getCreatorsForProduct!")
else:
    # search for switch (prodId) or if (prodId
    print("Searching for prodId matching in videos-criadores.js:")
    for m in re.finditer(r'(switch\s*\([^\)]*prodId[^\)]*\)\s*\{|if\s*\([^\)]*prodId[^\)]*\))', vc_content):
        start = m.start()
        print(vc_content[start:start+200])
        print("---")
