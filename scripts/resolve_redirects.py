import urllib.request

urls = [
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHKcAxudwo8p56UKh1JIsize3iVJEOITdmcsI0OYbN0cAQg_HgQCrXxbUJuPO-ymW1dkN55Q-58zyCXwoW8SWGb5JwFhbP8LbshNi2jlUctduqmHcAFwcWBVJHReZ450EmilfTWuYi-',
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGlPYFaCTpGbQ54G8rZbdtg2Jw1r5RdH7ZhO1u0NhSoS-Ehw8HmwZNrclhV7hdxO2i0gIvixSkWZg6Y8kEmSd6T8QDfd5yJn4Cijk0hJyMhyz-syY0dCCucoP_r00k9MvqPg-XrwSez',
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH9YJwj8HjWVPxBCEtsJuA3p-goMleid1bk6W9dn6uZsCktHmSDpEkhvHAlDsaZx7T0SrZK2DKg1B6z6Ns5T35XDTYTMz-j7fkE5C8c6sspiTER29Ai9hoAIQMCATbQ5mF8DR3ATLRgsfhrgm1JQx1ZbrLbLMPjTUZUxpDxpr5_STS34--UysJX-jhHGQM_007nwoaPpdX5kGvhcoO6VFIflHQhap-Y_-ItPP2u9HBFrzhL',
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEEccMXyuhGGDYdXdp1K0t9C19Nhm4cS_UZaa04MZbn0Ji2lxE1PxqsbCGowN5Nb1BXegGP_24f4-ekyOSWJEPRAgEFUUgGVjtaqG96cqmpsXEh-ZSmEX7WgfOaoRVCNhftR_e9OV55lQ=='
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for idx, u in enumerate(urls):
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[{idx+1}] Final URL: {resp.geturl()}")
    except Exception as e:
        print(f"[{idx+1}] Error: {e}")
