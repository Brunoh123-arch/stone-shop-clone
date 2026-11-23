import os, re, glob

with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

# Let's extract all datasets defined in videos-criadores.js and their lengths
dataset_counts = {}

# Find maps like const FOO_MAP = [ ... ];
map_matches = re.finditer(r'const\s+([A-Z0-9_]+_VIDEOS_MAP)\s*=\s*\[(.*?)\];', vc, re.DOTALL)
for m in map_matches:
    name = m.group(1)
    body = m.group(2)
    vids = re.findall(r'video:\s*["\']([^"\']+)["\']', body)
    dataset_counts[name] = len(vids)

# Also find direct CREATORS arrays if any
creator_matches = re.finditer(r'const\s+(CREATORS_[A-Z0-9_]+)\s*=\s*\[(.*?)\];', vc, re.DOTALL)
for m in creator_matches:
    name = m.group(1)
    body = m.group(2)
    vids = re.findall(r'video:\s*["\']([^"\']+)["\']', body)
    dataset_counts[name] = len(vids)

# Also check mappings like CREATORS_FOO = FOO_MAP.map(...)
mapping_matches = re.finditer(r'const\s+(CREATORS_[A-Z0-9_]+)\s*=\s*([A-Z0-9_]+_VIDEOS_MAP)\.map', vc)
for m in mapping_matches:
    c_name = m.group(1)
    map_name = m.group(2)
    if map_name in dataset_counts:
        dataset_counts[c_name] = dataset_counts[map_name]

print(f"Total datasets indexed: {len(dataset_counts)}")

# Now let's parse switch (prodId)
switch_match = re.search(r'switch\s*\(\s*prodId\s*\)\s*\{(.*?)\n    \}', vc, re.DOTALL)
if not switch_match:
    print("Could not find switch (prodId) block!")
else:
    switch_body = switch_match.group(1)
    # find case X: ... break;
    cases = re.findall(r'case\s+(\d+)\s*:\s*(.*?)(?=case|\bdefault:|$)', switch_body, re.DOTALL)
    print(f"Total cases in switch (prodId): {len(cases)}")
    
    prod_video_count = {}
    for case_num_str, case_code in cases:
        pid = int(case_num_str)
        # find activeDataset = ...
        ad_match = re.search(r'activeDataset\s*=\s*([A-Za-z0-9_]+)', case_code)
        if ad_match:
            ds_name = ad_match.group(1)
            count = dataset_counts.get(ds_name, -1)
            prod_video_count[pid] = (ds_name, count)
        else:
            prod_video_count[pid] = ("NO_DATASET", 0)

    # Check all products 1..124 that exist in pages/
    all_prods = []
    for f in glob.glob("pages/produto-*.html"):
        pid = int(re.search(r'produto-(\d+)\.html', f).group(1))
        all_prods.append(pid)
    all_prods.sort()
    
    print("\n=== SUMMARY OF PRODUCTS BY VIDEO COUNT ===")
    zero_vids = []
    one_vid = []
    two_to_five = []
    thirty_plus = []
    not_in_switch = []
    
    for pid in all_prods:
        if pid not in prod_video_count:
            not_in_switch.append(pid)
        else:
            ds_name, cnt = prod_video_count[pid]
            if cnt == 0:
                zero_vids.append((pid, ds_name))
            elif cnt == 1:
                one_vid.append((pid, ds_name))
            elif 2 <= cnt < 30:
                two_to_five.append((pid, ds_name, cnt))
            elif cnt >= 30:
                thirty_plus.append((pid, ds_name, cnt))
            else:
                zero_vids.append((pid, f"{ds_name} (unknown cnt)"))
    
    print(f"\n[!] NOT IN SWITCH (prodId) ({len(not_in_switch)} products):")
    print(not_in_switch)
    
    print(f"\n[!] ZERO VIDEOS (0) ({len(zero_vids)} products):")
    for pid, ds in zero_vids:
        print(f"  P{pid}: {ds}")
        
    print(f"\n[!] EXACTLY 1 VIDEO (1) ({len(one_vid)} products):")
    for pid, ds in one_vid:
        print(f"  P{pid}: {ds}")
        
    print(f"\n[*] 2 TO 29 VIDEOS ({len(two_to_five)} products):")
    for pid, ds, cnt in two_to_five:
        print(f"  P{pid}: {ds} -> {cnt} videos")
        
    print(f"\n[+] 30+ VIDEOS ({len(thirty_plus)} products):")
    for pid, ds, cnt in thirty_plus:
        print(f"  P{pid}: {ds} -> {cnt} videos")
