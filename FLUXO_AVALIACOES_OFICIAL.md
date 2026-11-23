# 🌟 FLUXO OFICIAL DAS AVALIAÇÕES (PADRÃO STONE SHOP & TIKTOK SHOP)

> **Autor:** Bruno (CTO & Fundador Uppi - Modo Zika Blindado)  
> **Status:** 100% Padronizado e Em Produção em 90 Produtos  
> **Regra de Ouro:** Todas as páginas `pages/produto-[ID].html` DEVEM seguir rigorosamente esta estrutura.

---

## 🏗️ 1. Como Funciona a Arquitetura

O sistema de avaliações opera em **duas camadas integradas**:

1. **Camada Estática (HTML Base)**:
   - Escrita no arquivo `pages/produto-[ID].html`.
   - Utiliza a estrutura semântica padrão: `.reviews-section` > `.reviews-header` + `.reviews-summary` + `.review-card`s.
   - Contém todos os reviews com fotos reais de clientes (`.review-photos` com `onclick="openPhotoModal(this.src)"`).

2. **Camada Dinâmica (`js/app.js`)**:
   - No carregamento da página (`DOMContentLoaded`), o script executa automaticamente:
     - `initReviewPagination()`
     - `formatCompactReviews()`
     - `renderStoreReviewsFilter()`
   - Transforma os cards HTML no formato visual compacto do TikTok Shop:
     - Cria o cabeçalho oficial: `★ 4.9 Avaliações dos clientes (X) ⓘ Ver mais ›`
     - Coluna da esquerda: Avatar 32x32 com inicial colorida ou foto, nome, estrelas, variação e comentário logo abaixo.
     - Coluna da direita: Miniatura 70x70 (`.review-compact-thumb-wrap`) com badge `+X` para múltiplas fotos ou ícone de play para vídeos.
     - Mantém **estritamente as 3 primeiras avaliações visíveis** e oculta as demais.
     - Injeta os filtros oficiais da loja: `📷 Inclui imagens ou vídeos (X)` e `★ 5 (X)`.
     - Botão expansor suave que revela 5 avaliações por clique.

---

## 📋 2. Template HTML Obrigatório para Novos Produtos

Sempre que adicionar ou gerar um produto, insira o seguinte bloco logo após a seção `<div id="creators-section" class="creators-section"></div>`:

```html
      <!-- AVALIAÇÕES DOS CLIENTES -->
      <div class="reviews-section">
        <h3 class="reviews-header">Avaliações dos clientes (TOTAL)</h3>
        <div class="reviews-summary">
          <span class="review-avg">4,9</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            ⭐⭐⭐⭐⭐
          </div>
        </div>

        <!-- Avaliação com Foto/Vídeo -->
        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img src="../img/creators-avatars/creator-11.jpg" alt="Nome Cliente" onerror="this.outerHTML='<div class=\'review-avatar-placeholder\'>R</div>'">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">Rodrigo Mendes</div>
                <div class="review-user-stars">⭐⭐⭐⭐⭐</div>
                <div class="review-date">18/10/2026 | Variação: SMART WI-FI 4K, BIVOLT</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Comentário humanizado e contextual com o produto...</p>
          <div class="review-photos">
            <img class="review-photo" src="../img/poster-projetor-1.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
            <img class="review-photo" src="https://down-br.img.susercontent.com/file/exemplo1.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação Apenas Texto (Sem Miniatura na Direita) -->
        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <div class="review-avatar-placeholder">C</div>
              </div>
              <div class="review-user-info">
                <div class="review-user-name">Camila Ferreira</div>
                <div class="review-user-stars">⭐⭐⭐⭐⭐</div>
                <div class="review-date">15/10/2026 | Variação: PADRÃO</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Entrega super rápida e muito bem embalado. Recomendo demais!</p>
        </div>

      </div>
```

---

## 🚫 3. Regras Inegociáveis Anti-Júnior

1. **PROIBIDO ASTERISCOS (`****`)**:
   - Jamais mantenha nomes como `p**a r**a` ou `J** R**s`.
   - Substitua por nomes brasileiros autênticos: *Paula Ramos*, *Juliana Alencar*, *Amanda Cristina*, *Lucas Ferreira*, etc.
2. **PROIBIDO COMENTÁRIO AO LADO DO NOME**:
   - O comentário fica **SEMPRE abaixo** do cabeçalho do usuário, dentro de `.review-content-wrap`, garantindo que textos longos não quebrem o layout ou espremam o avatar.
3. **MINIATURA 70x70 APENAS QUANDO HOUVER MÍDIA**:
   - Cards sem fotos ocupam 100% da largura. Não crie placeholders cinzas vazios na coluna da direita.
4. **MODAL DE FOTOS FUNCIONAL**:
   - Todas as fotos da classe `.review-photo` devem ter `onclick="openPhotoModal(this.src)"`.
5. **AVATARES COM CORES AUTOMÁTICAS**:
   - Elementos `<div class="review-avatar-placeholder">X</div>` recebem automaticamente cores da paleta oficial pelo `js/app.js` de acordo com a inicial.

---

## 🔄 4. Onde Está Implementado na Codebase

- **Mecanismo Dinâmico**: `js/app.js` (funções `formatCompactReviews` na linha ~1464 e `renderStoreReviewsFilter` na linha ~1683).
- **Estilos CSS**: `css/style.css` (classes `.reviews-section`, `.review-card`, `.review-header`, `.review-photos`, `.review-compact-thumb-wrap`).
- **Modal de Fotos**: `js/app.js` (`openPhotoModal`, `closePhotoModal`).
- **Páginas Referência**: `pages/produto-104.html`, `pages/produto-105.html`, `pages/produto-10.html`.
