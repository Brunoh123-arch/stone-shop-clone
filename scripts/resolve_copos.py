import urllib.request

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFrWN4G8TNe3o9VyfsyVD1Vo9upLHgYeDnVKklP8myX-XQb39WMFnySS_4spIGfjLbsYuGj4a2xfAT2KZRTl6YgxxJwMtvILxutPR3Ghu7-tZoY9TnNaRhVG3cTUzt3fzXiBpnr1wio__N0zk70Ll5pDayCW-5-v9G2I40tommw9MuChCtV2PS61s0-luwCXfezJHaAyIwvGyGyrTEqwe8crRw="

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print("Final URL:", resp.geturl())
except Exception as e:
    print("Error:", e)
