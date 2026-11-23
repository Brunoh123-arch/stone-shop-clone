import urllib.request
import urllib.parse

url = "https://www.google.com/aclk?sa=L&ai=DChsSEwitx8izxJCYAxUEWUgAHU1EDssYACICCAEQDRoCY2U&co=1&agsac=PtJ_7h1ZB-8&gclid=Cj0KCQiAk_DXBhCoARIsAHE-omPY0NrnaJY5TLEgRCLNdMdC5ARTq0CirWGF6_Y-CLfan9tunR39bjUaAp6TEALw_wcB&cid=CAASwALkaEY3fCqwxqYrB3kWQC9JerDwLAP59a9JdrSvIVXrcmekt02Cyjc1GttT06xmvYS0qzyU2jqJJe4IlI6zxujIEK_K2QeEBtdjaAgGgqbofL4pqNX_nnblxIu7dmdRtLlhbvdQNFhTjJoVby9PJwYNcFpKEZngHjLRU04Lv7HF4K4HC0HdmRBG-W-xF6L8X3-NcIsXoE6p-AbOXsSW8YO0zi6m0zKbx1QvFqryf6nIm70idbihp4UZtPIlqZTggcwLDS1K_nyvQXyYaKeh0-w8Fu035Q_nFW76Z1v53ZQq4oKdxAosSQJ1CGeeDLGi7OvVH2qnckhqlPGSlG3etjgNl8YnP_tTuE7p0LE-zVhXDs43Ux3Oadm7bt_32WHpgv2ZWayoxBBw9ydjU6YbGuUcFv_uCyR6fQB-PzKxwt2LZA&sig=AOD64_2lMhshq7wXesQbOpN2FNUodnbLCg&ctype=70&q=&ved=2ahUKEwie58KzxJCYAxUzO7kGHXwqOicQwg8oAHoECAoQBw&adurl="

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

req = urllib.request.Request(url, headers=headers)
try:
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
    resp = opener.open(req)
    print("Final URL:", resp.geturl())
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code, e.headers.get('Location'))
except Exception as e:
    print("Error:", e)
