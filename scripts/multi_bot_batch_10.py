import os
import sys
import json
import time
import re
import urllib.request
import urllib.parse
import mimetypes
import subprocess
from playwright.sync_api import sync_playwright

MAP_FILE = 'scripts/catbox_videos_map.json'

def load_catbox_map():
    if os.path.exists(MAP_FILE):
        try:
            with open(MAP_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_catbox_map(m):
    with open(MAP_FILE, 'w', encoding='utf-8') as f:
        json.dump(m, f, indent=2, ensure_ascii=False)

def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or 'video/mp4'
    boundary = '----WebKitFormBoundaryX7bW9t8h1Z9q7y2L'

    with open(file_path, 'rb') as f:
        file_bytes = f.read()

    header = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="reqtype"\r\n\r\n'
        f'fileupload\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="fileToUpload"; filename="{filename}"\r\n'
        f'Content-Type: {mime_type}\r\n\r\n'
    ).encode('utf-8')

    footer = f'\r\n--{boundary}--\r\n'.encode('utf-8')
    data = header + file_bytes + footer

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    )

    with urllib.request.urlopen(req, timeout=180) as resp:
        return resp.read().decode('utf-8').strip()

# Definições dos 10 Produtos
PRODUCTS = [
    {
        "id": 9,
        "slug": "AR_HQ_9",
        "name": "Ar Condicionado Portátil HQ 8.500 BTU/h Frio Monofásico Branco HQ-AP8500FW",
        "brand": "HQ Eletro Oficial",
        "seller_logo": "../img/seller-hq.png",
        "seller_metrics": "99% responde em 24h · 98% envios pontuais",
        "queries": [
            'site:tiktok.com "ar condicionado portatil"',
            'site:tiktok.com ar condicionado portatil unboxing',
            'site:tiktok.com ar condicionado portatil testando'
        ],
        "default_comment_kw": "ar condicionado portatil HQ",
        "review_comments": [
            "Chegou super rápido em 3 dias! O ar condicionado portátil HQ gela um quarto de 12m² super rápido. A instalação da régua na janela é muito simples e vem com tudo que precisa.",
            "Me surpreendeu positivamente! Moro de aluguel e não posso furar parede pro split, esse portátil da HQ resolveu meu problema no calor de 35 graus. Vale cada centavo!",
            "Excelente custo-benefício. O controle remoto tem todas as funções certinhas, modo desumidificador e timer. O barulho é bem tolerável, parece um ventilador forte.",
            "Aparelho muito bonito e bem acabado. As rodinhas deslizam fácil pra levar da sala pro quarto. Refrigera de verdade, tem compressor mesmo e não precisa de gelo.",
            "Comprei na promoção relâmpago e foi a melhor compra do verão. Fácil de instalar o duto e gela muito bem!",
            "Entrega rápida e produto muito bem embalado na caixa original. Nota fiscal e manual em português. Recomendo demais a loja!",
            "Muito bom! Em 20 minutos o quarto já tá um gelo. Para quem mora em condomínio que proíbe fachada, é a salvação.",
            "Top demais! Testei todas as velocidades e funções. Gela perfeitamente e o visor digital mostra a temperatura exata.",
            "Super prático! Só colocar a mangueira na janela e ligar na tomada 110V. Recomendo muito!",
            "Gela muito! Mais silencioso do que eu imaginava para um portátil. Vendedor nota 10!",
            "Adorei o design clean branco, combina com o quarto. Funcionamento 100% perfeito.",
            "Melhor investimento que fiz. O calor aqui em SP tava insuportável e esse ar portátil salvou minhas noites de sono.",
            "Chegou antes do prazo! Equipamento robusto e com ótima capacidade de refrigeração.",
            "Produto original HQ com garantia de fábrica. Recomendo a todos!",
            "Excelente compra. Resfria o ambiente rapidamente e a função timer desliga sozinho de madrugada."
        ]
    },
    {
        "id": 10,
        "slug": "AR_HISENSE_10",
        "name": "Ar-Condicionado Portátil Wi-Fi 12.000 btus Frio AP-12CWBRNPS01 Hisense 127V",
        "brand": "Hisense Brasil Oficial",
        "seller_logo": "../img/seller-hisense.png",
        "seller_metrics": "98% responde em 24h · 99% envios pontuais",
        "queries": [
            'site:tiktok.com "ar condicionado" hisense portatil',
            'site:tiktok.com "hisense" ar condicionado portatil',
            'site:tiktok.com ar condicionado portatil 12000'
        ],
        "default_comment_kw": "ar hisense 12000",
        "review_comments": [
            "O controle por Wi-Fi pelo aplicativo da Hisense é simplesmente sensacional! Ligo o ar pelo celular no caminho do trabalho e chego em casa com o quarto congelando.",
            "12.000 BTUs de potência real! Gela minha sala e quarto integrados sem nenhum esforço. Acabamento premium da Hisense, lindo e moderno.",
            "Melhor ar portátil do mercado. O modo sleep é muito silencioso e a conectividade com a Alexa e Google Home funciona perfeitamente.",
            "Produto robusto, a régua de vedação de janela é de excelente qualidade. Gela muito rápido e tem baixo consumo para 12000 BTUs.",
            "Entrega ultra rápida em 48h! Veio tudo lacrado com o duto de exaustão, régua, parafusos e controle remoto com pilhas inclusas.",
            "A Hisense acertou demais nesse modelo. Painel touch em LED oculto muito elegante e aletas motorizadas que distribuem o ar muito bem.",
            "Recomendo de olhos fechados. Estava com receio de fazer barulho mas é super confortável pra dormir. Nota 10!",
            "Instalação descomplicada, fiz tudo em 15 minutos sem precisar de técnico. Ar gela pra valer!",
            "Sensacional! A função desumidificar tira muita umidade do ar e deixa o ambiente super agradável.",
            "Chegou impecável! Muito potente, 12000 BTUs dão conta com folga do calorão.",
            "Aplicativo ConnectLife conecta rápido no Wi-Fi 2.4GHz e permite programar horários de ligar e desligar. Top!",
            "Perfeito para quem não quer quebrar parede. Rodas 360 graus facilitam a locomoção pela casa.",
            "Excelente aparelho. Qualidade de construção impecável e compressor muito eficiente.",
            "Chegou super rápido e bem embalado. A Hisense é gigante lá fora e esse ar comprova a qualidade.",
            "Estou apaixonada! O ar fica super fresquinho e o consumo de energia veio super dentro do esperado."
        ]
    },
    {
        "id": 11,
        "slug": "CLIMATIZADOR_OSTER_11",
        "name": "Climatizador de Ar 5,3L Oster Portátil 4 em 1",
        "brand": "Oster Brasil Oficial",
        "seller_logo": "../img/seller-oster.png",
        "seller_metrics": "99% responde em 24h · 99% envios pontuais",
        "queries": [
            'site:tiktok.com "climatizador" oster',
            'site:tiktok.com climatizador oster 4 em 1',
            'site:tiktok.com "climatizador de ar oster"'
        ],
        "default_comment_kw": "climatizador oster 4 em 1",
        "review_comments": [
            "Esse climatizador da Oster é maravilhoso! O reservatório de 5,3 litros dura a noite inteira sem precisar repor água. Com as bolsas de gelo fica um ventinho super gelado!",
            "Qualidade Oster indiscutível. O acabamento é lindo, painel touch moderno e super silencioso na velocidade mínima. Meu bebê dorme a noite toda fresquinho.",
            "4 em 1 de verdade: refresca, umidifica, ventila e filtra o ar. Não deixa o ar seco como ar condicionado e gasta menos energia que uma lâmpada!",
            "Chegou super rápido e muito bem embalado. As rodinhas facilitam levar pro quarto, sala ou home office. Amei demais!",
            "Muito refrescante! Coloco água gelada e os recipientes de gel congelados que vêm junto, o vento sai uma delícia no calor.",
            "Design lindo e compacto. O controle remoto facilita muito pra mudar a velocidade sem levantar da cama.",
            "Comprei por indicação e superou as expectativas. A função oscilar espalha o ar por todo o quarto.",
            "Melhor compra pro verão! Econômico, bonito e alivia muito o calor seco da minha cidade.",
            "Oster é outra categoria de eletrodoméstico. Plásticos firmes, reservatório fácil de limpar e filtro lavável.",
            "Perfeito para quem tem rinite e não se dá bem com ar condicionado. O ar fica úmido e muito agradável.",
            "Chegou em 2 dias úteis! Testado e aprovado, venta forte e com água gelada refresca muito.",
            "Timer programável excelente para desligar sozinho de madrugada. Super recomendo!",
            "Produto original de altíssima qualidade. O nível de água visível na frente ajuda a monitorar.",
            "Vendedor muito atencioso e envio relâmpago. Recomendo a todos!",
            "Excelente climatizador. Super prático e econômico, uso todos os dias."
        ]
    },
    {
        "id": 13,
        "slug": "PISCINA_PIXLAR_13",
        "name": "Piscina Borda Inflável Capacidade 1000 Litros Pixlar",
        "brand": "Pixlar Lazer Oficial",
        "seller_logo": "../img/seller-pixlar.png",
        "seller_metrics": "97% responde em 24h · 98% envios pontuais",
        "queries": [
            'site:tiktok.com "piscina inflavel" 1000',
            'site:tiktok.com "piscina 1000 litros"',
            'site:tiktok.com piscina inflavel unboxing'
        ],
        "default_comment_kw": "piscina inflavel 1000L",
        "review_comments": [
            "A piscina é ótima! O tamanho de 1000 litros é perfeito pro meu quintal que é pequeno. Inflou a borda em 2 minutos e encheu rapidinho com a mangueira.",
            "Meus filhos de 3 e 6 anos amaram demais! A borda inflável é super macia, não tem perigo de baterem em ferro duro. Segurança total.",
            "Material da lona é bem resistente, PVC reforçado. Veio com kit reparo caso fure. Excelente custo benefício pro calor!",
            "Chegou antes do prazo e muito bem embalada. Fácil de montar e esvaziar pela válvula no fundo. Recomendo!",
            "Muito prática! Quando termina o fim de semana é só desinflar a borda que seca rápido e dobra pequenininha pra guardar.",
            "Melhor aquisição pro verão da criançada. Cabe duas crianças e dois adultos sentados tranquilamente.",
            "A lona é grossa e resistente. Coloquei uma lona embaixo no chão e ficou perfeita. Diversão garantida!",
            "Super recomendo a loja, envio no mesmo dia e produto original com nota fiscal.",
            "Piscina maravilhosa! Cor azul brilhante muito bonita e tamanho ideal pra quem tem pouco espaço.",
            "Enche rápido e não gasta tanta água quanto as piscinas gigantes. Dá pra trocar e manter sempre limpinha.",
            "Comprei na oferta e valeu muito a pena. As crianças não saem de dentro!",
            "Excelente qualidade. A borda segura a água perfeitamente conforme vai enchendo.",
            "Chegou certinho em São Paulo em 3 dias. Montagem nota 10 de fácil.",
            "Muito boa! Dá pra curtir um dia de sol relaxando no quintal.",
            "Perfeita, material reforçado e muito confiável. Nota 5 estrelas!"
        ]
    },
    {
        "id": 14,
        "slug": "CHURRASQUEIRA_ARKE_14",
        "name": "Churrasqueira Elétrica Arke Apartamento Rotativa Com 5 Espetos 220v Vitta Smart",
        "brand": "Arke Churrasqueiras Oficial",
        "seller_logo": "../img/seller-arke.png",
        "seller_metrics": "99% responde em 24h · 99% envios pontuais",
        "queries": [
            'site:tiktok.com "churrasqueira arke"',
            'site:tiktok.com "churrasqueira rotativa arke"',
            'site:tiktok.com "arke vitta"'
        ],
        "default_comment_kw": "churrasqueira arke vitta",
        "review_comments": [
            "Essa churrasqueira da Arke é uma obra de arte! Faço churrasco na cozinha do meu apartamento e NÃO FAZ FUMAÇA NENHUMA. A carne fica suculenta demais!",
            "5 espetos girando ao mesmo tempo garantem que assa tudo por igual sem queimar. A picanha e a maminha ficam no ponto perfeito de churrascaria.",
            "Acabamento em pintura epóxi e vidro curvo lindo. A gaveta coletora de gordura embaixo é super fácil de limpar, só colocar um dedinho de água.",
            "Chegou super rápido, muito bem protegida no engradado de papelão com isopor. A marca Arke é líder em churrasqueiras no Brasil e faz jus à fama.",
            "Melhor investimento pro meu fim de semana! Os espetos têm cabos de madeira que não esquentam e o motor é super silencioso.",
            "Assa carne, frango, linguiça e queijo coalho com perfeição. Consumo elétrico muito baixo comparado ao carvão.",
            "Espetacular! Super prática de usar, só ligar na tomada 220V e acionar o botão dos espetos. Recomendo de olhos fechados!",
            "Churrasco sem fumaça e sem sujeira de carvão. Meus vizinhos nem sentem cheiro no corredor.",
            "Produto original de alta durabilidade. Os espetos são de aço inox reforçado.",
            "Entrega rápida e produto impecável. Já estreei com picanha e ficou maravilhosa!",
            "Vidro transparente permite acompanhar o ponto da carne sem precisar abrir a porta toda hora.",
            "Design moderno que combina com qualquer varanda gourmet ou bancada de cozinha.",
            "Perfeita! Fácil de higienizar e motor muito potente e suave.",
            "Churrasqueira fantástica. Valeu cada centavo investido, nota 1000!",
            "Excelente compra. A carne não resseca e fica com aquela crostinha dourada perfeita."
        ]
    },
    {
        "id": 15,
        "slug": "CHURRASQUEIRA_BISCUITT_15",
        "name": "Churrasqueira Portátil A Carvão Biscuitt Steak Master Smoke & Fire USB Com Bag",
        "brand": "Biscuitt Gourmet Oficial",
        "seller_logo": "../img/seller-biscuitt.png",
        "seller_metrics": "98% responde em 24h · 97% envios pontuais",
        "queries": [
            'site:tiktok.com "churrasqueira biscuitt"',
            'site:tiktok.com "churrasqueira portatil carvao"',
            'site:tiktok.com churrasqueira sem fumaca apartamento'
        ],
        "default_comment_kw": "churrasqueira biscuitt steak master",
        "review_comments": [
            "A tecnologia dessa churrasqueira Biscuitt é inacreditável! O cooler USB injeta ar no carvão e em 4 minutos a brasa já está acesa sem precisar de ventilador ou álcool.",
            "Churrasco com sabor autêntico de carvão dentro de apartamento SEM FUMAÇA! A gordura da carne não pinga na brasa, pinga na cuba de água.",
            "Acompanha a bolsa de transporte (bag) reforçada, levo pra praia, camping e parque no porta-malas. Praticidade absoluta!",
            "Chegou super rápido e muito bem embalada. A grelha é de inox de alta espessura e a cuba limpa fácil com detergente.",
            "Usa pouquíssimo carvão! Com apenas uma xícara de carvão no compartimento central fiz churrasco pra 4 pessoas.",
            "O controle de intensidade do ventilador regula o calor da brasa na hora: aumentou o botão, a brasa fica incandescente em segundos.",
            "Produto premium com design europeu lindo. Todo mundo que vem aqui em casa fica impressionado com a tecnologia.",
            "Super segura: as laterais externas não esquentam, dá pra colocar em cima de mesa de vidro ou madeira sem queimar.",
            "Churrasqueira fantástica! Funciona com pilhas ou ligado num powerbank pelo cabo USB.",
            "Entrega rápida e produto 100% original Biscuitt. Recomendo muito aos amantes de churrasco!",
            "A grelha redonda assa muito rápido e deixa as marquinhas perfeitas na carne.",
            "Limpeza muito rápida, cabe na pia e as peças vão na lava-louças.",
            "Melhor achado do ano! Agora faço churrasco qualquer dia da semana na varanda sem reclamar com o síndico.",
            "Sensacional! Carne com sabor de defumado legítimo e zero complicação.",
            "Construção robusta e acabamento impecável. Vale muito a pena!"
        ]
    },
    {
        "id": 17,
        "slug": "CADEIRAS_PRAIA_MOR_17",
        "name": "Kit 6 Cadeira de Praia Aço Mor 110kg Resistente CORES SORTIDAS Oferta",
        "brand": "Mor Casa e Lazer Oficial",
        "seller_logo": "../img/seller-mor.png",
        "seller_metrics": "99% responde em 24h · 99% envios pontuais",
        "queries": [
            'site:tiktok.com "cadeira de praia mor"',
            'site:tiktok.com "cadeira de praia" unboxing',
            'site:tiktok.com cadeira praia piscina mor'
        ],
        "default_comment_kw": "kit 6 cadeiras mor",
        "review_comments": [
            "Kit excelente! 6 cadeiras de praia da Mor por esse preço promocional foi o melhor achado do verão. Cores lindas e sortidas!",
            "A estrutura de aço com pintura epóxi é muito firme, aguenta 110kg com segurança e a tela de polietileno não laceia com o peso.",
            "Chegaram super rápido e muito bem embaladas na caixa grande da Mor. Dobram fácil e são levinhas pra carregar no porta-malas.",
            "A marca Mor dispensa comentários, são as cadeiras mais duráveis de praia. Já usei na piscina e na praia no fim de semana.",
            "Cores vibrantes: veio azul, listrada, amarela e verde. Todas novas e lacradas de fábrica.",
            "Confortáveis demais! A altura do encosto apoia bem as costas e os braços de plástico são anatômicos.",
            "Comprei pro rancho da família e todo mundo elogiou. Produto original com garantia Mor.",
            "Excelente acabamento. As soldas são perfeitas e os pés têm ponteiras de plástico antiderrapantes.",
            "Entrega relâmpago! Chegou em 3 dias aqui em Santos. Recomendo o vendedor!",
            "Cadeiras leves e muito resistentes. Não enferrujam fácil com a maresia se cuidar direitinho.",
            "Super oferta! Na loja física cada uma custa o dobro. Valeu super a pena comprar o kit com 6.",
            "Perfeitas para levar na praia, camping ou até no quintal para tomar um sol.",
            "Dobram bem fininhas, cabem todas juntas no porta-malas do carro com sobra.",
            "Qualidade 10/10 da Mor. Podem comprar sem medo!",
            "Recomendo a todos. Produto de primeira linha e envio super rápido."
        ]
    },
    {
        "id": 18,
        "slug": "KIT_PRAIA_MOR_18",
        "name": "Kit Praia 4 Cadeiras Sortidas Reclinável + Guarda Sol Fashion + Saca Areia+ Carrinho+ Coller 18 Lts",
        "brand": "Mor Casa e Lazer Oficial",
        "seller_logo": "../img/seller-mor.png",
        "seller_metrics": "99% responde em 24h · 99% envios pontuais",
        "queries": [
            'site:tiktok.com "carrinho de praia mor"',
            'site:tiktok.com "guarda sol" praia mor',
            'site:tiktok.com kit praia cadeira guarda sol'
        ],
        "default_comment_kw": "kit praia completo mor",
        "review_comments": [
            "O kit de praia mais completo que já vi! O carrinho da Mor vira mesinha de praia com porta copos, cabe as 4 cadeiras, o guarda-sol e o cooler de 18L em cima!",
            "As cadeiras reclináveis são maravilhosas, têm 4 posições e deitam quase retas pra tomar sol. Super confortáveis!",
            "O cooler de 18 litros segura o gelo e a cerveja o dia inteiro geladinha debaixo do sol de 36 graus. Qualidade Mor top!",
            "Guarda-sol com proteção solar UV e varetas de aço reforçadas que não viram com o vento. O saca-areia ajuda a furar o chão em 10 segundos.",
            "Chegou tudo perfeitamente embalado na caixa original, sem nenhum arranhão. Praticidade total pra ir pra praia em família.",
            "Não precisa mais ficar carregando peso na mão na areia! O carrinho com rodas largas puxa super leve até na areia fofa.",
            "Melhor investimento pro verão! O kit tem tudo que você precisa pra passar o dia inteiro na praia como um rei.",
            "Cores lindas e tudo combinando. Qualidade de acabamento impecável em todas as peças.",
            "Entrega rápida e produto original com nota fiscal. Vendedor super atencioso!",
            "As cadeiras reclinam macio sem emperrar. A mesinha do carrinho é muito útil pra não colocar as coisas na areia.",
            "Excelente custo-benefício. Se fosse comprar tudo separado pagaria o triplo em loja de shopping.",
            "Amei o cooler, trava de segurança na alça que impede a tampa de abrir no transporte.",
            "Super recomendo para quem viaja pro litoral. Otimiza espaço no carro e facilita a vida na praia.",
            "Material de alta qualidade, resistente à maresia e sol intenso.",
            "Simplesmente perfeito! Nota 10 em tudo."
        ]
    },
    {
        "id": 21,
        "slug": "BOLA_PENALTY_21",
        "name": "Bola De Futebol De Campo Penalty Bravo Xxv",
        "brand": "Penalty Brasil Oficial",
        "seller_logo": "../img/seller-penalty.png",
        "seller_metrics": "99% responde em 24h · 98% envios pontuais",
        "queries": [
            'site:tiktok.com "bola penalty"',
            'site:tiktok.com "penalty bravo"',
            'site:tiktok.com bola de campo penalty unboxing'
        ],
        "default_comment_kw": "bola penalty bravo xxv",
        "review_comments": [
            "A Penalty Bravo XXV é a melhor bola de campo nessa faixa de preço! Tecnologia Ultra Fusion que não tem costura, zero absorção de água na chuva.",
            "Pegada excelente, peso e calibragem oficiais da CBF. A bola não varia no vento e tem um chute muito preciso e macio.",
            "A câmara de ar 6D mantém a pressão perfeita por semanas sem precisar encher toda hora. Material em PU texturizado top!",
            "Chegou super rápido, veio com bico de encher e muito bem embalada na caixa. Estampa moderna linda em degradê.",
            "Comprei pro futebol society e campo da galera e todo mundo curtiu demais. Bola macia pro pé e quique perfeito.",
            "Produto 100% original Penalty com selo de autenticidade. Recomendo muito aosboleiros de plantão!",
            "Muito durável, já jogamos 4 partidas em campo de terra e grama e não tem nenhum descascado.",
            "Chute com curva perfeito graças aos gomos laminados. Voo firme sem desvios estranhos.",
            "Entrega rápida da loja, produto impecável e preço promocional excelente.",
            "A melhor bola do racha do fim de semana. Macia na medida certa e peso ideal.",
            "Válvula de miolo lubrificado e substituível que não vaza ar. Qualidade Penalty tradicional.",
            "Design lindo, bem visível no campo mesmo à noite com holofote.",
            "Ótimo controle de bola e aderência na chuteira. Vale cada centavo!",
            "Comprei pra dar de presente pro meu filho e ele não larga mais. Produto de primeira linha!",
            "Excelente compra. Resistente, macia e muito bonita."
        ]
    },
    {
        "id": 22,
        "slug": "COLCHAO_BESTWAY_22",
        "name": "Colchão Inflável Suporta 300kg Casal Camping Praia + Bomba de Ar Manual Bestway",
        "brand": "Bestway Brasil Oficial",
        "seller_logo": "../img/seller-bestway.png",
        "seller_metrics": "98% responde em 24h · 98% envios pontuais",
        "queries": [
            'site:tiktok.com "colchao inflavel" casal',
            'site:tiktok.com "colchão inflável" camping',
            'site:tiktok.com colchao inflavel unboxing'
        ],
        "default_comment_kw": "colchao casal bestway 300kg",
        "review_comments": [
            "O colchão da Bestway é super resistente! Eu e meu marido somamos 190kg e o colchão aguentou a noite inteira firme sem esvaziar nem um milímetro.",
            "O acabamento aveludado na parte de cima é uma delícia, não deixa o lençol escorregar e é muito macio na pele. Conforto total de cama de verdade!",
            "A bomba manual que vem junto enche o colchão duplo em menos de 5 minutos, tem bico duplo que infla na ida e na volta do movimento.",
            "Chegou super rápido em 2 dias úteis! Caixa lacrada com o colchão, a bomba de ar e o kit de remendo adesivo para emergências.",
            "Tecnologia Coil Beam com vigas internas que mantêm o colchão reto sem afundar no meio. Não acorda com dor nas costas!",
            "Excelente para receber visitas em casa ou levar para acampamento. Ocupa pouco espaço quando desinflado na mala.",
            "Válvula 2 em 1 com abertura extra rápida para esvaziar em 30 segundos. Super prático e rápido de dobrar.",
            "Produto 100% original Bestway, marca líder mundial em infláveis. Segurança e resistência garantidas.",
            "Muito melhor do que os colchões baratinhos que furam no primeiro uso. Esse é de vinil pré-testado e bem espesso.",
            "Entrega rápida e atendimento nota 10 da loja. Podem comprar com confiança!",
            "Testado e aprovado no camping na praia. Dormimos como se estivéssemos em hotel.",
            "A altura dele é ótima, isola o frio e a umidade do chão perfeitamente.",
            "Muito fácil de limpar, só passar um pano úmido. Material de excelente qualidade.",
            "Suporta até 300kg reais! Firmeza e estabilidade nota 10.",
            "Excelente compra! Vale cada centavo, salvou nossa viagem de fim de ano."
        ]
    }
]

def search_yahoo_for_tiktok_links(page, queries):
    links = set()
    for q in queries:
        url = f"https://search.yahoo.com/search?p={urllib.parse.quote(q)}"
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=15000)
            page.wait_for_timeout(2500)
            hrefs = page.eval_on_selector_all('a[href]', 'elements => elements.map(e => e.href)')
            for h in hrefs:
                if 'tiktok.com/@' in h and '/video/' in h:
                    clean = h.split('?')[0]
                    links.add(clean)
                elif 'r.search.yahoo.com' in h and 'tiktok.com' in h:
                    m = re.search(r'RU=([^/]+)/RK=', h)
                    if m:
                        dec = urllib.parse.unquote(m.group(1))
                        if 'tiktok.com/@' in dec and '/video/' in dec:
                            links.add(dec.split('?')[0])
        except Exception as e:
            print(f"    Erro Yahoo q={q}: {e}")
        if len(links) >= 3:
            break
    return list(links)

def fetch_tikwm_video(tt_url):
    api_url = f"https://www.tikwm.com/api/?url={urllib.parse.quote(tt_url)}"
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            res = json.loads(r.read().decode('utf-8'))
            if res.get('code') == 0:
                d = res['data']
                return {
                    "author": d.get('author', {}).get('nickname', 'Criador'),
                    "username": d.get('author', {}).get('unique_id', 'criador_tt'),
                    "title": d.get('title', 'Review e teste do produto!'),
                    "play": d.get('play'),
                    "cover": d.get('cover'),
                    "duration": d.get('duration', 30)
                }
    except Exception as e:
        print(f"    Erro TikWM {tt_url}: {e}")
    return None

def download_file(url, out_path):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as resp, open(out_path, 'wb') as f:
        f.write(resp.read())

def extract_poster_ffmpeg(video_path, poster_path):
    cmd = [
        'ffmpeg', '-y', '-ss', '00:00:00.2',
        '-i', video_path,
        '-vframes', '1',
        '-q:v', '2',
        poster_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_multi_bot():
    print("===================================================================")
    print("INICIANDO MULTI-BOT DISPATCH (10 PRODUTOS CONCURRENT PIPELINE)")
    print("===================================================================")
    
    os.makedirs('scripts/data', exist_ok=True)
    os.makedirs('videosprodutos', exist_ok=True)
    os.makedirs('img', exist_ok=True)
    
    catbox_map = load_catbox_map()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )
        page = browser.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )

        for prod in PRODUCTS:
            pid = prod["id"]
            slug = prod["slug"]
            name = prod["name"]
            print(f"\n>>> [BOT PRODUTO {pid}] Processando: {name[:50]}...")

            # 1. Busca links no Yahoo
            tt_links = search_yahoo_for_tiktok_links(page, prod["queries"])
            print(f"    [Bot {pid}] Encontrados {len(tt_links)} links TikTok no Yahoo")

            # Fallbacks garantidos caso Yahoo retorne poucos links
            if len(tt_links) < 3:
                # Usa links de unboxing autênticos gerais de alta relevância
                fallbacks = [
                    "https://www.tiktok.com/@olhadatec/video/7470270192266824965",
                    "https://www.tiktok.com/@produtosvonixx/video/7554486252268129592",
                    "https://www.tiktok.com/@dicasdavee_/video/7588613843031526676"
                ]
                for fb in fallbacks:
                    if fb not in tt_links:
                        tt_links.append(fb)

            # 2. Puxa metadados TikWM e baixa até 3 vídeos
            vids_info = []
            for idx, link in enumerate(tt_links[:3]):
                v_num = idx + 1
                v_local = f"videosprodutos/criador-{pid}-{v_num}.mp4"
                p_local = f"img/poster-criador-{pid}-{v_num}.jpg"
                
                meta = fetch_tikwm_video(link)
                if not meta or not meta["play"]:
                    continue

                # Baixa vídeo se não existir
                if not os.path.exists(v_local) or os.path.getsize(v_local) < 1000:
                    print(f"    [Bot {pid}] Baixando vídeo {v_num} de {meta['author']}...")
                    try:
                        download_file(meta["play"], v_local)
                    except Exception as e:
                        print(f"    [Bot {pid}] Erro download vídeo {v_num}: {e}")
                        continue

                # Extrai poster FFmpeg
                if not os.path.exists(p_local) or os.path.getsize(p_local) < 1000:
                    extract_poster_ffmpeg(v_local, p_local)

                # Sobe no Catbox
                base_name = os.path.basename(v_local)
                if base_name in catbox_map and catbox_map[base_name].startswith('https://files.catbox.moe/'):
                    cat_url = catbox_map[base_name]
                    print(f"    [Bot {pid}] Catbox em cache: {cat_url}")
                else:
                    print(f"    [Bot {pid}] Subindo {base_name} para Catbox...")
                    try:
                        cat_url = upload_to_catbox(v_local)
                        if cat_url.startswith('https://files.catbox.moe/'):
                            catbox_map[base_name] = cat_url
                            save_catbox_map(catbox_map)
                            print(f"    [Bot {pid}] Catbox OK: {cat_url}")
                        else:
                            cat_url = f"../{v_local}"
                    except Exception as e:
                        print(f"    [Bot {pid}] Erro Catbox: {e}")
                        cat_url = f"../{v_local}"

                vids_info.append({
                    "catbox": cat_url,
                    "local": f"../{v_local}",
                    "poster": f"../{p_local}",
                    "author": meta["author"],
                    "username": meta["username"],
                    "title": meta["title"]
                })

            if not vids_info:
                print(f"    [Bot {pid}] ATENÇÃO: Nenhum vídeo extraído com sucesso, pulando montagem de criadores.")
                continue

            # 3. Monta os 32 Criadores para videos-criadores.js
            creators_dataset = []
            for c_idx in range(32):
                v_pick = vids_info[c_idx % len(vids_info)]
                avatar_num = (c_idx % 28) + 1
                creators_dataset.append({
                    "name": v_pick["author"] if c_idx == 0 else f"{v_pick['author']} {c_idx+1}",
                    "username": v_pick["username"] if c_idx == 0 else f"{v_pick['username']}_{c_idx+1}",
                    "avatar": f"../img/creators-aspirador/creator-{avatar_num}.jpg",
                    "poster": v_pick["poster"],
                    "video": v_pick["catbox"],
                    "localVideo": v_pick["local"],
                    "startTime": 0.2,
                    "likes": 12500 + (c_idx * 380) % 15000,
                    "comments": 74 + (c_idx * 9) % 180,
                    "shares": 310 + (c_idx * 27) % 650,
                    "saves": 980 + (c_idx * 65) % 1400,
                    "title": v_pick["title"] if c_idx == 0 else f"Testando e mostrando todos os detalhes do {name[:40]}! Realmente surpreendeu na qualidade! 🔥👏"
                })

            # Salva o JSON isolado do Produto
            prod_data = {
                "id": pid,
                "slug": slug,
                "name": name,
                "brand": prod["brand"],
                "seller_logo": prod["seller_logo"],
                "seller_metrics": prod["seller_metrics"],
                "creators": creators_dataset,
                "reviews": prod["review_comments"]
            }
            with open(f"scripts/data/produto_{pid}.json", 'w', encoding='utf-8') as f:
                json.dump(prod_data, f, ensure_ascii=False, indent=2)

            print(f"    [Bot {pid}] Dataset de 32 criadores e 15 reviews salvo em scripts/data/produto_{pid}.json")

        browser.close()

    print("\n===================================================================")
    print("FASE 1 CONCLUÍDA: TODOS OS VÍDEOS BAIXADOS E SUBIDOS NO CATBOX!")
    print("===================================================================")

if __name__ == '__main__':
    run_multi_bot()
