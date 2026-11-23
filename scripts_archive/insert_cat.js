const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

const lastScript = html.lastIndexOf('<script');
const beforeScript = html.slice(0, lastScript);
const lastA = beforeScript.lastIndexOf('</a>');

// Achar onde fecham as divs de recommended-grid e produtos-recomendados-section
// O padrão é:
// </a>
//             </div>
//           </div>
const pattern = '</a>\n            </div>\n\n          </div>';
const patternAlt = '</a>\n            </div>\n          </div>';

let insertPos = html.indexOf(pattern, lastA - 100);
let patternLength = pattern.length;

if (insertPos === -1) {
  insertPos = html.indexOf(patternAlt, lastA - 100);
  patternLength = patternAlt.length;
}

if (insertPos === -1) {
  // Busca flexível
  const sub = html.slice(lastA, lastA + 200);
  const match = sub.match(/<\/a>\s*<\/div>\s*<\/div>/);
  if (match) {
    insertPos = lastA + match.index;
    patternLength = match[0].length;
  }
}

console.log('insertPos:', insertPos, 'patternLength:', patternLength);

if (insertPos !== -1) {
  const categoriasSectionOfficial = `

          <!-- CATEGORIAS SECTION OFICIAL TIKTOK SHOP (Print 2) -->
          <div id="categorias-section" style="display: none; background: white; min-height: 85vh; padding: 4px 16px 20px 16px;">
            <!-- Categoria 1: Calçados -->
            <div class="category-item-row" onclick="filterByCategory('Calçados')" style="display: flex; align-items: center; justify-content: space-between; padding: 14px 0; border-bottom: 1px solid #f5f5f5; cursor: pointer;">
              <div style="display: flex; align-items: center; gap: 14px;">
                <img src="https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/937eda3788b14961af3dc12028a4c886~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my3&from=3376456192"
                  alt="Calçados"
                  style="width: 48px; height: 48px; border-radius: 6px; object-fit: cover; background: #f7f7f7;">
                <span style="font-size: 15px; font-weight: 700; color: #161823;">Calçados</span>
              </div>
              <div style="display: flex; align-items: center; gap: 4px; color: #8a8b91; font-size: 14px;">
                <span>19</span>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 18l6-6-6-6"></path>
                </svg>
              </div>
            </div>

            <!-- Categoria 2: Moda infantil / Vestuário -->
            <div class="category-item-row" onclick="filterByCategory('Moda Feminina')" style="display: flex; align-items: center; justify-content: space-between; padding: 14px 0; border-bottom: 1px solid #f5f5f5; cursor: pointer;">
              <div style="display: flex; align-items: center; gap: 14px;">
                <img src="https://down-br.img.susercontent.com/file/sg-11134201-7rd5p-m7uwvu85tnp9ae"
                  alt="Moda infantil"
                  style="width: 48px; height: 48px; border-radius: 6px; object-fit: cover; background: #f7f7f7;">
                <span style="font-size: 15px; font-weight: 700; color: #161823;">Moda infantil</span>
              </div>
              <div style="display: flex; align-items: center; gap: 4px; color: #8a8b91; font-size: 14px;">
                <span>3</span>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 18l6-6-6-6"></path>
                </svg>
              </div>
            </div>
          </div>`;

  const endChunk = html.slice(insertPos, insertPos + patternLength);
  html = html.slice(0, insertPos) + endChunk + categoriasSectionOfficial + html.slice(insertPos + patternLength);

  fs.writeFileSync('index.html', html, 'utf8');
  console.log('✅ categorias-section inserida com sucesso no DOM oficial!');
} else {
  console.log('❌ Não encontrou posição de inserção para categorias-section');
}
