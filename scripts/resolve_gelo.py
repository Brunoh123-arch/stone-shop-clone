import urllib.request
import re

urls = [
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEtYRs_UATcFGA2zkRPeY0viq4zgGqS4zHkaoADz0G2b4dKhAJAgWqHGXvLRWI7fygntnhhb7GpjB9oW-ceFCyXYhxduDkIBkEA35NW1mZNh7N8wZlGRDOZyKApIiI3-HdIbPPrv2sWvBDfT2EXtnYKGdoT0HoreLgj1W4lOj4NVpRs6XMyHuR-A3R5bYB9-w==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFuN6L1IFTiQfRfvaG6vk7mnLlvLN-BK_sI4swctr4YyNhTub1VL_QioF_09FG7JgoWoUjlfyjWyKfzt33SLv4YGGe20y9eGbjkWWgLEs97mbtaUsetMBStV7CteF7h6oIz5VQJMkTf4rFbarxY3abgh5nEwkwacSM1MjdVSUQlQ_8VIg63FLjQ_tK9TsRodWSqjPE4lKiZ0HPDLqwZapyRWPY6_rsq5Ac-MjfXTyk="
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("Final URL:", resp.geturl())
    except Exception as e:
        print("Error:", e)
