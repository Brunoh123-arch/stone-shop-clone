# 🚀 MANUAL DEFINITIVO: Pipeline Automatizado TikTok Shop ➔ Stone Shop Clone

> **Autor:** Bruno (CTO & Fundador Uppi)  
> **Objetivo:** Permitir clonar, extrair e publicar qualquer produto do TikTok Shop para a Stone Shop em qualquer computador com padrão internacional e zero gambiarra.

---

## 🛠️ 1. Pré-Requisitos na Máquina Nova

Antes de rodar em um computador novo, certifique-se de ter instalado:
1. **Node.js** (v18 ou superior): [https://nodejs.org/](https://nodejs.org/)
2. **FFmpeg** instalado e adicionado ao `PATH` do sistema:
   - No Windows: `winget install Gyan.FFmpeg` ou baixe do site oficial.
   - Verifique digitando `ffmpeg -version` no terminal.
3. **Vercel CLI**:
   ```bash
   npm install -g vercel
   vercel login
   ```
4. **Dependências do Projeto**:
   Navegue até a pasta do projeto e instale:
   ```bash
   cd stone_shop_clone
   npm install
   ```

---

## ⚡ 2. Estrutura do Ecossistema

O repositório é composto por:
- `pages/produto-[ID].html`: Páginas dedicadas de cada produto (ex: `produto-104.html`).
- `js/catalogo.js`: Banco de dados do catálogo com todos os produtos, preços e tags.
- `js/videos-criadores.js`: Componente carrossel "Vídeos de criadores (28+)" com player interativo TikTok.
- `index.html`: Página inicial com a grade de recomendados.
- `real.html`, `stone.html`, `api/stone_content.js`: Cópias de sincronização servidas pela API Vercel Serverless.
- `img/`: Diretório com todas as fotos, posters e vídeos MP4 dos produtos.

---

## 🎬 3. O Fluxo de Extração de Vídeos Reais (Anti-Gambiarra)

> ⚠️ **REGRA DE OURO:** NUNCA use fotos estáticas com zoom do FFmpeg para simular vídeo. Isso fica amador e artificial. Use SEMPRE vídeos reais gravados!

### Como obter vídeos reais do TikTok sem marca d'água:
Usamos a API do TikWM, que extrai o vídeo oficial limpo de qualquer post público do TikTok:
```javascript
const apiUrl = `https://www.tikwm.com/api/?url=${encodeURIComponent(tiktokVideoUrl)}`;
const res = await fetch(apiUrl).then(r => r.json());
const videoDownloadUrl = res.data.play; // URL direta do MP4 em alta qualidade
```

### Como gerar a capa (poster) perfeitamente sincronizada:
Para que o card não dê nenhum pulo visual ao clicar, extraímos exatamente o frame `00:00:00.2` do início do vídeo:
```bash
ffmpeg -y -ss 00:00:00.2 -i "img/video-produto.mp4" -vframes 1 -q:v 2 "img/poster-produto.jpg"
```

---

## 📋 4. Passo a Passo para Adicionar um Novo Produto

Quando você receber um link do TikTok Shop (`https://shop.tiktok.com/...` ou `vt.tiktok.com/...`):

### Passo 1: Extrair Dados do Produto
1. Abra a página com Playwright headless ou navegador.
2. Extraia:
   - Título oficial limpo.
   - Preço original e preço com desconto.
   - Contagem de avaliações e vendas.
   - Fotos da galeria em alta resolução (800x800).
   - Descrição oficial.
   - Avaliações dos clientes com fotos reais.
   - **Desmascaramento de Nomes:** Nomes censurados (`J** R**s`, `p**a`) DEVEM ser substituídos por nomes brasileiros verossímeis (*Juliana Ramos*, *Paula Ramos*, etc.).

### Passo 2: Puxar Vídeos Reais de Criadores
1. Puxe o vídeo oficial do anúncio (`header_video` ou `desc_video`).
2. Se precisar de mais vídeos, busque no TikTok pelo modelo exato (ex: `chinelo feminino strass nó`).
3. Baixe os MP4s sem marca d'água usando `download_and_extract_tiktok_videos.js`.
4. Gere os posters no frame `00:00:00.2`.

### Passo 3: Criar a Página do Produto
Crie `pages/produto-[ID].html` seguindo o template do `produto-104.html` e `produto-105.html`:
1. Carrossel de fotos 1:1.
2. Barra de Oferta Relâmpago (Laranja) posicionada fora de `.product-info`.
3. Bloco Pré-Descrição com os 4 checks verdes de proteção.
4. Descrição oficial.
5. **Avaliações com fotos reais de clientes** (siga rigorosamente `FLUXO_AVALIACOES_OFICIAL.md` para marcação `.review-card` padrão que o `js/app.js` transforma automaticamente no layout TikTok Shop com chips e miniaturas 70x70).
6. Carrossel de "Vídeos de criadores (28+)".
7. Barra fixa inferior de compra com checkout Stone.

### Passo 4: Atualizar Catálogo e Cache
1. Registre o produto no topo de `js/catalogo.js`.
2. Adicione o card na grade `#recommended-grid` de `index.html`.
3. Atualize o cache buster com `node add_cache_buster.js`.
4. Sincronize todos os arquivos:
   ```bash
   node sync_all.js
   ```

### Passo 5: Deploy em Produção
Execute o deploy na Vercel e aponte para o domínio oficial:
```bash
node deploy_to_vercel.js
```
Ou manualmente no terminal:
```bash
npx vercel --prod --yes
npx vercel alias set <url-gerada> stoneshopclone.vercel.app
```

---

## 🛠️ 5. Scripts Auxiliares Prontos na Pasta

| Script | O que faz |
| :--- | :--- |
| `download_and_extract_tiktok_videos.js` | Baixa vídeos do TikTok sem marca d'água e gera os posters FFmpeg no frame exato. |
| `copy_assets.js` | Distribui os novos vídeos e posters entre todas as pastas (`img/`, `pages/img/`, `ds/`). |
| `add_cache_buster.js` | Injeta nova versão (`?v=timestamp`) do script em todas as 89 páginas HTML. |
| `sync_all.js` | Sincroniza `index.html` em `real.html`, `stone.html`, `api/stone_content.js` e workspace `ds/`. |
| `deploy_to_vercel.js` | Roda o deploy na Vercel e vincula o alias `stoneshopclone.vercel.app` automaticamente. |

---

## 🎯 6. Regra Inegociável para IAs / Novos Agentes
Qualquer IA ou dev que assumir o projeto deve ler este arquivo e o `GEMINI.md` na raiz antes de tocar em qualquer código. **Qualidade de produção, zero gambiarra, fotos reais e vídeos gravados de verdade.**
