import urllib.request

url = "https://p16-common-sign.tiktokcdn.com/tos-alisg-i-photomode-sg/3b995ef339414a849424bc8a2d1c5e32~tplv-photomode-image.jpeg?dr=14555&x-expires=1795132800&x-signature=sBpVXxfebGRcghaWlH9GWm0TkAA%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=9b759fb9&idc=my2&ftpl=1"
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data = resp.read()

with open('temp_tiktok_photo1.jpg', 'wb') as f:
    f.write(data)
print("Baixado temp_tiktok_photo1.jpg com sucesso!", len(data), "bytes")
