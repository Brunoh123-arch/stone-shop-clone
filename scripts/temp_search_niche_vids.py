import glob, re

print("=== CHECKING VIDEOS IN CODEBASE FOR NICHES ===")
keywords = {
    'aiwa': ['aiwa', 'bbs', 'aws'],
    'jbl': ['jbl', 'boombox'],
    'jantar': ['jantar', 'prato', 'oxford', 'ryo', 'porto'],
    'lava_seca': ['hisense', 'lava', 'midea', 'secadora'],
    'copos': ['copo', 'cristal', 'proper']
}

found = {k: [] for k in keywords}

for f in glob.glob("**/*.js", recursive=True) + glob.glob("**/*.html", recursive=True):
    if '.git' in f or 'node_modules' in f: continue
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    
    for k, words in keywords.items():
        for w in words:
            if w in c.lower():
                # find mp4 links in vicinity of this word
                matches = re.finditer(rf'.{{0,100}}{w}.{{0,100}}', c, re.IGNORECASE)
                for m in list(matches)[:3]:
                    # check if any mp4 in the block or nearby
                    pass

# Let's search all unique mp4 urls in js/videos-criadores.js and pages/
all_vids = {}
for f in glob.glob("pages/produto-*.html") + ["js/videos-criadores.js"]:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    vids = re.findall(r'https?://files\.catbox\.moe/[a-z0-9]+\.mp4', c)
    for v in vids:
        if v not in all_vids: all_vids[v] = []
        all_vids[v].append(f)

print(f"Total unique Catbox mp4s in repo: {len(all_vids)}")

# Let's see what videos are mapped to P8 (AIWA Partybox)
with open("js/videos-criadores.js", "r", encoding="utf-8") as fp:
    vc = fp.read()

for p in [8, 4, 35, 76, 82, 98, 50, 7]:
    m = re.search(r'case\s+' + str(p) + r'\s*:\s*(.*?)(?=case|\bdefault:|$)', vc, re.DOTALL)
    if m:
        print(f"Case {p}: {m.group(1).strip()[:100]}")
