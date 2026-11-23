import urllib.request

urls = [
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH_SJSzOmggvqBtULQDpaJxdiRWj0EHN2ZVPHbaEULEQ8xqR6aXYGzlUaN0Ac1XwamY3Sgy8vCMKB0aAl4v58HsE31hutKq4MxJncFKtPkLFTYguKFLq11N6yjPI3yqKL5xfvqA09SyH_PbKysaTRq9bwBRPE-l-I8qjnBf_s4kUya7cBRV7EQ=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHDwr6eBl5A1KPPuCf2AWVr0qj_m91-L9ftqUFCXXdYeTwmv-ChVs-LnpOOmx5CheQziecDTScsZKTwF6BD8_SZktS2Ql2jz5H_Xq9_rXlBjJLZ7XLRmMO3KnPioOB_hNBZHWpjpWHMMbRLNasM4PURsEIE4QseyhlnEA6Xa_nwtYtf6FTJjP5Vu0IDs2aKz4l8e-bNdci5M8jC1JMizdlEZRLs_KCJvGvANd4="
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("Final URL:", resp.geturl())
    except Exception as e:
        print("Error:", e)
