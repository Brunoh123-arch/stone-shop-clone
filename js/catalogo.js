// Catálogo gerado automaticamente — usa apenas imagens estáticas (não vídeo)
const CATALOGO_PRODUTOS = [
  {id:126,nome:'Patinete Elétrico Infantil Dobrável com Luzes LED nas Rodas e Guidão Ajustável em 3 Alturas',preco:97,precoOrig:'389,90',desc:75,vendidos:3800,img:'../img/patinete-126-slide-1.webp'},
  {id:115,nome:'Forno Elétrico HQ 48 Litros HQ48D 1600W Preto 127V / 220V',preco:289.9,precoOrig:'429,00',desc:35,vendidos:668,img:'../img/forno-hq-slide-1.webp'},
  {id:110,nome:'Tênis Kappa Pulse RX Masculino e Feminino Amortecimento Corrida e Caminhada',preco:69.9,precoOrig:'259,90',desc:73,vendidos:6520,img:'../img/produto-110-1.jpg'},
  {id:111,nome:'Projetor LED Natalino 16 Desenhos Temáticos USB Bivolt Decoração',preco:49.9,precoOrig:'199,90',desc:75,vendidos:5180,img:'../img/produto-111-oficial-1.jpg?v=3'},
  {id:112,nome:'Brinquedo Pista Montanha-Russa de Patinhos com Escada Musical e Luzes Led',preco:44.9,precoOrig:'169,90',desc:73,vendidos:3890,img:'../img/produto-112-patinho-1.jpg'},
  {id:113,nome:'Comedouro Cachorro e Gato Elevado Duplo em Acrílico Transparente Anti-Engasgo',preco:39.9,precoOrig:'129,90',desc:69,vendidos:7340,img:'../img/produto-113-1.jpg'},
  {id:114,nome:'Controle Arcade 7 em 1 Stick Retrô Multiplataforma PS4 PS3 Xbox PC Switch Celular',preco:89.9,precoOrig:'349,90',desc:74,vendidos:2950,img:'../img/produto-114-1.jpg'},
  {id:109,nome:'Modelador de Cachos Automático Sem Fio Portátil Cerâmica Bateria USB',preco:39.9,precoOrig:'362,70',desc:89,vendidos:14290,img:'../img/produto-109-1.jpg'},
  {id:108,nome:'Escova Secadora e Modeladora 5 em 1 Multifuncional Efeito Coanda Bivolt',preco:49.9,precoOrig:'415,80',desc:88,vendidos:18420,img:'../img/produto-108-1.jpg'},
  {id:107,nome:'Mini Aspirador de Pó Sem Fio Portátil e Soprador Turbo 2 em 1 Carro e Casa',preco:34.9,precoOrig:'139,90',desc:75,vendidos:16800,img:'../img/produto-107-1.jpg'},
  {id:106,nome:'Body Modelador Cinta Alta Compressão Invisível Efeito Lipo Redutora',preco:29.9,precoOrig:'189,90',desc:84,vendidos:23400,img:'../img/produto-106-1.jpg'},
  {id:105,nome:'Projetor HY300 Original Portátil Smart Android 11 4K Ultra HD HDMI Wifi Bluetooth Alto',preco:39.9,precoOrig:'399,90',desc:90,vendidos:14829,img:'img/prod-105-local-1.webp'},
  {id:104,nome:'Chinelo Feminino Luxo Strass Brilhante Macio Leve',preco:19.9,precoOrig:'59,90',desc:67,vendidos:21303,img:'../img/produto-104-1.jpg'},
  {id:103,nome:'Vestido longo feminino costas nua com fenda chique eventos festas moda fashion justo e elegante',preco:76.99,precoOrig:'129,99',desc:41,vendidos:648,img:'img/prod-103-local-1.webp'},
  {id:102,nome:'Scooter Elétrica TUI 1000w | 2 Lugares | Sem CNH | Autonomia 60km',preco:99.9,precoOrig:'2344,00',desc:94,vendidos:8944,img:'../imagemscooterpreta/D_NQ_NP_2X_712059-MLA99509048862_112025-F.webp'},
  {id:101,nome:'Pneus Pirelli - Encontre a medida ideal para o seu veículo',preco:87.9,precoOrig:'599,00',desc:83,vendidos:13488,img:'https://tyre24.pirelli.com/dynamic_engine/assets/visori/cake/p7cnt.png'},
  {id:52,nome:'Pad 11 Geração A16 256GB Wi-fi Tela 11pol Original Novo Lacrado com Garantia  de 1 ano',preco:94.9,precoOrig:'497,90',desc:81,vendidos:7654,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-mdh7rladn00h24'},
  {id:5,nome:'Fritadeira Elétrica Visio Fry Elgin 5L 1700w Air Fryer Digital Cinza',preco:124.99,precoOrig:'500,00',desc:75,vendidos:2000,img:'https://down-br.img.susercontent.com/file/br-11134207-81z1k-mh9e1c37asxxe2'},
  {id:6,nome:'Bicicleta Ergométrica Fitness para Cardio e Musculação 6kg Inercia com base Cor Preto e Vermelho Marca Sevenfit',preco:147,precoOrig:'1094,00',desc:87,vendidos:10000,img:'https://http2.mlstatic.com/D_NQ_NP_2X_679526-MLA100501405537_122025-F.webp'},
  {id:7,nome:'Caixa de Som AIWA',preco:69.9,precoOrig:'597,00',desc:88,vendidos:7894,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rceh-lrrqafsspb32c2'},
  {id:9,nome:'Ar Condicionado Portátil HQ 8.500 BTU/h Frio Monofásico Branco HQ-AP8500FW',preco:92.8,precoOrig:'754,44',desc:88,vendidos:10241,img:'https://down-br.img.susercontent.com/file/sg-11134201-7renf-m8lxuc60fdsy07'},
  
  
  {id:12,nome:'Piscina Splash Fun Redonda Inflável 2400 Litros - Mor',preco:89.90,precoOrig:'399,00',desc:78,vendidos:9840,img:'../img/produto-12-1.jpg'},
  {id:13,nome:'Piscina Inflável Redonda Mor 1000 Litros Splash Fun Azul',preco:69.99,precoOrig:'139,99',desc:50,vendidos:10004,img:'https://down-br.img.susercontent.com/file/sg-11134201-82260-mhoz9j95dloj8d'},
  {id:14,nome:'Churrasqueira Assador a Gás GLP Rotativo Arke 5 Espetos AGR-05 Bivolt',preco:189.9,precoOrig:'779,90',desc:76,vendidos:9874,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rdwx-lzpm7626yvg7c9'},
  {id:15,nome:'Churrasqueira Portátil A Carvão Biscuitt Steak Master Smoke & Fire USB Com Bag',preco:149.9,precoOrig:'624,90',desc:76,vendidos:7543,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-lqnmb7oulw6f02'},
  {id:16,nome:'Churrasqueira Resistente Modelo Rodeio Bacia Esmaltada Casa Praia Piscina Verão Lazer Preta - Mor',preco:129.3,precoOrig:'499,00',desc:74,vendidos:7548,img:'https://down-br.img.susercontent.com/file/sg-11134201-7reng-m1ya6at9aqw05a'},
  {id:17,nome:'Kit 6 Cadeira de Praia Aço Mor 110kg Resistente CORES SORTIDAS Oferta',preco:89,precoOrig:'399,90',desc:78,vendidos:5668,img:'https://down-br.img.susercontent.com/file/sg-11134201-7reoq-m8kskp1ohv2vcf'},
  {id:18,nome:'Kit Praia 4 Cadeiras Sortidas Reclinável + Guarda Sol Fashion + Saca Areia+ Carrinho+ Coller 18 Lts',preco:129.9,precoOrig:'699,00',desc:81,vendidos:10706,img:'https://down-br.img.susercontent.com/file/br-11134207-81z1k-mhuv620f45j7bf'},
  {id:19,nome:'Tablet Vision TAB 7 Stitch + Capa e Bolsa - Octa-Core 3GB RAM 64GB Android 14 Go Wi-Fi IPS Positivo',preco:137,precoOrig:'799,00',desc:83,vendidos:987,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-m84xjaeqhbf556'},
  {id:20,nome:'Bicicleta  Aro 29 GT Sprint MX7 24V index Freio Disco Alumínio Suspensão Aero MTB',preco:147,precoOrig:'799,00',desc:82,vendidos:984,img:'https://down-br.img.susercontent.com/file/br-11134207-81z1k-me910y70d7nmf6'},
  {id:21,nome:'Bola De Futebol De Campo Penalty Bravo Xxv',preco:49,precoOrig:'129,99',desc:62,vendidos:5346,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rbkz-m5oo5ljc9heg98'},
  {id:22,nome:'Colchão Inflável Suporta 300kg Casal Camping Praia + Bomba de Ar Manual Bestway',preco:69,precoOrig:'195,11',desc:65,vendidos:1531,img:'../img/colchao-bestway-oficial-1.jpg'},
  {id:23,nome:'Conjunto De 24 Potes Herméticos Croix Com Tampa E Trava',preco:64.99,precoOrig:'177,99',desc:63,vendidos:0,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-mci5ecdv44s2e5'},
  {id:24,nome:'Triciclo Infantil 4 em 1 Multifuncional Carrinho de Bebê Com Empurrador e CapotaSolar-Kababy',preco:159.9,precoOrig:'599,00',desc:73,vendidos:897,img:'../img/produto-24-slide-1.jpg'},
  {id:25,nome:'Bicicleta Aro 20 Bmx infantil GottBikes Freio V-Brake',preco:109,precoOrig:'569,00',desc:81,vendidos:769,img:'https://down-br.img.susercontent.com/file/br-11134207-81z1k-mer4ub5zgb9c1b'},
  {id:26,nome:'Carrinho de Bebê Guarda Chuva Passeio Leve e Dobrável Mega Compras Compacto, Seguro,Cinto',preco:94.9,precoOrig:'349,90',desc:73,vendidos:458,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-m5bgd8rac7dc02'},
  
  {id:28,nome:'Kit Mochila Rebecca Bonbon - Lancheira Térmica + Estojo + Box Escolar Nova Coleção Exclusiva Juvenil',preco:69.9,precoOrig:'489,90',desc:86,vendidos:12569,img:'https://down-br.img.susercontent.com/file/br-11134207-81z1k-mhqna6evm0oz72'},
  
  
  {id:31,nome:'Caixa De Som Bluetooth 200w 39000mah Tws Ipx6 Sabala Dr-909 Preto 127/220v',preco:69.8,precoOrig:'497,90',desc:86,vendidos:5867,img:'https://http2.mlstatic.com/D_NQ_NP_2X_610041-MLB96030304778_102025-F.webp'},
  {id:32,nome:'Chuveiro Acqua Duo Lorenzetti Ultra Eletrônico',preco:69.8,precoOrig:'459,90',desc:85,vendidos:9842,img:'https://down-br.img.susercontent.com/file/sg-11134201-825ar-mv0slfs1pmo9f8'},
  {id:33,nome:'Mochila Escolar Bluey E Bingo 15l Kit Meninas Com Lancheira',preco:369,precoOrig:'1.845,00',desc:80,vendidos:50,img:'https://http2.mlstatic.com/D_NQ_NP_2X_629077-MLB99739738865_112025-F-mochila-escolar-bluey-e-bingo-15l-kit-meninas-com-lancheira.webp'},
  {id:34,nome:'Lava Louças Praxis Portátil LLPP Semi-Automática Bivolt',preco:69.8,precoOrig:'397,90',desc:82,vendidos:9864,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-m850ox58do8h8b'},
  {id:35,nome:'Caixa de Som JBL Boombox 4 Bluetooth 210W Preta Bivolt',preco:67.43,precoOrig:'497,90',desc:81,vendidos:8569,img:'https://down-br.img.susercontent.com/file/sg-11134201-824i8-mdyu6aqj7g1td8'},
  {id:36,nome:'Celular Xiaomi Poco X7 Pro 5g Dual Sim 512gb Amarelo 12ram 50mpx',preco:92.8,precoOrig:'497,90',desc:81,vendidos:9853,img:'https://http2.mlstatic.com/D_NQ_NP_2X_884323-MLA99500626568_112025-F.webp'},
  {id:38,nome:'Kit Lattafa Yara Collection Feminino Edp - Perfume 4x25ml original',preco:69.9,precoOrig:'397,90',desc:82,vendidos:5490,img:'https://down-br.img.susercontent.com/file/br-11134207-81z1k-mh12vhr254hs6c'},
  {id:39,nome:'Secador de Cabelos Philco PSC3500 4 em 1 Dobrável 1450W',preco:68.7,precoOrig:'397,90',desc:83,vendidos:9872,img:'https://down-br.img.susercontent.com/file/sg-11134201-824hh-mfio0pwmo0su97'},
  {id:40,nome:'Micro-ondas Mondial Mo-01-21-e 1200w 21 Litros',preco:84.9,precoOrig:'389,90',desc:78,vendidos:8953,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-m9zqs2hxtuki59'},
  {id:41,nome:'Fritadeira Air Fryer Forno Oven 12L Mondial Preto e Inox0W AFON-12L-BI',preco:69.9,precoOrig:'397,90',desc:82,vendidos:8391,img:'https://down-br.img.susercontent.com/file/sg-11134201-7raui-mb4awu05e15c16'},
  
  {id:45,nome:'Prancha Pro 480 Turbo MQ Professional Bivolt',preco:69.9,precoOrig:'399,90',desc:83,vendidos:8654,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rept-m80tiqdhkwwh87'},
  {id:46,nome:'Panela de Pressão Elétrica Electrolux por Rita Lobo 6L Preta Experience Digital (PCC20)',preco:69.9,precoOrig:'399,90',desc:83,vendidos:9831,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rfhx-m9yig7n5t2mn18'},
  {id:47,nome:'Extratora e Higienizadora Portátil WAP Spot Cleaner 1400W Borrifa Esfrega e Extrai',preco:69.9,precoOrig:'399,90',desc:83,vendidos:9314,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rbn7-lqeu1vzxvsrqba'},
  {id:48,nome:'Panificadora Automática Mondial Master Bread 220V',preco:69.9,precoOrig:'399,90',desc:83,vendidos:9853,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rfi7-m3ar0zh6lc9a9a'},
  {id:49,nome:'Extratora e Higienizadora Portátil WAP Spot Cleaner W3 1450W Borrifa Esfrega e Extrai',preco:69.9,precoOrig:'399,90',desc:83,vendidos:9450,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rbn7-lqeu1vzxvsrqba'},
  {id:50,nome:'Lava e Seca Midea Master Clean Smart 11kg Wi-Fi MFM01D110WB-TKBR Titanium',preco:247.9,precoOrig:'597,90',desc:59,vendidos:8675,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rd5t-lvyp165360qj66'},
  {id:53,nome:'Starlink V4 Internet Satélite Wi-fi 6 Alta Velocidade Nacional Homologada Anatel (Starlink Padrão)',preco:94.9,precoOrig:'497,90',desc:81,vendidos:0,img:'https://down-br.img.susercontent.com/file/br-11134207-81z1k-me8xwns12tqb8f'},
  {id:54,nome:'Purificador Eletrônico Compacto Efficient Painel Digital Bivolt Cinza (PE11X)',preco:69.9,precoOrig:'497,90',desc:86,vendidos:9876,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rdxh-mdeoo0q0wuft89'},
  {id:55,nome:' SWITCH  DESBLOQUEADO + 10 JOGOS DA SUA ESCOLHA COM CARTÃO DE MEMORIA 128 GB',preco:64.9,precoOrig:'497,90',desc:87,vendidos:5462,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-m024asxqvazr6b'},
  {id:56,nome:'Esteira Elétrica Ergométrica Ginástica Corrida Dobrável - Max 85kg - Heroi Sports',preco:75.9,precoOrig:'788,90',desc:90,vendidos:9875,img:'../esteirafotos/esteiraprimeirafoto.PNG'},
  {id:57,nome:'caixa de som Joog One Hifi J 200w Com 2 Mic s/fio Controle remoto Ip67 app E Tws',preco:69.9,precoOrig:'497,90',desc:86,vendidos:9876,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-mdgxfw79ifo1aa'},
  {id:58,nome:'Caixa de som original Alaxe Echo Dot 5 geração com envio imediato e melhor preço',preco:69.9,precoOrig:'397,90',desc:82,vendidos:9876,img:'https://down-br.img.susercontent.com/file/br-11134207-81z1k-mgby6v6yabr9ad'},
  {id:59,nome:' Mini Internet rápida Via Satélite Antena Original Garantia de 01 ano ENVIO IMEDIATO',preco:94.9,precoOrig:'497,90',desc:81,vendidos:2000,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-md1zj59a435t8d'},
  {id:60,nome:'Caixa Som Sabala DR-908: A Escolha Definitiva para Quem Busca Potência,',preco:69.9,precoOrig:'497,90',desc:86,vendidos:9531,img:'https://down-br.img.susercontent.com/file/br-11134207-81ztc-mjev4ty4yzghc1'},
  {id:61,nome:'Caixa de Som Joog Amplificada Break X1 c/ Tela Touch 13 Microfone Sem Fio, Bluetooth, 800W, Android',preco:69.9,precoOrig:'997,87',desc:93,vendidos:8753,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rdvd-mdosx4yka39874'},
  {id:63,nome:'Smartwatch Redmi Watch 5 Lite GPS Preto Pulseira',preco:69.9,precoOrig:'397,90',desc:82,vendidos:9853,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rdyw-mc9fnkgv7dqz24'},
  {id:64,nome:'Bateria Auxiliar De Partida Portátil Com Bomba De Ar de Rosquear',preco:69.9,precoOrig:'397,90',desc:82,vendidos:8765,img:'https://down-br.img.susercontent.com/file/sg-11134201-8260z-mju7shogkd8jf5'},
  {id:65,nome:'Sofá 3 Lugares Retrátil e Reclinável Cama inBox Senses 2,00m Velusoft Cinza',preco:147.9,precoOrig:'697,90',desc:79,vendidos:8765,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rdxn-lzou0oyl6coa73'},
  {id:68,nome:'Jogo de Panelas Cerâmica Kit 5 Peças Antiaderente Tampa Vidro',preco:69.9,precoOrig:'397,86',desc:82,vendidos:9052,img:'https://down-br.img.susercontent.com/file/br-11134207-81z1k-mebnfn94x2pt4c'},
  {id:70,nome:'Secadora de Roupa Mueller Solaris 8 kg com timer ar quente e frio 6 varões e 5 cabides',preco:79.9,precoOrig:'497,90',desc:84,vendidos:8764,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-malrf6nra3dbc3'},
  {id:72,nome:'Jogo de Panelas 13 Peças Ferro Fundido Esmaltado Premium Alta Resistência Antibacteria Mantenha aquecido e fresco',preco:79.9,precoOrig:'497,90',desc:84,vendidos:7965,img:'https://down-br.img.susercontent.com/file/br-11134207-81ztc-mk3m0dsr37k1a6'},
  {id:73,nome:'Caixa de Som Bluetooth WAAW by Alok Hyperboom 1000 180W IPX7 TWS Bivolt',preco:69.9,precoOrig:'397,90',desc:82,vendidos:9853,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rdvj-m0excasdlftxa1'},
  {id:74,nome:'Kit compre 1 leve 2 Camisa Seleção Brasil Home Copa 2026',preco:129.9,precoOrig:'597,90',desc:78,vendidos:5331,img:'https://meu-pedido.sbs/images/743c81c8e45956c8395c961228aae233_1774470483.webp'},
  {id:75,nome:'Kit 10 Camisetas Dry Fit Masculina - Casual - Treino - Academia - Esportes - Exercícios - Corrida',preco:69.9,precoOrig:'397,90',desc:82,vendidos:9843,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rdxr-lyatwes75beuc5'},
  {id:76,nome:'Aparelho Jogo De Jantar 30 Peças Orgânico Petroleum Porto Brasil Carlos Bertolazzi + BRINDE',preco:69.9,precoOrig:'497,90',desc:86,vendidos:9843,img:'https://down-br.img.susercontent.com/file/sg-11134201-8261c-mkckrt97fvgg75'},
  {id:80,nome:'Panificadora 19 Programas Gallant 600w Inox / Antiaderente (Branca ou Preta)',preco:85.9,precoOrig:'398,90',desc:78,vendidos:100,img:'https://down-br.img.susercontent.com/file/br-11134207-81z1k-mg5ie67i4op35d'},
  {id:82,nome:'Lava e Seca 11kg Hisense 11 Programas de Lavagem, Steam, Wi-fi Titanium',preco:257.9,precoOrig:'2579,00',desc:90,vendidos:150,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-man0mifag5bt63'},
  {id:85,nome:'Caixa De Som Karaokê Joog X2 300w Tela 10,1 Com 2 Microfones',preco:39.9,precoOrig:'397,90',desc:90,vendidos:9853,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-m8jnvlvc270103'},
  {id:87,nome:'Calça Mom Jeans Feminina com Cinto Preto KISSMELADY Cintura Alta Modeladora',preco:77.97,precoOrig:'199,00',desc:61,vendidos:0,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-lx8mbd4xa1fj24'},
  {id:88,nome:'Conjunto Feminino de Trabalho em Alfaiataria Laris Blusa com Botões e Calça Social',preco:170.05,precoOrig:'850,25',desc:80,vendidos:0,img:'https://down-br.img.susercontent.com/file/br-11134207-81ztc-misy16cf0dmr4f'},
  {id:89,nome:'Kit conjunto de panelas de ferro esmaltadas luxo 18 peças',preco:79.9,precoOrig:'697,90',desc:89,vendidos:5432,img:'https://down-br.img.susercontent.com/file/br-11134207-81ztc-mj765kpbq3nla8'},
  {id:90,nome:'Jogo De Panela Avant Space 5 Peças - Tognana Cor Preto',preco:79.9,precoOrig:'647,90',desc:88,vendidos:5324,img:'https://http2.mlstatic.com/D_NQ_NP_747089-MLA96155562431_102025-O.webp'},
  {id:91,nome:'Pipoqueira Classic Retrô, Misturador Automático, Com Bandeja Para Servir Pipoca PPI04V Philco',preco:643.08,precoOrig:'3.215,40',desc:80,vendidos:215,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-ma357gbfhypu7c'},
  {id:92,nome:'Conjunto de Panelas de Ferro Fundido Esmaltado 10 Peças - Frigideira e Panelas Antiaderentes',preco:598,precoOrig:'2.990,00',desc:80,vendidos:37,img:'../img/produto-92-1.jpg'},
  {id:94,nome:'Bicicleta Bike Ergometrica Spinning Academia Fitness Profissional 120kg',preco:147,precoOrig:'735,00',desc:80,vendidos:0,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-m78dqlbsalos96'},
  {id:95,nome:'YESOP Máquina De Gelo Portátil Preto 12kg/dia 127V Produção Rápida Turbo Ice Para Casa E Bar',preco:48.05,precoOrig:'398,05',desc:88,vendidos:200,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-m9o8h6dyt2d529'},
  {id:96,nome:'Aparelho de Jantar/Chá Oxford Ryo Maresia 30 Peças',preco:69.9,precoOrig:'497,90',desc:86,vendidos:7643,img:'https://down-br.img.susercontent.com/file/sg-11134201-7rd5p-m7uwvu85tnp9ae'},
  {id:97,nome:'Jogo de Jantar Canyon Porcelana Decorada 20 Peças Tramontina',preco:69.9,precoOrig:'596,90',desc:88,vendidos:877,img:'https://down-br.img.susercontent.com/file/sg-11134201-81zwa-mimr7kh9srno54'},
  {id:98,nome:'Conjunto de 12 Copos De Cristal P/ Long Drink 490Ml Proper Effect',preco:69.9,precoOrig:'397,90',desc:82,vendidos:1,img:'https://down-br.img.susercontent.com/file/d8f8f5450da9553d8273c5ffe8a1ee61'},
  {id:99,nome:'Kit Compre 1 Leve 2 Camisa Seleção Portugal Copa 2026 (Masculina/Feminina)',preco:129.9,precoOrig:'620,00',desc:79,vendidos:14720,img:'../img/portugal/7.png'},
  {id:116,nome:'Smart TV DLED 32 HD Multi Roku 3HDMI 2USB Wi-Fi - TL052M',preco:879.0,precoOrig:'1.321,35',desc:33,vendidos:3120,img:'../img/tv-multi-slide-1.webp'},
  {id:117,nome:'Fogão Atlas Mônaco Top Glass 4 Bocas Mesa de Vidro Temperado Preto',preco:589.0,precoOrig:'1.299,00',desc:55,vendidos:4250,img:'../img/fogao-atlas-slide-1.webp'},
  {id:118,nome:'Conjunto Sala de Jantar Mesa Tampo Chanfrado com 4 Cadeiras Estofadas Suede Slim',preco:449.0,precoOrig:'990,00',desc:55,vendidos:1540,img:'../img/mesa-jantar-slide-1.webp'},
  {id:119,nome:'Combo Fardo Mega Fraldas Supreme Care + 4 Pacotes Lenços Umedecidos Toque Suave',preco:149.0,precoOrig:'310,00',desc:52,vendidos:8930,img:'../img/fraldas-slide-1.webp',variacoes:{"tamanho":{"com_imagem":false,"label":"Tamanho da Fralda","opcoes":[{"nome":"Tamanho M (5,5 a 9,5kg)","preco":149.00,"preco_antigo":310.00},{"nome":"Tamanho G (9 a 12,5kg)","preco":149.00,"preco_antigo":310.00},{"nome":"Tamanho XG (12 a 15kg)","preco":149.00,"preco_antigo":310.00},{"nome":"Tamanho XXG (+14kg)","preco":149.00,"preco_antigo":310.00}]}}},
  {id:120,nome:'Sofá Retrátil e Reclinável 3 Lugares 2,10m Suede Veludo com Molas Ensacadas e Pillow Top',preco:890.0,precoOrig:'1.890,00',desc:53,vendidos:1120,img:'../img/sofa-slide-1.webp'},
  {id:121,nome:'Travesseiro Cervical Ortopédico Abranuv Pro 2.0 Espuma de Memória Viscoelástica',preco:89.9,precoOrig:'219,00',desc:59,vendidos:6740,img:'../img/travesseiro-slide-1.webp'},
  {id:122,nome:'Panela de Pressão Elétrica Digital 5L Painel Touch Inox com 10 Travas de Segurança',preco:289.0,precoOrig:'599,00',desc:52,vendidos:2380,img:'../img/panela-pressao-slide-1.webp'},
  {id:123,nome:'Lavadora de Alta Pressão Portátil Sem Fio 48V com Maleta, 2 Baterias e Canhão de Espuma',preco:197.0,precoOrig:'499,00',desc:61,vendidos:5490,img:'../img/lavadora-slide-1.webp'},
  {id:124,nome:'Livro Infantil Interativo Bilíngue Falante com Som ao Toque - Português e Inglês com Caneta Tátil',preco:127.9,precoOrig:'259,90',desc:51,vendidos:2400,img:'../img/livro-interativo-slide-1.webp',variacoes:{"cor":{"com_imagem":true,"label":"Cor / Modelo","opcoes":[{"imagem":"../img/livro-interativo-slide-1.webp","nome":"Amarelo (Unissex)","preco":127.90,"preco_antigo":259.90},{"imagem":"../img/livro-interativo-slide-3.webp","nome":"Rosa","preco":127.90,"preco_antigo":259.90},{"imagem":"../img/livro-interativo-slide-4.webp","nome":"Azul","preco":127.90,"preco_antigo":259.90}]}}},
  {id:4,nome:'Caixa De Som Boombox 3 Bluetooth Preta JBL',preco:149.0,precoOrig:'899,00',desc:83,vendidos:8420,img:'../img/jbl-boombox3-1.jpg'},
  {id:8,nome:'Caixa de Som Amplificada AIWA Party Box AWS-PB-07 Bluetooth 100W RMS com Show de Luzes RGB e Bateria Recarregável',preco:149.99,precoOrig:'990,00',desc:85,vendidos:6310,img:'https://down-br.img.susercontent.com/file/br-11134207-7r98o-m688tqkxlw36d9'},
  {id:100,nome:'Apple iPhone 15, 15 Plus, 15 Pro e 15 Pro Max (Vitrine Premium)',preco:95.90,precoOrig:'2.314,40',desc:96,vendidos:12400,img:'../img/iphones/15/preto/1.png'},
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
