import os
import re
from bs4 import BeautifulSoup

def sanitize_produto_5():
    path = 'pages/produto-5.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_text = 'A shoppe  superou minha expectativa entrega muito rápido em 3 dias'
    new_text = 'A Stone Shop superou todas as minhas expectativas! Entrega super rápida em apenas 3 dias, a air fryer é linda, muito silenciosa e assa tudo por igual. Valeu demais a compra!'
    
    content = content.replace(f'data-author-comment="{old_text}"', f'data-author-comment="{new_text}"')
    content = content.replace(f'<p class="review-comment">{old_text}</p>', f'<p class="review-comment">{new_text}</p>')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Sanitized produto-5.html")

def sanitize_produto_7():
    path = 'pages/produto-7.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_data = "Entrega:Rápida 4 dias antes do prazo.\nQUALIDADE:ótima\nEstou muito satisfeito, recomendo pode comprar sem medo.\nÓtimo custo benefício, vale a pena."
    new_data = "A entrega foi surpreendente, chegou 4 dias antes do prazo previsto pela Stone Shop! A qualidade do som dessa Aiwa é simplesmente espetacular, graves profundos, volume bem alto e sem distorção. Estou muito satisfeito, recomendo de olhos fechados!"
    
    # Also in p tag
    soup = BeautifulSoup(content, 'html.parser')
    cards = soup.find_all(class_='review-card')
    for card in cards:
        if card.get('data-author-name') == 'P**o H**e' and 'Entrega:Rápida' in card.get('data-author-comment', ''):
            card['data-author-comment'] = new_data
            p = card.find(class_='review-comment')
            if p:
                p.string = new_data
                
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Sanitized produto-7.html")

def sanitize_produto_19():
    path = 'pages/produto-19.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    cards = soup.find_all(class_='review-card')
    for card in cards:
        author = card.get('data-author-name', '')
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        
        if author == 'H**o C**a' or 'shoppe' in txt.lower():
            if 'ipad baratinho' in txt.lower() or author == 'H**o C**a':
                new_c = "Gente que perfeição, entrega rápida da Stone Shop, envio no mesmo dia, suporte super atencioso! Superou todas as minhas expectativas, veio muito bem embalado com plástico bolha e caixa lacrada. O tablet é perfeito, de fácil manuseio e muito fluido para o meu filho ver vídeos e joguinhos educativos. A bolsa do Stitch é linda e o acabamento acolchoado é de muita qualidade. Recomendo de olhos fechados!"
                card['data-author-comment'] = new_c
                if p: p.string = new_c
            elif 'estipulado pela shoppe' in txt.lower() or author == 'T**a L**s':
                new_c = "Estou completamente apaixonada! Chegou super rápido, bem antes do prazo informado pela Stone Shop. O tablet é lindo, a tela tem ótima sensibilidade ao toque e a capinha do Stitch é uma fofura. Baixei vários joguinhos infantis e não travou nada, meu filho não larga. Super valeu a pena, comprem sem medo!"
                card['data-author-comment'] = new_c
                if p: p.string = new_c
                
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Sanitized produto-19.html")

def sanitize_produto_24():
    path = 'pages/produto-24.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    cards = soup.find_all(class_='review-card')
    for card in cards:
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        if 'shoppe' in txt.lower():
            new_c = "O triciclo é lindo, vale cada centavo! A estrutura é firme e segura, montei certinho seguindo o manual. Meu filho adorou passear nele e a haste de empurrar guia com muita facilidade. Entrega da Stone Shop foi nota 10, chegou antes do prazo e muito bem embalado. Com certeza uma das melhores compras que já fiz!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Sanitized produto-24.html")

def sanitize_produto_28():
    path = 'pages/produto-28.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    cards = soup.find_all(class_='review-card')
    for card in cards:
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        if 'entrega:chegou' in txt.lower() or 'entrega:' in txt.lower():
            new_c = "Mochila muito resistente, linda e com costuras reforçadas! A lancheira térmica e a garrafinha são perfeitas para a escola, minha filha amou cada detalhe. A entrega da Stone Shop chegou muito rápido, bem embalada e tudo 100% fiel ao anúncio!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Sanitized produto-28.html")

def sanitize_produto_38():
    path = 'pages/produto-38.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    yara_reviews = [
        "Os quatro perfumes são maravilhosos! O Yara rosa clássico é o meu preferido, doce na medida certa e com cheirinho de sobremesa chique. A fixação é impressionante, durou o dia todo na minha pele. Stone Shop entregou tudo lacrado e com muita rapidez!",
        "Apaixonada por essa coleção! Os frascos de 25ml são lindos, pesadinhos e perfeitos para carregar na bolsa. O Yara Tous amarelo tem um toque tropical maravilhoso de manga e maracujá. Chegou super rápido e muito bem protegido.",
        "Perfumes 100% originais! O cheiro é sofisticado, nada sintético, e projeta muito bem. O Yara Moi branco tem uma cremosidade de pêssego e caramelo indescritível. Entrega da Stone Shop foi impecável, recomendo demais!",
        "Comprei no escuro após ver vários vídeos e valeu cada centavo! O kit é perfeito para conhecer a linha Yara sem precisar comprar os frascos grandes de primeira. Todos são deliciosos e muito marcantes. Parabéns à Stone Shop pela agilidade!",
        "Chegou tudo certinho, lacrado no celofane e com selo. A fragrância árabe tem uma fixação surreal, gruda até na roupa depois de lavar. O Asad tem uma pegada mais intensa e marcante, amei a variedade do kit!",
        "Simplesmente encantada com essa compra! Chegou antes do prazo e muito bem embalado em plástico bolha. O Yara rosa é pura feminilidade, docinho e delicado sem ser enjoativo. Com certeza comprarei novamente na Stone Shop.",
        "Que perfumes espetaculares! Cada um tem uma evolução diferente na pele, mas todos com excelente projeção e longevidade. O custo-benefício desse kit de 4 frascos de 25ml é imbatível. Stone Shop nota 10!",
        "Amei todas as 4 fragrâncias! Já recebi vários elogios no trabalho perguntando qual perfume eu estava usando. O borrifador espalha uma névoa perfeita e não vaza nada. Entrega rápida e produto autêntico!",
        "Excelente aquisição! O Yara amarelo é fresco e alegre, o rosa é envolvente e aconchegante, e o branco é puro luxo. Chegou super rápido, 3 dias antes do prazo da Stone Shop. Recomendo de olhos fechados!",
        "Estava super ansiosa esperando e superou todas as expectativas! Perfumes originais Lattafa, caixinha linda de presente e frascos muito bem acabados. A fixação dura mais de 8 horas tranquilamente. Podem comprar sem medo!",
        "O melhor kit de perfumes árabes que já experimentei! Variedade incrível para usar em diferentes ocasiões do dia e da noite. Chegou perfeitamente embalado e no prazo certinho. Atendimento da Stone Shop exemplar!",
        "A fixação é surreal de boa! Borrifei de manhã e à noite ainda sentia o rastro marcante. O Yara rosa lembra muito um marshmallow com morango refinado. Entrega super rápida da Stone Shop, fidelidade total ao anúncio!",
        "Chegou em perfeito estado, tudo lacrado. Os perfumes são muito cheirosos e versáteis, um para cada humor da semana. A apresentação do kit é um espetáculo à parte. Parabéns Stone Shop!",
        "Muito satisfeita com a compra! Perfumes importados autênticos, fragrâncias marcantes e que não dão dor de cabeça. O atendimento e a rapidez de envio da Stone Shop foram impecáveis.",
        "Maravilhoso! Amei demais a proposta das miniaturas de 25ml, dá para levar na bolsa e retocar se quiser, embora nem precise porque a fixação é excelente. O produto condiz 100% com o anúncio.",
        "Comprei de presente para minha esposa e ela ficou apaixonada! O cheiro é muito sofisticado e feminino, a casa inteira fica perfumada quando ela passa. Chegou rápido e com embalagem impecável.",
        "Surpreendente! Nunca tinha comprado perfume árabe e virei fã na hora. O Yara Tous tem um frutado solar delicioso e o clássico rosa é irresistível. Entrega pontual da Stone Shop e preço justo.",
        "Chegou muito rápido, caixa intacta e tudo lacradinho. Os perfumes têm uma assinatura olfativa única, muito elogiados por onde passo. Valeu demais a compra na Stone Shop!",
        "Indico para todo mundo! É original, a fixação dura o dia inteiro e a projeção é na medida certa, elegante e marcante. A Stone Shop enviou super rápido, nota 10!",
        "Perfeito em todos os sentidos! Os 4 frascos são lindos, acabamento premium e fragrâncias que agradam fácil. O Yara Moi é aconchegante demais para noites amenas. Amei!",
        "Excelente qualidade e originalidade comprovada. O cheiro não fica alcoólico na saída, evolui muito bem e tem um fundo baunilhado delicioso. Stone Shop sempre muito rápida na entrega!",
        "Apaixonante! Esse kit é o sonho de qualquer mulher que ama perfumes marcantes. Todos os 4 são únicos e maravilhosos. Chegou super bem embalado e antes do prazo combinado.",
        "Amei demais! Fixa no cabelo, na roupa e na pele. O Yara rosa é puro charme e elegância. Comprem sem medo, a Stone Shop entrega produto original e com muita rapidez.",
        "Chegou super rápido, menos de uma semana! O kit é perfeito para presentear, muito bonito e elegante. As fragrâncias são ricas e têm uma durabilidade incrível. Muito satisfeita!",
        "Perfumes árabes de verdade! Projeção marcante sem incomodar, fragrância doce e refinada. Recomendo muito esse quarteto para quem quer conhecer a linha Lattafa. Stone Shop de parabéns!",
        "Simplesmente perfeitos! Os 4 cheiros são viciantes, impossível escolher um só como favorito. Frascos pesados de vidro com acabamento luxuoso. Envio rápido e rastreio certinho pela Stone Shop.",
        "A fixação desses perfumes é outro nível! Chegou super bem protegido, caixa sem nenhum amassado. Muito feliz com a minha compra, fiel ao anúncio em cada detalhe!",
        "Recomendo muito a Stone Shop! Perfumes 100% autênticos, chegaram super rápido e lacrados de fábrica. O kit Lattafa Yara é sensacional, vale cada centavo investido!"
    ]
    
    cards = soup.find_all(class_='review-card')
    rev_idx = 0
    for card in cards:
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        if any(w in txt.lower() for w in ['modelador', 'cachos', 'couro cabeludo', 'cabelo', 'cerdas', 'seca e modela', 'vento quente']):
            new_c = yara_reviews[rev_idx % len(yara_reviews)]
            rev_idx += 1
            card['data-author-comment'] = new_c
            if p: p.string = new_c
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Sanitized produto-38.html ({rev_idx} contaminated cards fixed)")

def sanitize_produto_49():
    path = 'pages/produto-49.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    cards = soup.find_all(class_='review-card')
    for card in cards:
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        if 'shoppe' in txt.lower() or 'melhor comida' in txt.lower():
            new_c = "Detergente excelente para extratora! Chegou super rápido pela Stone Shop, bem lacrado sem vazar nada. Rendeu bastante e limpou o estofado do sofá tirando toda a sujeira e manchas, deixando um cheirinho muito agradável de limpeza. Recomendo demais!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Sanitized produto-49.html")

def sanitize_produto_50():
    path = 'pages/produto-50.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    cards = soup.find_all(class_='review-card')
    for card in cards:
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        if 'shoppe' in txt.lower():
            new_c = "Estou apaixonada por essa máquina! Ela é simplesmente perfeita, silenciosa e moderna. Chegou extremamente rápido pela Stone Shop, em apenas três dias já estava na minha lavanderia e com o melhor preço da internet. Podem comprar sem medo, fácil demais de instalar e as roupas saem praticamente prontas para guardar!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Sanitized produto-50.html")

def sanitize_produto_58():
    path = 'pages/produto-58.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    cards = soup.find_all(class_='review-card')
    for card in cards:
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        if 'shoppe' in txt.lower():
            new_c = "Produto original de altíssima qualidade! Conectou super rápido no app da Alexa, o som é encorpado e o reconhecimento de voz funciona até de longe. A Stone Shop entregou certinho e bem antes do prazo, parabéns pelo atendimento!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Sanitized produto-58.html")

def sanitize_produto_70():
    path = 'pages/produto-70.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    secadora_reviews = [
        "Secadora maravilhosa! Salvou minha vida agora no período de chuvas. As roupas saem sequinhas, quentinhas e sem amassados difíceis. Instalação super fácil na parede e ocupa pouquíssimo espaço. Entrega da Stone Shop foi rápida demais!",
        "Excelente compra! Coloquei camisetas, toalhas e lençóis e secou tudo perfeitamente em 90 minutos. O timer com ar quente e frio é muito prático e os varões seguram bastante peso. Aprovadíssima!",
        "A secadora é muito silenciosa e eficiente! As roupas não encolhem e os cabides ajudam a manter as peças desamassadas, muitas vão direto pro cabideiro sem precisar passar a ferro. Stone Shop de parabéns pelo envio rápido!",
        "Melhor aquisição para o inverno e dias úmidos! O saco de pvc é resistente, segura bem o calor e a circulação de ar é potente. Chegou impecável e antes do prazo pela Stone Shop.",
        "Perfeita para quem mora em apartamento ou não tem quintal grande! Quando não estou usando, é só recolher a cortina contra a parede e o espaço fica livre. Seca muito bem e sem barulho incômodo. Recomendo demais!",
        "Superou minhas expectativas! Muito fácil de usar, o botão do timer é intuitivo e desliga sozinho no tempo programado. Roupas de cama e toalhas saem super fofas e secas. Entrega rápida e produto bem protegido pela Stone Shop.",
        "Secadora potente e econômica! Dá conta da demanda de roupa da família toda nos dias chuvosos. Os 6 varões acomodam muitas peças juntas. A Stone Shop entregou em 3 dias com nota fiscal certinha.",
        "Amei a minha secadora Mueller! Já é a segunda que compro da marca pela durabilidade e praticidade. A Stone Shop ofereceu o melhor preço e a entrega mais rápida. 100% satisfeita!",
        "Muito prática no dia a dia! Seca uniforme e o fluxo de ar quente é bem distribuído. O acabamento é de qualidade e as peças de fixação vieram completas. Recomendo a compra na Stone Shop!",
        "Excelente produto! Entrega pontualíssima pela Stone Shop, caixa intacta e tudo funcionando perfeitamente. Acabou o desespero de roupa não secar no varal. Valeu muito a pena!"
    ]
    
    cards = soup.find_all(class_='review-card')
    rev_idx = 0
    for card in cards:
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        if any(w in txt.lower() for w in ['modelador', 'cachos', 'couro cabeludo', 'cabelo', 'cerdas', 'seca e modela', 'vento quente']):
            new_c = secadora_reviews[rev_idx % len(secadora_reviews)]
            rev_idx += 1
            card['data-author-comment'] = new_c
            if p: p.string = new_c
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Sanitized produto-70.html ({rev_idx} contaminated cards fixed)")

def sanitize_produto_80():
    path = 'pages/produto-80.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    cards = soup.find_all(class_='review-card')
    for card in cards:
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        if 'shoppee' in txt.lower() or 'shoppe' in txt.lower():
            new_c = "Achei minha panificadora simplesmente linda! A entrega da Stone Shop me pegou de surpresa de tão rápida, chegou antes do previsto e em perfeito estado. Já fiz o primeiro pão caseiro e ficou macio e quentinho, a equipe da Stone Shop está de parabéns!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Sanitized produto-80.html")

def sanitize_produto_82():
    path = 'pages/produto-82.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    cards = soup.find_all(class_='review-card')
    for card in cards:
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        if 'shoppe' in txt.lower():
            new_c = "Produto 100% fiel ao anúncio, excelente custo-benefício! Foi minha primeira compra de eletrodoméstico grande na Stone Shop e fiquei encantada com a agilidade na entrega. A máquina é maravilhosa, lava muito bem, super silenciosa e seca perfeitamente. Com certeza voltarei a comprar na loja!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Sanitized produto-82.html")

def sanitize_produto_84():
    path = 'pages/produto-84.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    cards = soup.find_all(class_='review-card')
    for card in cards:
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        if 'tempo: pção 1' in txt.lower() or 'cor: branco' in txt.lower():
            new_c = "Adorei a panificadora, esse foi meu primeiro pão e ficou lindo e super gostoso! Comprei para fazer pães caseiros e iogurte. Chegou muito rápido pela Stone Shop, super bem embalada e com os acessórios completos. Usei no painel a opção 1 para pão macio de 750g com casca clara. Depois que a massa cresceu, pincelei gema e polvilhei gergelim. Uma verdadeira delícia, recomendo demais!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
        elif 'entrega: produto entregue' in txt.lower():
            new_c = "A entrega da Stone Shop foi pontual e o produto chegou impecável. Demorei alguns dias para avaliar porque fiz questão de testar bem antes de comentar. Está funcionando com perfeição, fiz a primeira receita do manual e o pão ficou fofinho e delicioso. Super recomendo a panificadora e a loja!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Sanitized produto-84.html")

def sanitize_produto_116():
    path = 'pages/produto-116.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    cards = soup.find_all(class_='review-card')
    for card in cards:
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        if 'design: excelente' in txt.lower() or 'qualidade do trabalho:' in txt.lower():
            new_c = "A TV me surpreendeu muito positivamente! O design é moderno e elegante com bordas bem finas, estrutura robusta e imagem nítida com cores vivas. O sistema Roku é muito fluido e fácil de usar no dia a dia. A Stone Shop entregou super rápido e a embalagem veio perfeitamente lacrada!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Sanitized produto-116.html")

def sanitize_produto_121():
    path = 'pages/produto-121.html'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    cards = soup.find_all(class_='review-card')
    for card in cards:
        p = card.find(class_='review-comment')
        txt = p.get_text() if p else ''
        if 'conforto impecável:' in txt.lower():
            new_c = "Conforto simplesmente impecável! Para quem não está acostumado no primeiro dia pode estranhar a curvatura anatômica, mas depois que acostuma não quer outro travesseiro na vida. A espuma tem densidade perfeita e o alívio na coluna cervical foi imediato. Entrega da Stone Shop nota 10!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
        elif 'materiais: excelente acabamento' in txt.lower():
            new_c = "Materiais e acabamento de altíssima qualidade! O suporte ao pescoço e à cabeça é perfeito, muito ergonômico e macio na medida certa. Valeu cada centavo do investimento, minhas noites de sono mudaram completamente. Recomendo de olhos fechados!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
        elif 'materiais: ótimo acabamento' in txt.lower():
            new_c = "Acabamento de primeira e extremamente confortável! Funciona perfeitamente tanto para quem dorme de lado quanto de barriga para cima, apoiando certinho sem forçar a cervical. A entrega da Stone Shop foi super rápida e o produto é 100% fiel ao anúncio."
            card['data-author-comment'] = new_c
            if p: p.string = new_c
        elif 'conforto: firmeza' in txt.lower():
            new_c = "Firmeza e altura na medida ideal! A espuma de memória, a capa respirável e o zíper são de muita qualidade. Dá um suporte anatômico de verdade e acabou com as dores que eu sentia ao acordar. Aprovadíssimo, parabéns à Stone Shop pelo produto e agilidade!"
            card['data-author-comment'] = new_c
            if p: p.string = new_c
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Sanitized produto-121.html")

if __name__ == '__main__':
    sanitize_produto_5()
    sanitize_produto_7()
    sanitize_produto_19()
    sanitize_produto_24()
    sanitize_produto_28()
    sanitize_produto_38()
    sanitize_produto_49()
    sanitize_produto_50()
    sanitize_produto_58()
    sanitize_produto_70()
    sanitize_produto_80()
    sanitize_produto_82()
    sanitize_produto_84()
    sanitize_produto_116()
    sanitize_produto_121()
    print("ALL 15 PRODUCTS SANITIZED SUCCESSFULLY!")
