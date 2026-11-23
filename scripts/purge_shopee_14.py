with open('pages/produto-14.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Substitui o script de imagens do produto
import re
html = re.sub(r"img:\s*'https://down-tx-br\.vod\.susercontent\.com/[^']*'", "img: '../img/produto-14-1.jpg'", html)
html = re.sub(r'imagens:\s*\["https://down-tx-br\.vod\.susercontent\.com/[^"]*"\]', 'imagens: ["../img/produto-14-1.jpg", "../img/produto-14-2.jpg", "../img/produto-14-3.jpg", "../img/produto-14-4.jpg"]', html)

# Substitui imagens dos relacionados que eram Shopee
html = re.sub(r'src="https://down-br\.img\.susercontent\.com/[^"]*"', 'src="../img/produto-104-1.jpg"', html)

with open('pages/produto-14.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Residual Shopee purgado com sucesso!")
