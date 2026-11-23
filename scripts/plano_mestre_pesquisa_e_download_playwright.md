# Dossiê de Engenharia & Fila Mestre de Pesquisa e Download (MCP Playwright - Profile 42)

**Autor:** Bruno (CTO Stone Shop - Modo Zika Blindado)  
**Data:** 19/11/2026 (Horário de Brasília)  
**Status:** Auditado, Corrigido e Estruturado para Execução  
**Referência Mestre:** `auditoria-103-produtos.pdf` (21 Páginas) & `GEMINI.md`

---

## 1. Raio-X das Correções Imediatas Executadas em Código

| Item | Problema Diagnosticado | Solução Aplicada no Código | Status |
|---|---|---|---|
| **Avatares Masculinos em Produtos Femininos (Print do Usuário)** | No produto `produto-104` (Chinelo Feminino Strass), aparecia um homem idoso de boné (`mulher_52`) e o logo STILOZ (`mulher_53`) na produção porque o deploy anterior servia a pasta antiga `mulheres_brasil`. | Criado o banco `img/reviews-avatars/mulheres_validadas/` com **75 mulheres brasileiras reais do TikTok** auditadas visualmente uma a uma. Aplicado em todos os 11 produtos femininos. | **BLINDADO & AUDITADO** |
| **Resíduos de Avatares Externos em P108 e P109** | P108 (Escova 5 em 1) e P109 (Modelador de Cachos) continham 32 avaliações apontando para `creator-1.jpg`. | Substituídos todos os 64 avatares pelas imagens do banco `mulheres_validadas/`. | **100% HOMOLOGADO** |
| **Carrossel Oculto da Scooter (P102)** | Em `js/videos-criadores.js`, a função de desacoplamento filtrava o vídeo da descrição (`scooter-preta.mp4`), zerando o dataset e forçando `targetContainer.style.display = 'none'`. | Lógica corrigida na linha 6264: se o filtro zerar os vídeos, o container NUNCA é ocultado, mantendo a exibição contínua. | **CORRIGIDO** |
| **Imagens de Catálogo em Avaliações de Compradores** | P21 (Bola Penalty), P74 (Camisa Brasil) e P99 (Camisa Portugal) tinham renders 3D e fotos de catálogo em fundo branco fingindo ser unboxing de compradores. | Renders de catálogo expurgados das avaliações desses 3 produtos. Fila de unboxing real estruturada abaixo. | **EXPURGADO** |

---

## 2. Fila Mestre de Pesquisa e Download via MCP Playwright (Profile 42)

Toda a extração DEVE ser realizada pelo **MCP Playwright** conectado ao perfil logado **Max Digital (Profile 42)** no TikTok Shop e TikTok Web, com fallback exclusivo no Mercado Livre para unboxing de compradores reais.

### FILA A: 12 PRODUTOS COM VÍDEOS DE CRIADORES 0 BYTES / QUEBRADOS NO CATBOX
*Estes 12 produtos tiveram links no Catbox retornando 0 bytes ou sem reprodução. Devem ser baixados vídeos reais do TikTok com criadores brasileiros demonstrando o produto exato:*

1. **P4 · Caixa De Som Boombox 3 Bluetooth Preta JBL**
   - **Busca TikTok:** `"JBL boombox 3" review som grave unboxing`
   - **Critério:** Criadores reais ligando e testando o grave da Boombox 3 (sem corte para outros modelos).
   - **Meta:** 10 a 15 vídeos MP4 reais.

2. **P5 · Fritadeira Elétrica Visio Fry Elgin 5L 1700W Air Fryer Digital Cinza**
   - **Busca TikTok:** `"air fryer elgin visio fry" 5L receita review`
   - **Critério:** Air fryer cinza com visor transparente cozinhando alimentos na bancada.
   - **Meta:** 10 a 15 vídeos MP4 reais.

3. **P7 · Caixa de Som AIWA Bluetooth**
   - **Busca TikTok:** `"caixa de som aiwa" bluetooth teste review`
   - **Critério:** Caixa AIWA portátil real tocando música.
   - **Meta:** 10 vídeos MP4 reais.

4. **P8 · Caixa de Som Amplificada AIWA Party Box AWS-PB-07 Bluetooth 100W RMS com Luzes RGB**
   - **Busca TikTok:** `"aiwa party box" AWS-PB-07 review som luzes`
   - **Critério:** Party Box AIWA grande com painel de luzes LED pulsando.
   - **Meta:** 10 a 15 vídeos MP4 reais.

5. **P9 · Ar Condicionado Portátil HQ 8.500 BTU/h Frio Monofásico Branco HQ-AP8500FW**
   - **Busca TikTok:** `"ar condicionado portatil HQ" 8500 btu esfria mesmo`
   - **Critério:** Aparelho portátil HQ branco instalado no quarto/sala com duto na janela.
   - **Meta:** 10 vídeos MP4 reais.

6. **P12 · Piscina Splash Fun Redonda Inflável 2400 Litros - Mor**
   - **Busca TikTok:** `"piscina mor 2400" inflavel montagem enchendo quintal`
   - **Critério:** Famílias montando ou usando a piscina redonda Mor de 2400L com anel inflável.
   - **Meta:** 10 a 15 vídeos MP4 reais.

7. **P13 · Piscina Inflável Redonda Mor 1000 Litros Splash Fun Azul**
   - **Busca TikTok:** `"piscina mor 1000" litros inflavel criancas quintal`
   - **Critério:** Piscina redonda Mor pequena de 1000L com crianças se refrescando.
   - **Meta:** 10 vídeos MP4 reais.

8. **P17 · Kit 6 Cadeira de Praia Aço Mor 110kg Resistente CORES SORTIDAS**
   - **Busca TikTok:** `"cadeira de praia mor" 110kg resistente praia teste`
   - **Critério:** Criadores na praia ou piscina usando as cadeiras Mor coloridas de aço.
   - **Meta:** 15 a 20 vídeos MP4 reais.

9. **P18 · Kit Praia 4 Cadeiras Sortidas Reclinável + Guarda Sol Fashion + Saca Areia Mor**
   - **Busca TikTok:** `"kit praia mor" cadeira reclinavel guarda sol montando praia`
   - **Critério:** Conjunto completo na areia da praia montado.
   - **Meta:** 15 vídeos MP4 reais.

10. **P35 · Caixa de Som JBL Boombox 4 Bluetooth 210W Preta Bivolt**
    - **Busca TikTok:** `"jbl boombox" teste potencia som festa`
    - **Critério:** Caixa JBL Boombox preta de alta potência ao ar livre ou em festa.
    - **Meta:** 10 vídeos MP4 reais.

11. **P41 · Fritadeira Air Fryer Forno Oven 12L Mondial Preto e Inox AFON-12L-BI**
    - **Busca TikTok:** `"air fryer forno mondial 12l" oven frango assando`
    - **Critério:** Forno Air Fryer Mondial de 12 litros com porta de vidro e grelhas duplas.
    - **Meta:** 10 a 15 vídeos MP4 reais.

12. **P116 · Smart TV DLED 32 HD Multi Roku 3HDMI 2USB Wi-Fi - TL052M**
    - **Busca TikTok:** `"smart tv multi roku 32" unboxing instalando imagem`
    - **Critério:** TV Multi/Multilaser de 32 polegadas com interface Roku TV ligada na sala.
    - **Meta:** 10 vídeos MP4 reais.

---

### FILA B: 13 PRODUTOS COM IMAGENS DE UNBOXING REAL PENDENTES (EXPURGO DE CATÁLOGO)
*Estes produtos necessitam de extração obrigatória de fotos de unboxing doméstico (chão da sala, bancada, mesa, desembalando) de compradores reais no TikTok Shop ou Mercado Livre:*

1. **P21 · Bola De Futebol De Campo Penalty Bravo XXV**
   - **Extração ML/TikTok Shop:** Fotos de clientes com a bola na grama, na mão ou na caixa recebida pelos Correios.
2. **P74 · Kit Camisa Seleção Brasil Home Copa 2026**
   - **Extração ML/TikTok Shop:** Torcedores vestindo a camisa amarela da Seleção no quarto/espelho ou com ela esticada na cama.
3. **P99 · Kit Camisa Seleção Portugal Copa 2026**
   - **Extração ML/TikTok Shop:** Compradores mostrando o manto de Portugal recebido (número 7 / Cristiano Ronaldo), detalhes do escudo e tecido.
4. **P8 · Caixa AIWA Party Box AWS-PB-07**
   - **Extração ML/TikTok Shop:** Fotos reais de clientes com a caixa na sala, na varanda ou no churrasco.
5. **P31 · Caixa De Som Sabala DR-909 200W**
   - **Extração ML/TikTok Shop:** Fotos reais de clientes mostrando a caixa Sabala desencaixotada.
6. **P35 · Caixa JBL Boombox 4 210W**
   - **Extração ML/TikTok Shop:** Fotos de clientes desembalando a JBL na mesa ou no chão.
7. **P61 & P83 · Caixa de Som Joog Break X1 Tela Touch 13"**
   - **Extração ML/TikTok Shop:** Fotos de clientes mostrando a tela touch ligada e os microfones sem fio reais.
8. **P117 · Fogão Atlas Mônaco Top Glass 4 Bocas Mesa de Vidro**
   - **Extração ML/TikTok Shop:** Fotos reais de clientes com o fogão instalado na cozinha (bancada, azulejo, botões acesos).
9. **P118 · Conjunto Sala de Jantar Mesa Tampo Chanfrado com 4 Cadeiras**
   - **Extração ML/TikTok Shop:** Fotos reais de compradores com a mesa e cadeiras montadas na sala de jantar de suas casas.
10. **P120 · Sofá Retrátil e Reclinável 3 Lugares 2,10m Suede Veludo**
    - **Extração ML/TikTok Shop:** Fotos reais de compradores com o sofá aberto na sala de estar, almofadas e tecido visíveis.
11. **P122 · Panela de Pressão Elétrica Digital 5L Painel Touch Inox**
    - **Extração ML/TikTok Shop:** Fotos reais de clientes com a panela na bancada da cozinha cozinhando feijão/carne.
12. **P123 · Lavadora de Alta Pressão Portátil Sem Fio 48V com Maleta**
    - **Extração ML/TikTok Shop:** Fotos de clientes lavando carro, moto ou calçada com a pistola portátil e a maleta aberta.

---

### FILA C: DESACOPLAMENTO DE MÍDIA CRUZADA EM CRIADORES (POOL EXCLUSIVO POR NICHO)
*Desconectar os pools genéricos e atribuir vídeos estritamente do nicho do produto:*

- **Churrasqueiras (P14, P15, P16):** Exclusivamente vídeos de churrasco, espetos girando e carne assando. Proibido panela elétrica ou fritadeira.
- **Bicicletas e Esteiras (P6, P20, P25, P56, P94):** Cada tipo de bike com seu vídeo (spinning para P6/P94, aro 29 MTB para P20, BMX infantil para P25, esteira para P56).
- **Mundo Gamer (P55 Switch, P114 Arcade):** Vídeos de gameplay no Switch portátil e no painel arcade com manche e botões luminosos.
- **Pet Shop (P113 Comedouro Gato/Cachorro):** Vídeos reais de cães e gatos comendo no suporte elevado com tigela inclinada.
