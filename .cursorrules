# Regra Global de Extração de Produtos TikTok Shop (Bruno CTO - Modo Zika Blindado)

> trigger: always_on quando o usuário enviar qualquer link do TikTok Shop (`https://shop.tiktok.com/...` ou `vt.tiktok.com/...`)
> Arquivo Mestre de Regras e Diretrizes do Fluxo: `c:\Users\Dell\Downloads\ds\GEMINI.md`

Sempre que o usuário enviar um link de produto do TikTok Shop de QUALQUER NICHO (Geladeira, Televisão, Eletrônicos, Calçados, Vestuário, Beleza, Casa, etc.), execute o fluxo completo de forma 100% autônoma, sem pedir permissão e sem enrolação corporativa:

---

### Doutrina Fundamental: Fidelidade Rigorosa 1:1 ao Anúncio do Vendedor (Tolerância Zero a Invenção de Dados)

O produto clonado deve ser o espelho exato do anúncio oficial do vendedor no TikTok Shop. É **terminantemente proibido inventar dados, inventar tabelas fakes ou reutilizar mídias de outros produtos como fallback**.

---

### Fluxo de Execução Obrigatório Multi-Nicho:

#### 1. Extração de Dados Oficiais via Playwright Headless & Sessão Logada:
- **REGRA INEGOCIÁVEL DE SESSÃO / CONTEXTO DE NAVEGAÇÃO (PROIBIDO NAVEGADOR DESLOGADO/INCÓGNITO)**:
  - O TikTok Shop impõe barreiras anti-bot (Captcha UniSec / Slardar e telas de login forçado) em qualquer navegador deslogado. Reutilizar sempre a sessão logada ativa.
- Puxar o título completo e limpo do produto.
- Puxar o preço promocional, preço original (riscado) e desconto %.
- Puxar contagem real de vendidos (ex: `23.7K vendidos`) e nota média oficial (ex: `4.8`).
- Puxar todas as variações (voltagens, cores, modelos, tamanhos, capacidades com fotos reais).
- Puxar todas as fotos oficiais da galeria em alta resolução (800x800).

#### 2. Regra Inegociável para Vídeo Oficial do Vendedor (`product_video`):
- **SÓ EXISTE SE O VENDEDOR REALMENTE CADASTROU VÍDEO OFICIAL**:
  - Se o anúncio oficial do vendedor no TikTok Shop possui vídeo demonstrativo do produto na descrição/detalhes, extraia em alta definição para `video/produto-[ID]-demo.mp4` e gere o poster sincronizado no frame `00:00:00.2` via FFmpeg.
  - **SE O VENDEDOR NÃO COLOCOU VÍDEO NO ANÚNCIO: OMITIR O BLOCO DE VÍDEO POR COMPLETO!**
  - **PROIBIÇÃO ABSOLUTA**: Jamais coloque vídeo de outro produto (ex: vídeo de chinelo em eletrônico ou TV). Se não tem vídeo oficial do produto, o bloco de vídeo NÃO ENTRA no HTML.

#### 3. Regra Inegociável para Tabela / Guia de Tamanhos (`size_guide`):
- **SEGUIR ESTRITAMENTE O QUE O VENDEDOR CADASTROU**:
  - **Vestuário & Calçados (Moda Feminina/Masculina)**: O TikTok Shop possui a seção nativa de "Guia de tamanhos". O vendedor sobe uma imagem da tabela dele (ex: *33/34 - 23 cm | 35/36 - 24 cm*) ou preenche a grade de medidas corporais (comprimento, busto, cintura). Nesses produtos, extrair **rigorosamente a tabela do vendedor** (imagem oficial ou tabela HTML idêntica à dele).
  - **Eletrônicos, Gadgets, Beleza, Casa & Outros Nichos**: No TikTok Shop, essas categorias **NÃO POSSUEM Guia de Tamanhos** no painel do vendedor.
    - Se o vendedor NÃO colocou tabela de especificações no anúncio dele, é **TERMINANTEMENTE PROIBIDO INVENTAR TABELA OU DIMENSÕES ARTIFICIAIS** (como tabela de TV com padrão VESA em projetor/celular)!
    - O bloco de tabela simplesmente **NÃO É RENDERIZADO** no HTML, e a página transita direto de `Detalhes` para `Descrição`, exatamente igual ao app oficial do TikTok Shop!

#### 4. Regra Inegociável para a Descrição do Produto:
- **100% FIEL E EXCLUSIVA DO PRODUTO DO VENDEDOR**:
  - Extrair o texto oficial exato cadastrado pelo vendedor: destaques reais, ficha técnica, itens inclusos na embalagem, especificações e termos de garantia.
  - **PROIBIDO misturar descrições ou atributos de outros produtos ou nichos**.
  - O texto oficial é formatado dentro do container padrão TikTok Shop com:
    - Altura inicial limitada a ~98px (`.description-expandable-container`).
    - Gradiente translúcido de fade-out no final (`.desc-fade-overlay`).
    - Botão centralizado em texto limpo com ícone SVG: `Ver mais ∨` que expande para `Ver menos ⌃` (`toggleDescricaoCompleta()`).

#### 5. Múltiplos Vídeos de Criadores DIFERENTES (Zero Repetição de Rosto/Cena):
- **Descoberta Automatizada via Playwright Google**: `site:tiktok.com "[NOME DO PRODUTO]"`.
- **Download Limpo via TikWM API**: Zero marca d'água flutuante.
- **Posters Sincronizados**: Extrair frame `00:00:00.2` via FFmpeg.
- **PROIBIDO GERAR VÍDEO FAKE COM FOTO TREMENDO / ZOOMPAN**: Gravações humanas reais de teste/unboxing do produto específico.

#### 6. Avaliações dos Clientes com Mídias Reais do Produto:
- Estritamente avaliações que contenham fotos/vídeos reais de compradores legítimos do produto.
- Zero clones artificiais e zero hotlinking de links temporários assinados da CDN (baixar sempre para `img/`).

#### 7. Carrossel "Vídeos de Criadores" Dinâmico & Precedência no `videos-criadores.js`:
- Declaração canônica no HTML: `<div id="creators-section" class="creators-section"></div>`.
- O script `videos-criadores.js` instancia os cards e carrossel dinamicamente em tempo de execução.

#### 8. Seção "Sobre este produto" Padronizada & Calibrada (Paridade 1:1 TikTok Shop):
- **SUBSEÇÃO 1: Detalhes Compactos do Vendedor**:
  - Labels à esquerda (`color: #73747b; font-size: 12.5px; width: 135px; min-width: 135px;`).
  - Valores à direita (`color: #161823; font-size: 13px; font-weight: 400;`).
  - Espaçamento vertical ultra compacto (`gap: 3px; padding: 2px 0;`).
  - 4 primeiros atributos visíveis e os restantes com classe `.is-hidden.toggleable-row`.
  - Link azul à esquerda: `<button type="button" class="btn-detalhes-link" id="btn-toggle-detalhes" onclick="toggleProductDetails(this)">Ver mais</button>`.
- **SUBSEÇÃO 2: Vídeo Compacto Oficial (Condicional: Somente se existir no anúncio)**:
  - Card horizontal de 230px de altura com cantos arredondados de 10px e fundo preto sólido (`#000000`).
  - Vídeo centralizado com faixas pretas sólidas nas laterais (*pillarbox*).
  - Triângulo branco de Play clássico (`▶`) centralizado com sombra suave.
  - Barra inferior com play/pause, tempo `00:00`, linha de progresso fina, duração total e botão fullscreen `[ ]`.
- **SUBSEÇÃO 3: Guia de Tamanhos / Tabela (Condicional: Somente se existir no anúncio)**:
  - Tabela limpa ou imagem gráfica oficial do vendedor, alinhada rigorosamente aos dados do vendedor.
- **SUBSEÇÃO 4: Descrição Oficial com Fade-out de Opacidade e Toggle**:
  - Container `.description-expandable-container` com altura inicial limitada a 98px.
  - Overlay `.desc-fade-overlay` com gradiente suave de transparência branca (`linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(255,255,255,0.8) 55%, #ffffff 100%)`).
  - Botão centralizado: `<button type="button" class="btn-toggle-desc" id="btn-toggle-desc" onclick="toggleDescricaoCompleta()"><span id="btn-toggle-desc-text">Ver mais</span> <svg class="toggle-icon-desc" ...><polyline points="6 9 12 15 18 9"></polyline></svg></button>`.

#### 9. Integridade do DOM, Sincronização e Deploy:
- Tag depth rigorosamente igual a 0 (`diff: 0`).
- Atualizar cache busters em todas as páginas via `scripts/update_cache_buster.py`.
- Sincronizar para `C:\Users\Dell\Downloads\stone_shop_clone` via `scripts/sync_to_clone.py`.
- Deploy na Vercel e apontamento do alias `stoneshopclone.vercel.app`.
- **PROIBIDO ENVIAR LOCALHOST**: Sempre entregar HTTPS oficial.
