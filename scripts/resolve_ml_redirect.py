import urllib.request
import re

url1 = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHYJkbLXBzmGIvCGOFfC4oxVCjpOA5FvXNcLZNV4HU_lLeCZNEP00z6dYM9aypKP-hxGazSTwMg-XLRPavxKeQUjpDF7vrMzKi91O6mc2J23Y6MSXWr4K-j-meodYbxuR8tOpo-I8_omuJVU_yFp4fGNMqsnnN_6OHaaJtZ_4NiXo_zqQ8IlVHXpnstmROkbOplgjS1RmOnvT4jgjum6BcDKQ=="

req = urllib.request.Request(url1, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        final_url = resp.geturl()
        print("Final URL:", final_url)
        content = resp.read().decode('utf-8', errors='ignore')
        print(f"Content length: {len(content)}")
        # Look for MLA images
        mla_imgs = re.findall(r'https?://[^\s"\'<>]*(?:MLA\d+|user_review)[^\s"\'<>]*', content)
        print(f"Found {len(mla_imgs)} review/MLA image candidates")
        for img in mla_imgs[:5]:
            print(" ", img)
except Exception as e:
    print("Error:", e)
