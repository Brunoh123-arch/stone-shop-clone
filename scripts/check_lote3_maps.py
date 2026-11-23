# -*- coding: utf-8 -*-
import re

text = open('js/videos-criadores-v3.js', 'r', encoding='utf-8').read()
arrays = [
    'CREATORS_PAD11_52', 'PAD11_52_VIDEOS_MAP',
    'CREATORS_STARLINK_53', 'STARLINK_53_VIDEOS_MAP',
    'CREATORS_SWITCH_55', 'SWITCH_55_VIDEOS_MAP',
    'CREATORS_STARLINK_59', 'STARLINK_59_VIDEOS_MAP',
    'CREATORS_REDMI_WATCH_63', 'REDMI_WATCH_63_VIDEOS_MAP',
    'CREATORS_SOFA_SENSES_65', 'SOFA_SENSES_65_VIDEOS_MAP',
    'CREATORS_SPOTCLEANER_78', 'SPOTCLEANER_78_VIDEOS_MAP', 'WAP_EXTRATORA_78_VIDEOS_MAP',
    'CREATORS_SMART_TV_116', 'SMART_TV_116_VIDEOS_MAP'
]

for arr in arrays:
    m = re.search(r'const\s+' + arr + r'\s*=\s*([^;]+);', text)
    if m:
        val = m.group(1).strip()
        if len(val) > 80:
            val = val[:80] + '...'
        print(f"{arr} = {val}")
