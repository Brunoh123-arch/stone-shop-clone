// Catálogo gerado automaticamente — usa apenas imagens estáticas (não vídeo)
const CATALOGO_PRODUTOS = [
  {id:146,nome:"Caixa de Som Portátil JBL PartyBox Encore Essential Bluetooth 100W RMS Show de Luzes LED IPX4",preco:197.9,precoOrig:'1.299,00',desc:85,vendidos:7438,img:"../img/jbl-146-slide-1.webp"},
  {id:147,nome:"Triciclo Elétrico Drift Infantil 360° 350W Bateria 36V c/ Luzes LED, Chave, Display e Bluetooth",preco:167.9,precoOrig:'799,90',desc:79,vendidos:5126,img:"../img/triciclo-147-slide-1.webp"},
  {id:148,nome:"Jogo de Panelas Brinox Ceramic Life Smart Plus 8 Peças Antiaderente Pro-Ceramic Vanilla c/ Tampas de Vidro",preco:119.9,precoOrig:'549,90',desc:78,vendidos:8290,img:"../img/panelas-148-slide-1.webp"},
  {id:149,nome:"Cortina Cascata Luminosa 3m x 3m 300 LEDs Colorido RGB & Branco Quente USB IP44 c/ Controle Remoto",preco:29.89,precoOrig:'119,90',desc:75,vendidos:11420,img:"../img/cortina-149-slide-1.webp"},
  {id:150,nome:"Fogão 4 Bocas Esmaltec Ideal Super Mesa Inox Acendimento Automático Forno Limpa Fácil 50L Bivolt",preco:189.9,precoOrig:'599,90',desc:68,vendidos:4180,img:"../img/fogao-150-slide-1.webp"},
  {id:151,nome:"Smart TV 32\" LG HD LED ThinQ AI HDR10 Processador α5 WebOS Wi-Fi Bluetooth Alexa Integrada",preco:279.9,precoOrig:'999,00',desc:72,vendidos:5890,img:"../img/tv-151-slide-1.webp"},
  {id:152,nome:"Smartphone Samsung Galaxy A17 5G Dual SIM Tela Super AMOLED 6,7\" 90Hz Câmera Tripla 50MP OIS NFC",preco:279.9,precoOrig:'949,00',desc:71,vendidos:6310,img:"../img/galaxy-152-slide-1.webp"},
  {id:153,nome:"Tablet Samsung Galaxy Tab S10 FE Tela 10,9\" 90Hz Wi-Fi IP68 c/ Caneta S-Pen e Capa Inclusas",preco:297.9,precoOrig:'1.855,00',desc:84,vendidos:4290,img:"../img/tabs10-153-slide-1.webp"},
  {id:154,nome:"Máquina de Lavar Roupas Brastemp 13kg Automática Cesto Inox Ciclo Tira-Manchas Advanced e Antibolinhas",preco:397.9,precoOrig:'1.679,00',desc:76,vendidos:3740,img:"../img/brastemp-154-slide-1.webp"},
  {id:136,nome:"Kit Cozinha Mondial Liquidificador 550W + Batedeira 400W 3,6L + Copo Medidor e Espátula",preco:89.9,precoOrig:'299,90',desc:70,vendidos:2840,img:"../img/kit-mondial-136-slide-1.webp"},
  {id:138,nome:"Cortina de LED 3m x 3m 300 LEDs USB c/ Controle Remoto 8 Funções e Ganchos Integrados",preco:24.89,precoOrig:'109,90',desc:77,vendidos:8420,img:"../img/cortina-led-138-slide-1.webp"},
  {id:139,nome:'Vestido Curto Ombro a Ombro Drapeado c/ Faixa Lateral Assimétrica Festas Natal e Réveillon',preco:19.89,precoOrig:'159,90',desc:88,vendidos:3650,img:'../img/vestido-139-slide-1.webp'},
  {id:144,nome:"Câmera Infantil Instantânea que Imprime a Foto na Hora Sem Tinta + 3 Bobinas Térmicas e Alça",preco:37.89,precoOrig:'199,90',desc:81,vendidos:4829,img:"../img/camera-144-slide-1.webp"},
  {id:129,nome:"Escova Elétrica Giratória de Limpeza Sem Fio 9 em 1 Impermeável c/ Cabo Extensor Retrátil USB",preco:29.89,precoOrig:'159,90',desc:81,vendidos:6184,img:"../img/escova-129-slide-1.webp"},
  {id:127,nome:"Carrinho Controle Remoto Drift 4x4 Turbo que Solta Fumaça com LED + Kit Pneus Drift e Cones",preco:49.89,precoOrig:'249,90',desc:80,vendidos:3918,img:"../img/drift-127-slide-1.webp"},
  {id:145,nome:"Combo Mala de Bordo Rígida ABS Giro 360° Padrão ANAC + Frasqueira de Viagem (Kit 2 Peças)",preco:69.89,precoOrig:'399,90',desc:83,vendidos:4376,img:"../img/mala-145-slide-1.webp"},
  {id:128,nome:"Mesa Dobrável Portátil Vira Maleta 1,80m Reforçada com Alça e Trava (Ceia, Churrasco e Camping)",preco:67.89,precoOrig:'329,90',desc:79,vendidos:3695,img:"../img/mesa-128-slide-1.webp"},
  {id:135,nome:'Smartwatch Série 10 W99+ Pro Tela Super AMOLED NFC ChatGPT GPS Faz e Recebe Ligações',preco:89.9,precoOrig:'349,90',desc:74,vendidos:9200,img:'../img/smartwatch-135-slide-1.webp'},
  {id:134,nome:"Caneta Aparadora e Depiladora de Sobrancelhas Elétrica Recarregável USB c/ Luz LED Indolor",preco:11.89,precoOrig:'49,90',desc:76,vendidos:5191,img:"../img/sobrancelha-134-slide-1.webp"},
  {id:133,nome:'Cordão de Luz Natal Pisca-Pisca 100 LEDs 9m 8 Funções Fio Transparente Decoração',preco:9.69,precoOrig:'39,90',desc:76,vendidos:6454,img:'../img/pisca-133-slide-1.webp'},
  {id:132,nome:"Cinta Modeladora Feminina Redutora Abdominal M+ 6 Níveis de Ajuste Tecido Respirável",preco:19.79,precoOrig:'89,90',desc:78,vendidos:4617,img:"../img/cinta-132-slide-1.webp"},
  {id:126,nome:"Patinete Elétrico Infantil Dobrável com Luzes LED nas Rodas e Guidão Ajustável em 3 Alturas",preco:119.9,precoOrig:'499,90',desc:76,vendidos:3842,img:"../img/patinete-126-slide-1.webp"},
  {id:110,nome:"Tênis Kappa Pulse RX Masculino e Feminino Amortecimento Corrida e Caminhada",preco:69.9,precoOrig:"259,90",desc:73,vendidos:6553,img:"../img/produto-110-1.jpg"},
  {id:111,nome:"Projetor LED Natalino 16 Desenhos Temáticos USB Bivolt Decoração",preco:19.69,precoOrig:'99,90',desc:80,vendidos:5253,img:"../img/produto-111-oficial-1.jpg?v=3"},
  {id:112,nome:"Brinquedo Pista Montanha-Russa de Patinhos com Escada Musical e Luzes Led",preco:16.73,precoOrig:'89,90',desc:81,vendidos:3914,img:"../img/produto-112-patinho-1.jpg"},
  {id:113,nome:"Comedouro Cachorro e Gato Elevado Duplo em Acrílico Transparente Anti-Engasgo",preco:14.69,precoOrig:'79,90',desc:82,vendidos:7401,img:"../img/produto-113-1.jpg"},
  {id:114,nome:"Controle Arcade 7 em 1 Stick Retrô Multiplataforma PS4 PS3 Xbox PC Switch Celular",preco:89.9,precoOrig:"349,90",desc:74,vendidos:2965,img:"../img/produto-114-1.jpg"},
  {id:109,nome:"Modelador de Cachos Automático Sem Fio Portátil Cerâmica Bateria USB",preco:23.79,precoOrig:'149,90',desc:84,vendidos:14369,img:"../img/produto-109-1.jpg"},
  {id:108,nome:"Escova Secadora e Modeladora 5 em 1 Multifuncional Efeito Coanda Bivolt",preco:27.89,precoOrig:'149,90',desc:81,vendidos:18462,img:"../img/produto-108-1.jpg"},
  {id:107,nome:"Mini Aspirador de Pó Sem Fio Portátil e Soprador Turbo 2 em 1 Carro e Casa",preco:13.79,precoOrig:'89,90',desc:85,vendidos:16888,img:"../img/produto-107-1.jpg"},
  {id:106,nome:"Body Modelador Cinta Alta Compressão Invisível Efeito Lipo Redutora",preco:16.89,precoOrig:'89,90',desc:81,vendidos:23451,img:"../img/produto-106-1.jpg"},
  {id:105,nome:"Projetor HY300 Original Portátil Smart Android 11 4K Ultra HD HDMI Wifi Bluetooth Alto",preco:34.79,precoOrig:'199,90',desc:83,vendidos:14829,img:"img/prod-105-local-1.webp"},
  {id:104,nome:"Chinelo Feminino Luxo Strass Brilhante Macio Leve",preco:11.49,precoOrig:'59,90',desc:81,vendidos:21303,img:"../img/produto-104-1.jpg"},
  {id:103,nome:"Vestido longo feminino costas nua com fenda chique eventos festas moda fashion justo e elegante",preco:49.9,precoOrig:"189,90",desc:74,vendidos:5648,img:"img/prod-103-local-1.webp"},
  {id:101,nome:"Pneus Pirelli - Encontre a medida ideal para o seu veículo",preco:189.9,precoOrig:'599,00',desc:68,vendidos:13488,img:"https://tyre24.pirelli.com/dynamic_engine/assets/visori/cake/p7cnt.png"},
  {id:52,nome:"Pad 11 Geração A16 256GB Wi-fi Tela 11pol Original Novo Lacrado com Garantia  de 1 ano",preco:389.9,precoOrig:'2.199,00',desc:82,vendidos:7654,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-mdh7rladn00h24"},
  {id:5,nome:"Fritadeira Elétrica Visio Fry Elgin 5L 1700w Air Fryer Digital Cinza",preco:67.9,precoOrig:"399,90",desc:83,vendidos:5849,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-mh9e1c37asxxe2"},
  {id:7,nome:"Caixa de Som AIWA",preco:69.9,precoOrig:"597,00",desc:88,vendidos:7894,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rceh-lrrqafsspb32c2"},
  {id:9,nome:"Ar Condicionado Portátil HQ 8.500 BTU/h Frio Monofásico Branco HQ-AP8500FW",preco:349.9,precoOrig:'1.799,00',desc:81,vendidos:10241,img:"https://down-br.img.susercontent.com/file/sg-11134201-7renf-m8lxuc60fdsy07"},
  {id:12,nome:"Piscina Splash Fun Redonda Inflável 2400 Litros - Mor",preco:89.9,precoOrig:"399,00",desc:78,vendidos:9899,img:"../img/produto-12-1.jpg"},
  {id:13,nome:"Piscina Inflável Redonda Mor 1000 Litros Splash Fun Azul",preco:49.9,precoOrig:"169,90",desc:71,vendidos:10004,img:"https://down-br.img.susercontent.com/file/sg-11134201-82260-mhoz9j95dloj8d"},
  {id:14,nome:"Churrasqueira Assador a Gás GLP Rotativo Arke 5 Espetos AGR-05 Bivolt",preco:189.9,precoOrig:'749,90',desc:75,vendidos:9874,img:"../img/produto-14-1.jpg"},
  {id:15,nome:"Churrasqueira Portátil A Carvão Biscuitt Steak Master Smoke & Fire USB Com Bag",preco:69.9,precoOrig:"349,90",desc:80,vendidos:7543,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-lqnmb7oulw6f02"},
  {id:16,nome:"Churrasqueira Resistente Modelo Rodeio Bacia Esmaltada Casa Praia Piscina Verão Lazer Preta - Mor",preco:64.9,precoOrig:"299,90",desc:78,vendidos:7548,img:"https://down-br.img.susercontent.com/file/sg-11134201-7reng-m1ya6at9aqw05a"},
  {id:17,nome:"Kit 6 Cadeira de Praia Aço Mor 110kg Resistente CORES SORTIDAS Oferta",preco:89,precoOrig:"399,90",desc:78,vendidos:5668,img:"https://down-br.img.susercontent.com/file/sg-11134201-7reoq-m8kskp1ohv2vcf"},
  {id:18,nome:"Kit Praia 4 Cadeiras Sortidas Reclinável + Guarda Sol Fashion + Saca Areia+ Carrinho+ Coller 18 Lts",preco:84.9,precoOrig:"499,00",desc:83,vendidos:10706,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-mhuv620f45j7bf"},
  {id:19,nome:"Tablet Vision TAB 7 Stitch + Capa e Bolsa - Octa-Core 3GB RAM 64GB Android 14 Go Wi-Fi IPS Positivo",preco:139.9,precoOrig:'499,00',desc:72,vendidos:4987,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m84xjaeqeia9c4"},
  {id:20,nome:"Bicicleta  Aro 29 GT Sprint MX7 24V index Freio Disco Alumínio Suspensão Aero MTB",preco:269.9,precoOrig:'1.099,00',desc:75,vendidos:4984,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-me910y70d7nmf6"},
  {id:21,nome:"Bola De Futebol De Campo Penalty Bravo Xxv",preco:34.9,precoOrig:"129,90",desc:73,vendidos:5346,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rbkz-m5oo5ljc9heg98"},
  {id:22,nome:"Colchão Inflável Suporta 300kg Casal Camping Praia + Bomba de Ar Manual Bestway",preco:49.9,precoOrig:"195,90",desc:75,vendidos:5531,img:"../img/colchao-bestway-oficial-1.jpg"},
  {id:23,nome:"Conjunto De 24 Potes Herméticos Croix Com Tampa E Trava",preco:24.73,precoOrig:'119,90',desc:79,vendidos:6691,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-mci5ecdv44s2e5"},
  {id:24,nome:"Triciclo Infantil 4 em 1 Multifuncional Carrinho de Bebê Com Empurrador e CapotaSolar-Kababy",preco:84.9,precoOrig:"399,00",desc:79,vendidos:4897,img:"../img/produto-24-slide-1.jpg"},
  {id:25,nome:"Bicicleta Aro 20 Bmx infantil GottBikes Freio V-Brake",preco:79.9,precoOrig:"449,00",desc:82,vendidos:4769,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-mer4ub5zgb9c1b"},
  {id:26,nome:"Carrinho de Bebê Guarda Chuva Passeio Leve e Dobrável Mega Compras Compacto, Seguro,Cinto",preco:69.9,precoOrig:"299,90",desc:77,vendidos:4458,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m5bgd8rac7dc02"},
  {id:34,nome:"Lava Louças Praxis Portátil LLPP Semi-Automática Bivolt",preco:219.9,precoOrig:'899,90',desc:76,vendidos:9864,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m850ox58do8h8b"},
  {id:35,nome:"Caixa de Som JBL Boombox 4 Bluetooth 210W Preta Bivolt",preco:297.9,precoOrig:'1.899,00',desc:84,vendidos:8569,img:"../img/produtos/p35/slide_1.jpg"},
  {id:36,nome:"Smartphone Xiaomi Poco X7 Pro 5G Dual SIM Tela AMOLED 120Hz Câmera 50MP OIS NFC",preco:329.9,precoOrig:'1.699,00',desc:81,vendidos:9853,img:"../img/produtos/p36/slide_1.jpg"},
  {id:38,nome:"Kit Lattafa Yara Collection Feminino Edp - Perfume 4x25ml original",preco:69.9,precoOrig:"397,90",desc:82,vendidos:5515,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-mh12vhr254hs6c"},
  {id:39,nome:"Secador de Cabelos Philco PSC3500 4 em 1 Dobrável 1450W",preco:68.7,precoOrig:"397,90",desc:83,vendidos:9872,img:"https://down-br.img.susercontent.com/file/sg-11134201-824hh-mfio0pwmo0su97"},
  {id:40,nome:"Micro-ondas Mondial Mo-01-21-e 1200w 21 Litros",preco:179.9,precoOrig:'549,90',desc:67,vendidos:8953,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m9zqs2hxtuki59"},
  {id:41,nome:"Fritadeira Air Fryer Forno Oven 12L Mondial Preto e Inox0W AFON-12L-BI",preco:139.9,precoOrig:'529,90',desc:74,vendidos:8391,img:"https://down-br.img.susercontent.com/file/sg-11134201-7raui-mb4awu05e15c16"},
  {id:45,nome:"Prancha Pro 480 Turbo MQ Professional Bivolt",preco:69.9,precoOrig:"399,90",desc:83,vendidos:8654,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rept-m80tiqdhkwwh87"},
  {id:46,nome:"Panela de Pressão Elétrica Electrolux por Rita Lobo 6L Preta Experience Digital (PCC20)",preco:149.9,precoOrig:'599,90',desc:75,vendidos:9831,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rfhx-m9yig7n5t2mn18"},
  {id:47,nome:"Extratora e Higienizadora Portátil WAP Spot Cleaner 1400W Borrifa Esfrega e Extrai Sujeira",preco:169.9,precoOrig:'699,90',desc:76,vendidos:9314,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rbn7-lqeu1vzxvsrqba"},
  {id:53,nome:"Starlink V4 Internet Satélite Wi-fi 6 Alta Velocidade Nacional Homologada Anatel (Starlink Padrão)",preco:347.9,precoOrig:'1.899,00',desc:82,vendidos:5801,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-me8xwns11f5v8f"},
  {id:54,nome:"Purificador Eletrônico Compacto Efficient Painel Digital Bivolt Cinza (PE11X)",preco:169.9,precoOrig:'649,90',desc:74,vendidos:9876,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rdxh-mdeoo0q0wuft89"},
  {id:55,nome:"SWITCH  DESBLOQUEADO + 10 JOGOS DA SUA ESCOLHA COM CARTÃO DE MEMORIA 128 GB",preco:289.9,precoOrig:'1.599,00',desc:82,vendidos:5462,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m024asxqvazr6b"},
  {id:58,nome:"Caixa de som original Alaxe Echo Dot 5 geração com envio imediato e melhor preço",preco:69.9,precoOrig:"397,90",desc:82,vendidos:9876,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-mgby6v6yabr9ad"},
  {id:63,nome:"Smartwatch Redmi Watch 5 Lite GPS Preto Pulseira",preco:69.9,precoOrig:"397,90",desc:82,vendidos:9853,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rdyw-mc9fnkgv7dqz24"},
  {id:64,nome:"Bateria Auxiliar De Partida Portátil Com Bomba De Ar de Rosquear",preco:69.9,precoOrig:"397,90",desc:82,vendidos:8765,img:"https://down-br.img.susercontent.com/file/sg-11134201-8260z-mju7shogkd8jf5"},
  {id:68,nome:"Jogo de Panelas Cerâmica Kit 5 Peças Antiaderente Tampa Vidro",preco:44.73,precoOrig:'249,90',desc:82,vendidos:9052,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-mebnfn94x2pt4c"},
  {id:75,nome:"Kit 10 Camisetas Dry Fit Masculina - Casual - Treino - Academia - Esportes - Exercícios - Corrida",preco:69.9,precoOrig:"397,90",desc:82,vendidos:9843,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rdxr-lyatwes75beuc5"},
  {id:76,nome:"Aparelho Jogo De Jantar 30 Peças Orgânico Petroleum Porto Brasil Carlos Bertolazzi + BRINDE",preco:69.9,precoOrig:"497,90",desc:86,vendidos:9843,img:"https://down-br.img.susercontent.com/file/sg-11134201-8261c-mkckrt97fvgg75"},
  {id:85,nome:"Caixa De Som Karaokê Joog X2 300w Tela 10,1 Com 2 Microfones",preco:197.9,precoOrig:'1.199,00',desc:83,vendidos:9853,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m8jnvlvc270103"},
  {id:89,nome:"Kit conjunto de panelas de ferro esmaltadas luxo 18 peças",preco:79.9,precoOrig:"697,90",desc:89,vendidos:5432,img:"https://down-br.img.susercontent.com/file/br-11134207-81ztc-mj765kpbq3nla8"},
  {id:90,nome:"Jogo De Panela Avant Space 5 Peças - Tognana Cor Preto",preco:79.9,precoOrig:"647,90",desc:88,vendidos:5324,img:"https://http2.mlstatic.com/D_NQ_NP_747089-MLA96155562431_102025-O.webp"},
  {id:95,nome:"YESOP Máquina De Gelo Portátil Preto 12kg/dia 127V Produção Rápida Turbo Ice Para Casa E Bar",preco:159.9,precoOrig:'699,90',desc:77,vendidos:5259,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m9o8h6dyt2d529"},
  {id:96,nome:"Aparelho de Jantar/Chá Oxford Ryo Maresia 30 Peças",preco:69.9,precoOrig:"497,90",desc:86,vendidos:7643,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rd5p-m7uwvu85tnp9ae"},
  {id:97,nome:"Jogo de Jantar Canyon Porcelana Decorada 20 Peças Tramontina",preco:69.9,precoOrig:"596,90",desc:88,vendidos:4877,img:"https://down-br.img.susercontent.com/file/sg-11134201-81zwa-mimr7kh9srno54"},
  {id:98,nome:"Conjunto de 12 Copos De Cristal P/ Long Drink 490Ml Proper Effect",preco:44.9,precoOrig:"249,90",desc:82,vendidos:4812,img:"https://down-br.img.susercontent.com/file/d8f8f5450da9553d8273c5ffe8a1ee61"},
  {id:119,nome:"Combo Fardo Mega Fraldas Supreme Care + 4 Pacotes Lenços Umedecidos Toque Suave",preco:69.9,precoOrig:"279,90",desc:75,vendidos:8964,img:"../img/fraldas-slide-1.webp","variacoes":{"tamanho":{"com_imagem":false,"label":"Tamanho da Fralda","opcoes":[{"nome":"Tamanho M (5,5 a 9,5kg)","preco":69.9,"preco_antigo":279.9},{"nome":"Tamanho G (9 a 12,5kg)","preco":69.9,"preco_antigo":279.9},{"nome":"Tamanho XG (12 a 15kg)","preco":69.9,"preco_antigo":279.9},{"nome":"Tamanho XXG (+14kg)","preco":69.9,"preco_antigo":279.9}]}}},
  {id:121,nome:"Travesseiro Cervical Ortopédico Abranuv Pro 2.0 Espuma de Memória Viscoelástica",preco:39.9,precoOrig:"159,90",desc:75,vendidos:6765,img:"../img/travesseiro-slide-1.webp"},
  {id:122,nome:"Panela de Pressão Elétrica Digital 5L Painel Touch Inox com 10 Travas de Segurança",preco:139.9,precoOrig:'449,90',desc:69,vendidos:4842,img:"../img/panela-pressao-slide-1.webp?v=1795147990000"},
  {id:123,nome:"Lavadora de Alta Pressão Portátil Sem Fio 48V com Maleta, 2 Baterias e Canhão de Espuma",preco:79.9,precoOrig:"399,00",desc:80,vendidos:5506,img:"../img/lavadora-slide-1.webp"},
  {id:124,nome:"Livro Infantil Interativo Bilíngue Falante com Som ao Toque - Português e Inglês com Caneta Tátil",preco:21.89,precoOrig:'99,90',desc:78,vendidos:4953,img:"../img/livro-interativo-slide-1.webp","variacoes":{"idioma":{"label":"Edição","opcoes":[{"nome":"Bilíngue Português / Inglês","imagem":"../img/livro-interativo-slide-1.webp","preco":21.89}]}}},
];

// Override dinâmico de preços e produtos novos configurados no Painel Admin
(function () {
  try {
    if (typeof localStorage !== 'undefined') {
      // 1. Injeta produtos criados no painel admin
      const novosProdutos = JSON.parse(localStorage.getItem('stone_custom_produtos_criados') || '[]');
      if (Array.isArray(novosProdutos) && novosProdutos.length > 0) {
        novosProdutos.forEach(np => {
          const existe = CATALOGO_PRODUTOS.find(p => Number(p.id) === Number(np.id));
          if (!existe) {
            CATALOGO_PRODUTOS.unshift(np);
          }
        });
      }

      // 2. Aplica overrides de preços
      const customPrecos = JSON.parse(localStorage.getItem('STONE_CUSTOM_PRECOS') || localStorage.getItem('stone_custom_precos') || '{}');
      CATALOGO_PRODUTOS.forEach(p => {
        if (!p || !p.id) return;
        if (customPrecos[p.id] !== undefined && customPrecos[p.id] !== null) {
          const item = customPrecos[p.id];
          if (typeof item === 'object') {
            if (item.preco) p.preco = parseFloat(item.preco);
            if (item.precoOrig) p.precoOrig = item.precoOrig;
          } else if (item !== '') {
            p.preco = parseFloat(item);
          }
        }
      });
    }
  } catch (e) {
    console.warn('[Catalogo] Erro ao carregar customizações do admin:', e);
  }
})();
