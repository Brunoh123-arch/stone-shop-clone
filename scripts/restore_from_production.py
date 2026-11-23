import urllib.request
import os
import time

BASE_URL = "https://stoneshopclone.vercel.app/pages"

pids = list(range(1, 130))

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

success_count = 0
for pid in pids:
    filename = f"produto-{pid}.html"
    url = f"{BASE_URL}/{filename}"
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req)
        if resp.status == 200:
            content = resp.read()
            # Verify valid HTML
            if b'<html' in content and len(content) > 300:
                out_path = os.path.join("pages", filename)
                with open(out_path, "wb") as f:
                    f.write(content)
                success_count += 1
                if success_count % 10 == 0:
                    print(f"Restored {success_count} files...")
    except Exception as e:
        # Not all IDs exist, that's expected
        pass

print(f"Total files restored from production: {success_count}")
