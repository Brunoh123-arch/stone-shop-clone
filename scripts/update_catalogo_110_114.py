import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('js/catalogo.js', encoding='utf-8') as f:
    content = f.read()

new_entries = """const CATALOGO_PRODUTOS = [
  {id:110,nome:'Tênis Kappa Pulse RX Masculino e Feminino Amortecimento Corrida e Caminhada',preco:69.9,precoOrig:'259,90',desc:73,vendidos:6520,img:'../img/produto-110-1.jpg'},
  {id:111,nome:'Projetor de Árvore de Natal HD USB com 6 Cenas Festivas 3D Rotativo',preco:49.9,precoOrig:'199,90',desc:75,vendidos:5180,img:'../img/produto-111-1.jpg'},
  {id:112,nome:'Caminhão de Bombeiros 2 em 1 Montanha-Russa de Patinhos Bate-Volta Led Musical',preco:44.9,precoOrig:'169,90',desc:73,vendidos:3890,img:'../img/produto-112-1.jpg'},
  {id:113,nome:'Comedouro Cachorro e Gato Elevado Duplo em Acrílico Transparente Anti-Engasgo',preco:39.9,precoOrig:'129,90',desc:69,vendidos:7340,img:'../img/produto-113-1.jpg'},
  {id:114,nome:'Controle Arcade 7 em 1 Stick Retrô Multiplataforma PS4 PS3 Xbox PC Switch Celular',preco:89.9,precoOrig:'349,90',desc:74,vendidos:2950,img:'../img/produto-114-1.jpg'},"""

if 'const CATALOGO_PRODUTOS = [' in content:
    content = content.replace('const CATALOGO_PRODUTOS = [', new_entries, 1)
    with open('js/catalogo.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("js/catalogo.js updated successfully with products 110-114!")
else:
    print("ERROR: could not find CATALOGO_PRODUTOS header")
