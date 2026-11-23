# -*- coding: utf-8 -*-
import urllib.request
import re

url = 'https://stoneshopclone.vercel.app/pages/produto-28'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as res:
    html = res.read().decode('utf-8')

print("Posters no HTML retornado pelo Vercel:")
posters = re.findall(r'poster=["\']([^"\']+)["\']', html)
for p in posters:
    print("  POSTER:", p)

videos = re.findall(r'src=["\']([^"\']+\.mp4[^"\']*)["\']', html)
for v in videos:
    print("  VIDEO:", v)

scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html)
for s in scripts:
    if 'video' in s or 'criador' in s:
        print("  SCRIPT:", s)
