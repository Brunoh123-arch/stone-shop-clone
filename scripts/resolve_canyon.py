import urllib.request

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFLmQcsF3J09W-FhoumxEndPezvzRGUHg2I_H0O-IryzplrK47RklLjmiBprQQHxvKx-Gb3-epAgqQf_y9VHRj2Jo54rT6Xj_AYK_MT98t4fjEsa_bQ7I73yTehfLXycdabY8afQPsF_Pn-tOpqr_v8zDsquuuUHFIolvz9GdJ2BdE007INMdc6sMpQpfci34g8v4yyDDuj6Ds="

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print("Final URL:", resp.geturl())
except Exception as e:
    print("Error:", e)
