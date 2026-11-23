import glob
import os

catbox_ids = [
    ('P04', 's313zy.mp4'),
    ('P05', 'a8zjrb.mp4'),
    ('P06', 'perlvk.mp4'),
    ('P07', '1ig8lo.mp4'),
    ('P08', 'k3u5ff.mp4'),
    ('P09', 'mr2lij.mp4'),
    ('P12', 'h5x3n6.mp4'),
    ('P13', 'h5x3n6.mp4'),
    ('P14', 'ibv6vn.mp4'),
    ('P15', 'qfampv.mp4'),
    ('P16', 'abwltl.mp4'),
    ('P17', '18m1t8.mp4'),
    ('P18', '18m1t8.mp4'),
    ('P19', '8octvc.mp4'),
    ('P20', '8oqszr.mp4'),
    ('P21', 'rs5lzn.mp4'),
    ('P22', 'ekswrf.mp4'),
    ('P23', '08kgk9.mp4'),
    ('P24', '3g9fcx.mp4'),
    ('P25', 'ncrzdr.mp4'),
]

files = glob.glob('scripts/*.py') + glob.glob('scripts/*.json') + glob.glob('scripts/*.js')
for p, vid in catbox_ids:
    found_in = []
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()
                if vid in content:
                    found_in.append(os.path.basename(f))
        except:
            pass
    print(f"{p} ({vid}): found in {found_in}")
