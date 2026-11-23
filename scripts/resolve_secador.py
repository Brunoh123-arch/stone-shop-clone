import urllib.request
import re

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFk9BFut3F7BZzNjO68liHZAy8wFZu8719D9kx0zEzEGvn2ojoq_qWuPp7uFBnQwqLTdSYluDaagYZO9bMc2jzi3JjM18ICvFyCzKbg3Lo6X1BqjRDqZa-DIDilWxCgJ35HBTzoJy8YZFbWLsJyZbt1Zi88Bk7VG2B3sHU_gH2zOBH5MUtZAAA0MhoiNdwXtphLFvD0_k2BOWN95PXQ4HeFTtwQGnc="

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print("Final URL:", resp.geturl())
except Exception as e:
    print("Error:", e)
