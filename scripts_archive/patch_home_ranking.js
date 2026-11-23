const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('id="principais-produtos-section"');
const eIdx = html.indexOf('id="produtos-recomendados-section"');

if (sIdx !== -1 && eIdx !== -1) {
  const newPrincipaisHtml = `id="principais-produtos-section" style="background: white; padding: 14px 16px; margin-bottom: 8px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; cursor: pointer;">
              <h2 style="font-size: 16px; font-weight: 700; color: #161823; margin: 0px;">Principais produtos</h2>
              <div style="display: flex; align-items: center; gap: 2px; font-size: 13px; color: #757575;">
                Ver mais
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 18l6-6-6-6"></path>
                </svg>
              </div>
            </div>
            
            <!-- GRADE TOP 3 RANKING (IDÊNTICO AO PRINT 3) -->
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 18px;">
              <!-- TOP 1 -->
              <a href="pages/produto-103.html" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;">
                <div style="position: relative; background: #f7f7f7; border-radius: 6px; overflow: hidden; aspect-ratio: 1/1; margin-bottom: 6px;">
                  <span style="position: absolute; top: 0; left: 0; background: #ecd299; color: #5c4314; font-size: 11px; font-weight: 800; padding: 2px 7px; border-bottom-right-radius: 6px; z-index: 5;">1</span>
                  <img src="https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/ef0c4879de7a44f4955799ce3a17e13e~tplv-o3syd03w52-resize-jpeg:800:800.jpeg"
                    alt="Chinelo feminino Cruzada Glitter" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <h3 style="font-size: 12.5px; font-weight: 500; color: #161823; line-height: 1.25; margin: 0 0 4px 0; height: 32px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                  Chinelo feminino Cruz...
                </h3>
                <div style="margin-bottom: 3px;">
                  <span class="badge-frete-gratis">Frete grátis</span>
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-start;">
                  <div style="color: #fe2c55; font-size: 14px; font-weight: 800; line-height: 1.1;">
                    <span style="font-size: 10px; font-weight: 800;">R$</span> 32,44
                  </div>
                  <div style="font-size: 10.5px; color: #999; text-decoration: line-through; margin-top: 1px;">R$ 49,90</div>
                </div>
                <div style="font-size: 10.5px; color: #888; margin-top: 2px;">14.1K vendido(s)</div>
              </a>

              <!-- TOP 2 -->
              <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;">
                <div style="position: relative; background: #f7f7f7; border-radius: 6px; overflow: hidden; aspect-ratio: 1/1; margin-bottom: 6px;">
                  <span style="position: absolute; top: 0; left: 0; background: #cbd5e1; color: #334155; font-size: 11px; font-weight: 800; padding: 2px 7px; border-bottom-right-radius: 6px; z-index: 5;">2</span>
                  <img src="https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/66d3a87ec7e8424b94f06ddfd71bc391~tplv-o3syd03w52-resize-jpeg:800:800.jpeg"
                    alt="Chinelo feminino NO STRASS Verão 2025" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <h3 style="font-size: 12.5px; font-weight: 500; color: #161823; line-height: 1.25; margin: 0 0 4px 0; height: 32px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                  Chinelo feminino NO S...
                </h3>
                <div style="margin-bottom: 3px;">
                  <span class="badge-frete-gratis">Frete grátis</span>
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-start;">
                  <div style="color: #fe2c55; font-size: 14px; font-weight: 800; line-height: 1.1;">
                    <span style="font-size: 10px; font-weight: 800;">R$</span> 39,53
                  </div>
                  <div style="font-size: 10.5px; color: #999; text-decoration: line-through; margin-top: 1px;">R$ 59,90</div>
                </div>
                <div style="font-size: 10.5px; color: #888; margin-top: 2px;">9017 vendido(s)</div>
              </a>

              <!-- TOP 3 -->
              <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;">
                <div style="position: relative; background: #f7f7f7; border-radius: 6px; overflow: hidden; aspect-ratio: 1/1; margin-bottom: 6px;">
                  <span style="position: absolute; top: 0; left: 0; background: #d9b89d; color: #4a2c16; font-size: 11px; font-weight: 800; padding: 2px 7px; border-bottom-right-radius: 6px; z-index: 5;">3</span>
                  <img src="https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/218cb51a37c34fca92f1683be83c4b9a~tplv-o3syd03w52-resize-jpeg:800:800.jpeg"
                    alt="Chinelo Feminino Luxo Strass Brilhante Macio Leve" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <h3 style="font-size: 12.5px; font-weight: 500; color: #161823; line-height: 1.25; margin: 0 0 4px 0; height: 32px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                  Chinelo feminino LUX...
                </h3>
                <div style="margin-bottom: 3px;">
                  <span class="badge-frete-gratis">Frete grátis</span>
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-start;">
                  <div style="color: #fe2c55; font-size: 14px; font-weight: 800; line-height: 1.1;">
                    <span style="font-size: 10px; font-weight: 800;">R$</span> 39,53
                  </div>
                  <div style="font-size: 10.5px; color: #999; text-decoration: line-through; margin-top: 1px;">R$ 59,90</div>
                </div>
                <div style="font-size: 10.5px; color: #888; margin-top: 2px;">8967 vendido(s)</div>
              </a>
            </div>

            <!-- SEÇÃO NOVOS LANÇAMENTOS (IDÊNTICO AO PRINT 3) -->
            <div style="margin-top: 8px;">
              <h2 style="font-size: 16px; font-weight: 700; color: #161823; margin: 0 0 12px 0;">Novos lançamentos</h2>
              
              <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: flex; gap: 12px; background: #fff; border-radius: 8px; align-items: center;">
                <div style="width: 110px; height: 110px; min-width: 110px; border-radius: 8px; overflow: hidden; background: #f7f7f7;">
                  <img src="https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/5135cb7416344aa18e950ceee9ff304d~tplv-o3syd03w52-resize-jpeg:800:800.jpeg"
                    alt="Sandália feminino LIA Delicada" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <div style="flex: 1; display: flex; flex-direction: column; justify-content: space-between; height: 110px; padding: 2px 0;">
                  <div>
                    <h3 style="font-size: 13.5px; font-weight: 500; color: #161823; line-height: 1.3; margin: 0 0 4px 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                      Sandália feminino LIA Delicada, C...
                    </h3>
                    <div style="margin-bottom: 6px;">
                      <span class="badge-frete-gratis">Frete grátis</span>
                    </div>
                  </div>
                  <div style="display: flex; align-items: flex-end; justify-content: space-between; width: 100%;">
                    <div style="display: flex; flex-direction: column; align-items: flex-start;">
                      <div style="color: #fe2c55; font-size: 17px; font-weight: 800; line-height: 1.1; display: flex; align-items: baseline;">
                        <span style="font-size: 11px; font-weight: 800; margin-right: 2px;">R$</span>25,95
                      </div>
                      <div style="display: flex; align-items: center; gap: 4px; margin-top: 2px;">
                        <span style="font-size: 11px; color: #999; text-decoration: line-through;">R$ 49,90</span>
                        <span class="badge-discount-percent">-48%</span>
                      </div>
                    </div>
                    <div style="display: flex; align-items: stretch; height: 30px; border-radius: 6px; overflow: hidden; cursor: pointer; box-shadow: 0 1px 3px rgba(254, 44, 85, 0.15);">
                      <div onclick="event.preventDefault(); event.stopPropagation(); window.openProductModalDirectly('pages/produto-104.html');" style="background: #ffe8ee; display: flex; align-items: center; justify-content: center; padding: 0 9px;">
                        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#fe2c55" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="9" cy="21" r="1"></circle>
                          <circle cx="20" cy="21" r="1"></circle>
                          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                        </svg>
                      </div>
                      <div onclick="event.stopPropagation(); window.location.href='pages/produto-104.html';" style="background: #fe2c55; color: #ffffff; font-size: 12.5px; font-weight: 700; display: flex; align-items: center; justify-content: center; padding: 0 10px;">
                        Comprar
                      </div>
                    </div>
                  </div>
                </div>
              </a>
            </div>
          </div>\n\n          <!-- PRODUTOS RECOMENDADOS -->\n          <div `;

  html = html.slice(0, sIdx) + newPrincipaisHtml + html.slice(eIdx + 4);
  fs.writeFileSync('index.html', html, 'utf8');
  console.log('✅ principais-produtos-section atualizado com perfeição do Print 3!');
} else {
  console.log('❌ Não encontrou delimitadores de principais-produtos-section');
}
