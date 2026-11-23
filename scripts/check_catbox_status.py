import json

with open("scripts/catbox_audit_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

details = data.get("details", {})
print(f"Total details: {len(details)}")

catbox_ids = [
    ('P04', 'https://files.catbox.moe/s313zy.mp4'),
    ('P05', 'https://files.catbox.moe/a8zjrb.mp4'),
    ('P06', 'https://files.catbox.moe/perlvk.mp4'),
    ('P07', 'https://files.catbox.moe/1ig8lo.mp4'),
    ('P08', 'https://files.catbox.moe/k3u5ff.mp4'),
    ('P09', 'https://files.catbox.moe/mr2lij.mp4'),
    ('P12', 'https://files.catbox.moe/h5x3n6.mp4'),
    ('P13', 'https://files.catbox.moe/h5x3n6.mp4'),
    ('P14', 'https://files.catbox.moe/ibv6vn.mp4'),
    ('P15', 'https://files.catbox.moe/qfampv.mp4'),
    ('P16', 'https://files.catbox.moe/abwltl.mp4'),
    ('P17', 'https://files.catbox.moe/18m1t8.mp4'),
    ('P18', 'https://files.catbox.moe/18m1t8.mp4'),
    ('P19', 'https://files.catbox.moe/8octvc.mp4'),
    ('P20', 'https://files.catbox.moe/8oqszr.mp4'),
    ('P21', 'https://files.catbox.moe/rs5lzn.mp4'),
    ('P22', 'https://files.catbox.moe/ekswrf.mp4'),
    ('P23', 'https://files.catbox.moe/08kgk9.mp4'),
    ('P24', 'https://files.catbox.moe/3g9fcx.mp4'),
    ('P25', 'https://files.catbox.moe/ncrzdr.mp4'),
]

for p, url in catbox_ids:
    if url in details:
        print(f"{p}: status={details[url].get('status')}, size={details[url].get('content_length')}, type={details[url].get('content_type')}")
    else:
        print(f"{p}: NOT in details")
