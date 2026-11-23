# -*- coding: utf-8 -*-
"""
TIKTOK TO CATBOX PRO DOWNLOADER & UPLOADER - BRUNO CTO
Usa os cookies oficiais da sessão Max Digital do Profile 42 para
baixar os MP4 diretamente do TikTok CDN e subir para o Catbox.
"""

import sys
import os
import re
import json
import urllib.request
import urllib.parse

COOKIES = (
    'tt_chain_token=T0mPOmzCJn19h0AkhnKWjw==; '
    'sessionid=a174e267e59473125b7972eb0c421696; '
    'odin_tt=d53a1d0970e419f39b1246dd60489d4dbdbf1c3055487e473d2850874e9dd27b3f6853e4305bacd5e96b40a2479deaf2f4770cd5e776959c79a565129d4a3d0d2229eb37b909ae08b89a6de4f19de376; '
    'ttwid=1%7CG5LI_3P7aFYrRCav1o18Z0R5WW8fZv2OrA5TF2bg_R0%7C1795190393%7Caf18b7d29c56ef1c67e43fd98994e6bdc329eecb37b2c96947ce1e9330ae91f7; '
    '_ttp=3L3CCnYhlrZpgh63tBvmm3b7ZA2.1792673239554'
)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36',
    'Referer': 'https://www.tiktok.com/',
    'Cookie': COOKIES
}

def extract_video_info(video_url):
    req = urllib.request.Request(video_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        html = r.read().decode('utf-8', errors='ignore')

    m = re.search(r'id=["\']__UNIVERSAL_DATA_FOR_REHYDRATION__["\'][^>]*>(.*?)</script>', html)
    if not m:
        m2 = re.search(r'id=["\']SIGI_STATE__["\'][^>]*>(.*?)</script>', html)
        if m2:
            try:
                sigi = json.loads(m2.group(1))
                item_module = sigi.get('ItemModule', {})
                if item_module:
                    vid_key = list(item_module.keys())[0]
                    item = item_module[vid_key]
                    return {
                        'nickname': item.get('author', ''),
                        'username': item.get('author', ''),
                        'avatar': '',
                        'desc': item.get('desc', ''),
                        'playAddr': item.get('video', {}).get('playAddr', ''),
                        'cover': item.get('video', {}).get('cover', '')
                    }
            except Exception as e:
                print(f"[-] Erro SIGI: {e}")
        print(f"[-] Rehydration/SIGI nao achado! HTML length: {len(html)} | Title: {re.findall(r'<title>(.*?)</title>', html)}")
        return None

    try:
        data = json.loads(m.group(1))
        detail = data.get('__DEFAULT_SCOPE__', {}).get('webapp.video-detail', {})
        item = detail.get('itemInfo', {}).get('itemStruct', {})
        if not item:
            return None

        author = item.get('author', {})
        video = item.get('video', {})
        return {
            'nickname': author.get('nickname', ''),
            'username': author.get('uniqueId', ''),
            'avatar': author.get('avatarThumb', ''),
            'desc': item.get('desc', ''),
            'playAddr': video.get('playAddr', ''),
            'cover': video.get('cover', '')
        }
    except Exception as e:
        print(f"[-] Erro ao parsear JSON: {e}")
        return None

def download_and_upload_to_catbox(play_addr, filename):
    req = urllib.request.Request(play_addr, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        video_bytes = r.read()

    print(f"[*] Baixou {len(video_bytes)} bytes do TikTok CDN.")

    # Upload para o Catbox
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = bytearray()
    body.extend(f'--{boundary}\r\n'.encode('utf-8'))
    body.extend(b'Content-Disposition: form-data; name="reqtype"\r\n\r\n')
    body.extend(b'fileupload\r\n')

    body.extend(f'--{boundary}\r\n'.encode('utf-8'))
    body.extend(f'Content-Disposition: form-data; name="fileToUpload"; filename="{filename}"\r\n'.encode('utf-8'))
    body.extend(b'Content-Type: video/mp4\r\n\r\n')
    body.extend(video_bytes)
    body.extend(b'\r\n')
    body.extend(f'--{boundary}--\r\n'.encode('utf-8'))

    catbox_req = urllib.request.Request(
        'https://catbox.moe/user/api.php',
        data=bytes(body),
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Content-Type': f'multipart/form-data; boundary={boundary}'
        }
    )

    with urllib.request.urlopen(catbox_req, timeout=60) as r:
        catbox_url = r.read().decode('utf-8').strip()

    return catbox_url

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.tiktok.com/@mocadosperfumescba/video/7643502573189664007'
    print(f"[*] Testando com: {url}")
    info = extract_video_info(url)
    if not info:
        print("[-] Falha ao extrair info!")
        sys.exit(1)

    print(f"[+] Autor: {info['nickname']} (@{info['username']})")
    print(f"[+] Descrição: {info['desc'][:60]}...")
    print(f"[+] PlayAddr: {info['playAddr'][:80]}...")

    catbox = download_and_upload_to_catbox(info['playAddr'], f"{info['username']}.mp4")
    print(f"[+] CATBOX URL: {catbox}")
