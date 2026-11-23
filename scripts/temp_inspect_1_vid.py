import os, re, glob

# Let's inspect all products with their real active dataset lengths
with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

# Parse all case statements in switch (prodId)
switch_match = re.search(r'switch\s*\(\s*prodId\s*\)\s*\{(.*?)\n    \}', vc, re.DOTALL)
switch_body = switch_match.group(1)
cases = re.findall(r'case\s+(\d+)\s*:\s*(.*?)(?=case|\bdefault:|$)', switch_body, re.DOTALL)

prod_info = {}
for case_num_str, case_code in cases:
    pid = int(case_num_str)
    ad_match = re.search(r'activeDataset\s*=\s*([A-Za-z0-9_]+)', case_code)
    if ad_match:
        ds_name = ad_match.group(1)
        # Find where ds_name is defined
        # It could be: const ds_name = [ ... ];
        # Or: const ds_name = OTHER_MAP.map(...);
        p1 = vc.find(f"const {ds_name} =")
        if p1 != -1:
            p_end = vc.find(";\n", p1)
            ds_def = vc[p1:p_end]
            # Check if it has .map
            map_match = re.search(r'=\s*([A-Za-z0-9_]+)\.map', ds_def)
            if map_match:
                source_map = map_match.group(1)
                p_map = vc.find(f"const {source_map} =")
                p_map_end = vc.find(";\n", p_map)
                map_def = vc[p_map:p_map_end]
                vids = re.findall(r'https?://[^\s"\'<>]+\.mp4', map_def)
                prod_info[pid] = (ds_name, len(vids), vids)
            else:
                vids = re.findall(r'https?://[^\s"\'<>]+\.mp4', ds_def)
                prod_info[pid] = (ds_name, len(vids), vids)
        else:
            prod_info[pid] = (ds_name, 0, [])

# Get titles from HTML files
titles = {}
for f in glob.glob("pages/produto-*.html"):
    pid = int(re.search(r'produto-(\d+)\.html', f).group(1))
    with open(f, "r", encoding="utf-8") as fp:
        c = fp.read()
    t_match = re.search(r'<title>(.*?)</title>', c)
    titles[pid] = t_match.group(1).replace(" - Stone Shop", "") if t_match else "Sem título"

print("=== PRODUTOS COM 0 VÍDEOS ===")
for pid in sorted(prod_info.keys()):
    ds, cnt, vids = prod_info[pid]
    if cnt == 0 and pid not in [78, 79, 81, 83, 84]:
        print(f"P{pid}: {titles.get(pid, '')} | Dataset: {ds}")

print("\n=== PRODUTOS COM EXATAMENTE 1 VÍDEO ===")
one_vid_pids = []
for pid in sorted(prod_info.keys()):
    ds, cnt, vids = prod_info[pid]
    if cnt == 1:
        one_vid_pids.append(pid)
        print(f"P{pid}: {titles.get(pid, '')} | Video: {vids[0] if vids else 'N/A'}")

print(f"\nTotal com 1 vídeo: {len(one_vid_pids)}")
