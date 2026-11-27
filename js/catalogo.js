// Catálogo gerado automaticamente — usa apenas imagens estáticas (não vídeo)
const CATALOGO_PRODUTOS = [
  {id:144,nome:"Câmera Infantil Instantânea que Imprime a Foto na Hora Sem Tinta + 3 Bobinas Térmicas e Alça",preco:37.89,precoOrig:'199,90',desc:81,vendidos:4829,img:"../img/camera-144-slide-1.webp"},
  {id:129,nome:"Escova Elétrica Giratória de Limpeza Sem Fio 9 em 1 Impermeável c/ Cabo Extensor Retrátil USB",preco:29.89,precoOrig:'159,90',desc:81,vendidos:6184,img:"../img/escova-129-slide-1.webp"},
  {id:127,nome:"Carrinho Controle Remoto Drift 4x4 Turbo que Solta Fumaça com LED + Kit Pneus Drift e Cones",preco:49.89,precoOrig:'249,90',desc:80,vendidos:3918,img:"../img/drift-127-slide-1.webp"},
  {id:145,nome:"Combo Mala de Bordo Rígida ABS Giro 360° Padrão ANAC + Frasqueira de Viagem (Kit 2 Peças)",preco:69.89,precoOrig:'399,90',desc:83,vendidos:4376,img:"../img/mala-145-slide-1.webp"},
  {id:128,nome:"Mesa Dobrável Portátil Vira Maleta 1,80m Reforçada com Alça e Trava (Ceia, Churrasco e Camping)",preco:67.89,precoOrig:'329,90',desc:79,vendidos:3695,img:"../img/mesa-128-slide-1.webp"},
  {id:135,nome:'Smartwatch Série 10 W99+ Pro Tela Super AMOLED NFC ChatGPT GPS Faz e Recebe Ligações',preco:89.9,precoOrig:'349,90',desc:74,vendidos:9200,img:'../img/smartwatch-135-slide-1.webp'},
  {id:134,nome:"Caneta Aparadora e Depiladora de Sobrancelhas Elétrica Recarregável USB c/ Luz LED Indolor",preco:11.89,precoOrig:'49,90',desc:76,vendidos:5191,img:"../img/sobrancelha-134-slide-1.webp"},
  {id:133,nome:'Cordão de Luz Natal Pisca-Pisca 100 LEDs 9m 8 Funções Fio Transparente Decoração',preco:9.69,precoOrig:'39,90',desc:76,vendidos:6454,img:'../img/pisca-133-slide-1.webp'},
  {id:132,nome:"Cinta Modeladora Feminina Redutora Abdominal M+ 6 Níveis de Ajuste Tecido Respirável",preco:19.79,precoOrig:'89,90',desc:78,vendidos:4617,img:"../img/cinta-132-slide-1.webp"},
  {id:126,nome:"Patinete Elétrico Infantil Dobrável com Luzes LED nas Rodas e Guidão Ajustável em 3 Alturas",preco:47.89,precoOrig:'199,90',desc:76,vendidos:3842,img:"../img/patinete-126-slide-1.webp"},
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
  {id:102,nome:"Scooter Elétrica TUI 1000w | 2 Lugares | Sem CNH | Autonomia 60km",preco:99.9,precoOrig:"2.344,00",desc:82,vendidos:8944,img:"../imagemscooterpreta/D_NQ_NP_2X_712059-MLA99509048862_112025-F.webp"},
  {id:101,nome:"Pneus Pirelli - Encontre a medida ideal para o seu veículo",preco:87.9,precoOrig:"599,00",desc:83,vendidos:13488,img:"https://tyre24.pirelli.com/dynamic_engine/assets/visori/cake/p7cnt.png"},
  {id:52,nome:"Pad 11 Geração A16 256GB Wi-fi Tela 11pol Original Novo Lacrado com Garantia  de 1 ano",preco:94.9,precoOrig:"497,90",desc:81,vendidos:7654,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-mdh7rladn00h24"},
  {id:5,nome:"Fritadeira Elétrica Visio Fry Elgin 5L 1700w Air Fryer Digital Cinza",preco:67.9,precoOrig:"399,90",desc:83,vendidos:5849,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-mh9e1c37asxxe2"},
  {id:7,nome:"Caixa de Som AIWA",preco:69.9,precoOrig:"597,00",desc:88,vendidos:7894,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rceh-lrrqafsspb32c2"},
  {id:9,nome:"Ar Condicionado Portátil HQ 8.500 BTU/h Frio Monofásico Branco HQ-AP8500FW",preco:92.8,precoOrig:"754,44",desc:88,vendidos:10241,img:"https://down-br.img.susercontent.com/file/sg-11134201-7renf-m8lxuc60fdsy07"},
  {id:12,nome:"Piscina Splash Fun Redonda Inflável 2400 Litros - Mor",preco:89.9,precoOrig:"399,00",desc:78,vendidos:9899,img:"../img/produto-12-1.jpg"},
  {id:13,nome:"Piscina Inflável Redonda Mor 1000 Litros Splash Fun Azul",preco:49.9,precoOrig:"169,90",desc:71,vendidos:10004,img:"https://down-br.img.susercontent.com/file/sg-11134201-82260-mhoz9j95dloj8d"},
  {id:14,nome:"Churrasqueira Assador a Gás GLP Rotativo Arke 5 Espetos AGR-05 Bivolt",preco:89.9,precoOrig:"599,90",desc:85,vendidos:9874,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rdwx-lzpm7626yvg7c9"},
  {id:15,nome:"Churrasqueira Portátil A Carvão Biscuitt Steak Master Smoke & Fire USB Com Bag",preco:69.9,precoOrig:"349,90",desc:80,vendidos:7543,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-lqnmb7oulw6f02"},
  {id:16,nome:"Churrasqueira Resistente Modelo Rodeio Bacia Esmaltada Casa Praia Piscina Verão Lazer Preta - Mor",preco:64.9,precoOrig:"299,90",desc:78,vendidos:7548,img:"https://down-br.img.susercontent.com/file/sg-11134201-7reng-m1ya6at9aqw05a"},
  {id:17,nome:"Kit 6 Cadeira de Praia Aço Mor 110kg Resistente CORES SORTIDAS Oferta",preco:89,precoOrig:"399,90",desc:78,vendidos:5668,img:"https://down-br.img.susercontent.com/file/sg-11134201-7reoq-m8kskp1ohv2vcf"},
  {id:18,nome:"Kit Praia 4 Cadeiras Sortidas Reclinável + Guarda Sol Fashion + Saca Areia+ Carrinho+ Coller 18 Lts",preco:84.9,precoOrig:"499,00",desc:83,vendidos:10706,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-mhuv620f45j7bf"},
  {id:19,nome:"Tablet Vision TAB 7 Stitch + Capa e Bolsa - Octa-Core 3GB RAM 64GB Android 14 Go Wi-Fi IPS Positivo",preco:74.9,precoOrig:"449,00",desc:83,vendidos:4987,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m84xjaeqhbf556"},
  {id:20,nome:"Bicicleta  Aro 29 GT Sprint MX7 24V index Freio Disco Alumínio Suspensão Aero MTB",preco:97.9,precoOrig:"699,00",desc:86,vendidos:4984,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-me910y70d7nmf6"},
  {id:21,nome:"Bola De Futebol De Campo Penalty Bravo Xxv",preco:34.9,precoOrig:"129,90",desc:73,vendidos:5346,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rbkz-m5oo5ljc9heg98"},
  {id:22,nome:"Colchão Inflável Suporta 300kg Casal Camping Praia + Bomba de Ar Manual Bestway",preco:49.9,precoOrig:"195,90",desc:75,vendidos:5531,img:"../img/colchao-bestway-oficial-1.jpg"},
  {id:23,nome:"Conjunto De 24 Potes Herméticos Croix Com Tampa E Trava",preco:24.73,precoOrig:'119,90',desc:79,vendidos:6691,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-mci5ecdv44s2e5"},
  {id:24,nome:"Triciclo Infantil 4 em 1 Multifuncional Carrinho de Bebê Com Empurrador e CapotaSolar-Kababy",preco:84.9,precoOrig:"399,00",desc:79,vendidos:4897,img:"../img/produto-24-slide-1.jpg"},
  {id:25,nome:"Bicicleta Aro 20 Bmx infantil GottBikes Freio V-Brake",preco:79.9,precoOrig:"449,00",desc:82,vendidos:4769,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-mer4ub5zgb9c1b"},
  {id:26,nome:"Carrinho de Bebê Guarda Chuva Passeio Leve e Dobrável Mega Compras Compacto, Seguro,Cinto",preco:69.9,precoOrig:"299,90",desc:77,vendidos:4458,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m5bgd8rac7dc02"},
  {id:34,nome:"Lava Louças Praxis Portátil LLPP Semi-Automática Bivolt",preco:69.8,precoOrig:"397,90",desc:82,vendidos:9864,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m850ox58do8h8b"},
  {id:35,nome:"Caixa de Som JBL Boombox 4 Bluetooth 210W Preta Bivolt",preco:67.43,precoOrig:"497,90",desc:81,vendidos:8569,img:"https://down-br.img.susercontent.com/file/sg-11134201-824i8-mdyu6aqj7g1td8"},
  {id:36,nome:"Celular Xiaomi Poco X7 Pro 5g Dual Sim 512gb Amarelo 12ram 50mpx",preco:92.8,precoOrig:"497,90",desc:81,vendidos:9853,img:"https://http2.mlstatic.com/D_NQ_NP_2X_884323-MLA99500626568_112025-F.webp"},
  {id:38,nome:"Kit Lattafa Yara Collection Feminino Edp - Perfume 4x25ml original",preco:69.9,precoOrig:"397,90",desc:82,vendidos:5515,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-mh12vhr254hs6c"},
  {id:39,nome:"Secador de Cabelos Philco PSC3500 4 em 1 Dobrável 1450W",preco:68.7,precoOrig:"397,90",desc:83,vendidos:9872,img:"https://down-br.img.susercontent.com/file/sg-11134201-824hh-mfio0pwmo0su97"},
  {id:40,nome:"Micro-ondas Mondial Mo-01-21-e 1200w 21 Litros",preco:84.9,precoOrig:"389,90",desc:78,vendidos:8953,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m9zqs2hxtuki59"},
  {id:41,nome:"Fritadeira Air Fryer Forno Oven 12L Mondial Preto e Inox0W AFON-12L-BI",preco:54.73,precoOrig:'299,90',desc:82,vendidos:8391,img:"https://down-br.img.susercontent.com/file/sg-11134201-7raui-mb4awu05e15c16"},
  {id:45,nome:"Prancha Pro 480 Turbo MQ Professional Bivolt",preco:69.9,precoOrig:"399,90",desc:83,vendidos:8654,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rept-m80tiqdhkwwh87"},
  {id:46,nome:"Panela de Pressão Elétrica Electrolux por Rita Lobo 6L Preta Experience Digital (PCC20)",preco:69.9,precoOrig:"399,90",desc:83,vendidos:9831,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rfhx-m9yig7n5t2mn18"},
  {id:47,nome:"Extratora e Higienizadora Portátil WAP Spot Cleaner 1400W Borrifa Esfrega e Extrai",preco:69.9,precoOrig:"399,90",desc:83,vendidos:9314,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rbn7-lqeu1vzxvsrqba"},
  {id:53,nome:"Starlink V4 Internet Satélite Wi-fi 6 Alta Velocidade Nacional Homologada Anatel (Starlink Padrão)",preco:94.9,precoOrig:"497,90",desc:81,vendidos:5801,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-me8xwns12tqb8f"},
  {id:54,nome:"Purificador Eletrônico Compacto Efficient Painel Digital Bivolt Cinza (PE11X)",preco:69.9,precoOrig:"497,90",desc:86,vendidos:9876,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rdxh-mdeoo0q0wuft89"},
  {id:55,nome:" SWITCH  DESBLOQUEADO + 10 JOGOS DA SUA ESCOLHA COM CARTÃO DE MEMORIA 128 GB",preco:64.9,precoOrig:"497,90",desc:87,vendidos:5462,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m024asxqvazr6b"},
  {id:58,nome:"Caixa de som original Alaxe Echo Dot 5 geração com envio imediato e melhor preço",preco:69.9,precoOrig:"397,90",desc:82,vendidos:9876,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-mgby6v6yabr9ad"},
  {id:63,nome:"Smartwatch Redmi Watch 5 Lite GPS Preto Pulseira",preco:69.9,precoOrig:"397,90",desc:82,vendidos:9853,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rdyw-mc9fnkgv7dqz24"},
  {id:64,nome:"Bateria Auxiliar De Partida Portátil Com Bomba De Ar de Rosquear",preco:69.9,precoOrig:"397,90",desc:82,vendidos:8765,img:"https://down-br.img.susercontent.com/file/sg-11134201-8260z-mju7shogkd8jf5"},
  {id:65,nome:"Sofá 3 Lugares Retrátil e Reclinável Cama inBox Senses 2,00m Velusoft Cinza",preco:99.9,precoOrig:"697,90",desc:86,vendidos:8765,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rdxn-lzou0oyl6coa73"},
  {id:68,nome:"Jogo de Panelas Cerâmica Kit 5 Peças Antiaderente Tampa Vidro",preco:44.73,precoOrig:'249,90',desc:82,vendidos:9052,img:"https://down-br.img.susercontent.com/file/br-11134207-81z1k-mebnfn94x2pt4c"},
  {id:75,nome:"Kit 10 Camisetas Dry Fit Masculina - Casual - Treino - Academia - Esportes - Exercícios - Corrida",preco:69.9,precoOrig:"397,90",desc:82,vendidos:9843,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rdxr-lyatwes75beuc5"},
  {id:76,nome:"Aparelho Jogo De Jantar 30 Peças Orgânico Petroleum Porto Brasil Carlos Bertolazzi + BRINDE",preco:69.9,precoOrig:"497,90",desc:86,vendidos:9843,img:"https://down-br.img.susercontent.com/file/sg-11134201-8261c-mkckrt97fvgg75"},
  {id:85,nome:"Caixa De Som Karaokê Joog X2 300w Tela 10,1 Com 2 Microfones",preco:39.9,precoOrig:"397,90",desc:90,vendidos:9853,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m8jnvlvc270103"},
  {id:89,nome:"Kit conjunto de panelas de ferro esmaltadas luxo 18 peças",preco:79.9,precoOrig:"697,90",desc:89,vendidos:5432,img:"https://down-br.img.susercontent.com/file/br-11134207-81ztc-mj765kpbq3nla8"},
  {id:90,nome:"Jogo De Panela Avant Space 5 Peças - Tognana Cor Preto",preco:79.9,precoOrig:"647,90",desc:88,vendidos:5324,img:"https://http2.mlstatic.com/D_NQ_NP_747089-MLA96155562431_102025-O.webp"},
  {id:95,nome:"YESOP Máquina De Gelo Portátil Preto 12kg/dia 127V Produção Rápida Turbo Ice Para Casa E Bar",preco:48.05,precoOrig:"398,05",desc:88,vendidos:5259,img:"https://down-br.img.susercontent.com/file/br-11134207-7r98o-m9o8h6dyt2d529"},
  {id:96,nome:"Aparelho de Jantar/Chá Oxford Ryo Maresia 30 Peças",preco:69.9,precoOrig:"497,90",desc:86,vendidos:7643,img:"https://down-br.img.susercontent.com/file/sg-11134201-7rd5p-m7uwvu85tnp9ae"},
  {id:97,nome:"Jogo de Jantar Canyon Porcelana Decorada 20 Peças Tramontina",preco:69.9,precoOrig:"596,90",desc:88,vendidos:4877,img:"https://down-br.img.susercontent.com/file/sg-11134201-81zwa-mimr7kh9srno54"},
  {id:98,nome:"Conjunto de 12 Copos De Cristal P/ Long Drink 490Ml Proper Effect",preco:44.9,precoOrig:"249,90",desc:82,vendidos:4812,img:"https://down-br.img.susercontent.com/file/d8f8f5450da9553d8273c5ffe8a1ee61"},
  {id:119,nome:"Combo Fardo Mega Fraldas Supreme Care + 4 Pacotes Lenços Umedecidos Toque Suave",preco:69.9,precoOrig:"279,90",desc:75,vendidos:8964,img:"../img/fraldas-slide-1.webp","variacoes":{"tamanho":{"com_imagem":false,"label":"Tamanho da Fralda","opcoes":[{"nome":"Tamanho M (5,5 a 9,5kg)","preco":69.9,"preco_antigo":279.9},{"nome":"Tamanho G (9 a 12,5kg)","preco":69.9,"preco_antigo":279.9},{"nome":"Tamanho XG (12 a 15kg)","preco":69.9,"preco_antigo":279.9},{"nome":"Tamanho XXG (+14kg)","preco":69.9,"preco_antigo":279.9}]}}},
  {id:121,nome:"Travesseiro Cervical Ortopédico Abranuv Pro 2.0 Espuma de Memória Viscoelástica",preco:39.9,precoOrig:"159,90",desc:75,vendidos:6765,img:"../img/travesseiro-slide-1.webp"},
  {id:122,nome:"Panela de Pressão Elétrica Digital 5L Painel Touch Inox com 10 Travas de Segurança",preco:79.9,precoOrig:"389,00",desc:79,vendidos:4842,img:"../img/panela-pressao-slide-1.webp"},
  {id:123,nome:"Lavadora de Alta Pressão Portátil Sem Fio 48V com Maleta, 2 Baterias e Canhão de Espuma",preco:79.9,precoOrig:"399,00",desc:80,vendidos:5506,img:"../img/lavadora-slide-1.webp"},
  {id:124,nome:"Livro Infantil Interativo Bilíngue Falante com Som ao Toque - Português e Inglês com Caneta Tátil",preco:21.89,precoOrig:'99,90',desc:78,vendidos:4953,img:"../img/livro-interativo-slide-1.webp","variacoes":{"idioma":{"label":"Edição","opcoes":[{"nome":"Bilíngue Português / Inglês","imagem":"../img/livro-interativo-slide-1.webp","preco":21.89}]}}},
  {id:100,nome:"Apple iPhone 15, 15 Plus, 15 Pro e 15 Pro Max (Vitrine Premium)",preco:95.9,precoOrig:"2.314,40",desc:82,vendidos:12478,img:"../img/iphones/15/preto/1.png"},
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
