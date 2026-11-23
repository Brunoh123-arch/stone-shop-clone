import urllib.request
import os
import sys

def upload(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as f:
        data = f.read()

    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    parts = []
    parts.append(('--' + boundary + '\r\nContent-Disposition: form-data; name="reqtype"\r\n\r\nfileupload\r\n').encode('utf-8'))
    parts.append(('--' + boundary + '\r\nContent-Disposition: form-data; name="fileToUpload"; filename="' + filename + '"\r\nContent-Type: video/mp4\r\n\r\n').encode('utf-8'))
    parts.append(data)
    parts.append(('\r\n--' + boundary + '--\r\n').encode('utf-8'))
    payload = b''.join(parts)

    req = urllib.request.Request('https://catbox.moe/user/api.php', data=payload, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'multipart/form-data; boundary=' + boundary
    })

    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf-8').strip()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        res = upload(sys.argv[1])
        print('Uploaded:', res)
