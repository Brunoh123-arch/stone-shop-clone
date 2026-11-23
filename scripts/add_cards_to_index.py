import re

path = 'index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se já foram adicionados
if 'pages/produto-106.html' in content and 'pages/produto-107.html' in content:
    print("Cards 106 e 107 já estão no index.html!")
else:
    cards_html = """              <!-- PRODUTO 106 -->
              <a class="product-card-rec" href="pages/produto-106.html" data-cat="Moda" data-nome="body modelador cinta alta compressao invisivel efeito lipo redutora" data-vendas="19482" data-id="106" style="text-decoration: none; color: inherit;">
                <div class="card-inner-box">
                  <img src="img/produto-106-1.jpg" alt="Body Modelador Cinta Alta Compressao Invisivel" loading="lazy" class="card-thumb-img">
                  <div class="card-details-col">
                    <div class="card-top-info">
                      <h3 class="product-name">Body Modelador Cinta Alta Compressão Invisível Efeito Lipo Redutora</h3>
                      <div class="badge-flash-tag" style="display: inline-flex !important; align-items: stretch !important; height: 18px !important; border-radius: 9px !important; overflow: hidden !important; margin: 3px 0 2px 0 !important; width: fit-content !important; box-sizing: border-box !important;">
                        <span style="background: #ff4800 !important; color: #ffffff !important; display: inline-flex !important; align-items: center !important; gap: 3px !important; padding: 0 6px 0 6px !important; font-size: 9.5px !important; font-weight: 800 !important; line-height: 1 !important; white-space: nowrap !important;">
                          <svg viewBox="0 0 24 24" width="10" height="10" fill="#ffffff" style="flex-shrink: 0 !important;"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" /></svg>
                          Oferta 11.11
                        </span>
                        <span style="background: #ffebe5 !important; color: #ff4800 !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; padding: 0 6px !important; font-size: 9.5px !important; font-weight: 800 !important; line-height: 1 !important; white-space: nowrap !important;">
                          19:46:52
                        </span>
                      </div>
                      <div class="card-badges-row">
                        <span class="badge-frete-gratis">Frete grátis</span>
                        <span class="related-discount" style="background: #fff0f2; color: #fe2c55; border: 1px solid #ffd8e0; font-size: 9px; font-weight: 700; padding: 0.5px 3px; border-radius: 2px; line-height: 1.2;">-75%</span>
                      </div>
                    </div>
                    <div class="card-bottom-info">
                      <div class="card-price-row">
                        <span class="currency">R$</span>
                        <span class="price-val">29,90</span>
                        <span class="price-old">R$ 119,90</span>
                      </div>
                      <div class="card-extra-row">
                        <div class="card-rating">
                          <svg viewBox="0 0 24 24" class="star-icon" style="width: 11px; height: 11px; fill: #ffb800;"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                          <span>4.9</span>
                        </div>
                        <span class="sales-text">19.482 vendido(s)</span>
                      </div>
                    </div>
                  </div>
                </div>
              </a>

              <!-- PRODUTO 107 -->
              <a class="product-card-rec" href="pages/produto-107.html" data-cat="Automotivo" data-nome="mini aspirador de po sem fio portatil e soprador turbo 2 em 1 carro e casa" data-vendas="16340" data-id="107" style="text-decoration: none; color: inherit;">
                <div class="card-inner-box">
                  <img src="img/produto-107-1.jpg" alt="Mini Aspirador de Po Sem Fio Portatil Soprador Turbo" loading="lazy" class="card-thumb-img">
                  <div class="card-details-col">
                    <div class="card-top-info">
                      <h3 class="product-name">Mini Aspirador de Pó Sem Fio Portátil e Soprador Turbo 2 em 1 Carro e Casa</h3>
                      <div class="badge-flash-tag" style="display: inline-flex !important; align-items: stretch !important; height: 18px !important; border-radius: 9px !important; overflow: hidden !important; margin: 3px 0 2px 0 !important; width: fit-content !important; box-sizing: border-box !important;">
                        <span style="background: #ff4800 !important; color: #ffffff !important; display: inline-flex !important; align-items: center !important; gap: 3px !important; padding: 0 6px 0 6px !important; font-size: 9.5px !important; font-weight: 800 !important; line-height: 1 !important; white-space: nowrap !important;">
                          <svg viewBox="0 0 24 24" width="10" height="10" fill="#ffffff" style="flex-shrink: 0 !important;"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" /></svg>
                          Oferta 11.11
                        </span>
                        <span style="background: #ffebe5 !important; color: #ff4800 !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; padding: 0 6px !important; font-size: 9.5px !important; font-weight: 800 !important; line-height: 1 !important; white-space: nowrap !important;">
                          19:46:52
                        </span>
                      </div>
                      <div class="card-badges-row">
                        <span class="badge-frete-gratis">Frete grátis</span>
                        <span class="related-discount" style="background: #fff0f2; color: #fe2c55; border: 1px solid #ffd8e0; font-size: 9px; font-weight: 700; padding: 0.5px 3px; border-radius: 2px; line-height: 1.2;">-75%</span>
                      </div>
                    </div>
                    <div class="card-bottom-info">
                      <div class="card-price-row">
                        <span class="currency">R$</span>
                        <span class="price-val">34,90</span>
                        <span class="price-old">R$ 139,90</span>
                      </div>
                      <div class="card-extra-row">
                        <div class="card-rating">
                          <svg viewBox="0 0 24 24" class="star-icon" style="width: 11px; height: 11px; fill: #ffb800;"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                          <span>4.9</span>
                        </div>
                        <span class="sales-text">16.340 vendido(s)</span>
                      </div>
                    </div>
                  </div>
                </div>
              </a>

"""
    target = '              <!-- PRODUTO 105 -->'
    if target in content:
        content = content.replace(target, cards_html + target)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Cards 106 e 107 inseridos com sucesso no index.html!")
    else:
        print("Erro: Target <!-- PRODUTO 105 --> não encontrado.")
