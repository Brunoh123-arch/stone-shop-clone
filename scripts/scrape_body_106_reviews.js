const puppeteer = require('../ttk/node_modules/puppeteer-core');
const fs = require('fs');
const path = require('path');

const PDP_URLS = [
  'https://shop.tiktok.com/br/pdp/body-modelador-feminino-fio-compressao-e-conforto/1734383629760562835',
  'https://shop.tiktok.com/br/pdp/body-modelador-compressao-abdominal-fecho-frontal/1733651206797493907',
  'https://shop.tiktok.com/br/pdp/body-modelador-feminino-sem-costura-alca-ajustavel-premium/1733749756587050880',
  'https://shop.tiktok.com/br/pdp/body-macaquinho-cinta-modeladora-conforto-modelagem/1734237331624461971',
  'https://shop.tiktok.com/br/pdp/short-cinta-modeladora-alta-compressao-efeito-empina-barbatanas-antienrolamento-forro-antibacteri/1737541224990213779',
  'https://shop.tiktok.com/br/pdp/calcinha-cinta-modeladora-alta-compressao-redutora-barriga-fio-dental/1733664990936073875',
  'https://shop.tiktok.com/br/pdp/1732415228413511045',
  'https://shop.tiktok.com/br/pdp/1736054260214367538'
];

async function run() {
  console.log('--- Subagente Bruno CTO: Iniciando Scraping de Avaliações Reais Produto 106 ---');
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });

  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.chrome = { runtime: {} };
  });

  const allCapturedReviews = [];
  const allRawResponses = [];

  page.on('response', async res => {
    const u = res.url();
    if (u.includes('api') && (u.includes('review') || u.includes('pdp') || u.includes('page_data') || u.includes('item'))) {
      try {
        const text = await res.text();
        allRawResponses.push({ url: u, text });
      } catch (e) {}
    }
  });

  for (let idx = 0; idx < PDP_URLS.length; idx++) {
    const url = PDP_URLS[idx];
    console.log(`\n[${idx + 1}/${PDP_URLS.length}] Navegando para PDP: ${url}`);

    try {
      await page.goto(url, { waitUntil: 'networkidle2', timeout: 35000 });
    } catch (e) {
      console.log('Timeout/erro ao carregar:', e.message);
    }

    await new Promise(r => setTimeout(r, 4000));

    const pageTitle = await page.title();
    console.log('  Título:', pageTitle);

    if (pageTitle.includes('Security Check') || pageTitle.includes('Entrar')) {
      console.log('  Skipping (Security Check ou Login):', pageTitle);
      continue;
    }

    // Tentar clicar no filtro "Inclui imagens ou vídeos" ou "Ver todas as fotos"
    try {
      const clickResult = await page.evaluate(() => {
        const allSpans = Array.from(document.querySelectorAll('span, button, div'));
        const filterBtn = allSpans.find(el => el.innerText && el.innerText.trim() === 'Inclui imagens ou vídeos');
        if (filterBtn) {
          filterBtn.click();
          return 'Clicou filtro Inclui imagens ou vídeos';
        }
        const photosBtn = allSpans.find(el => el.innerText && el.innerText.trim() === 'Ver todas as fotos' && el.children.length === 0);
        if (photosBtn) {
          photosBtn.click();
          return 'Clicou Ver todas as fotos';
        }
        return 'Nenhum botão de fotos encontrado';
      });
      console.log('  Ação de fotos:', clickResult);
      await new Promise(r => setTimeout(r, 2500));
    } catch (e) {}

    // Extrair avaliações estruturadas da página
    const extractedData = await page.evaluate(() => {
      // 1. Extrair de dados de script (JSON embutido)
      let scriptReviews = [];
      const scripts = Array.from(document.querySelectorAll('script')).map(s => s.innerText);
      for (const s of scripts) {
        if (s.includes('product_reviews') || s.includes('review_info')) {
          try {
            // tentar achar JSON
            const m = s.match(/\{.*\"product_reviews\".*\}/);
            if (m) {
              const d = JSON.parse(m[0]);
              if (d && d.review_info && d.review_info.product_reviews) {
                scriptReviews = d.review_info.product_reviews;
              }
            }
          } catch (e) {}
        }
      }

      // 2. Extrair do DOM
      // Buscar cards de compras verificadas
      const badges = Array.from(document.querySelectorAll('*')).filter(el => el.innerText && el.innerText.trim() === 'Compras verificadas' && el.children.length === 0);
      
      const domReviews = [];
      for (const b of badges) {
        // subir até achar o container da avaliação
        let cur = b;
        for (let i = 0; i < 8; i++) {
          if (!cur.parentElement) break;
          cur = cur.parentElement;
          if (cur.innerText.includes('Item:') || cur.innerText.includes('BR\n')) {
            break;
          }
        }

        const lines = cur.innerText.split('\n').map(l => l.trim()).filter(Boolean);
        const name = lines[0] || 'Cliente TikTok';
        const dateMatch = cur.innerText.match(/\d{4}-\d{2}-\d{2}|\d{2}\/\d{2}/);
        const date = dateMatch ? dateMatch[0] : '';
        const itemMatch = cur.innerText.match(/Item:\s*([^\n]+)/);
        const variation = itemMatch ? itemMatch[1] : '';
        
        // Coletar texto do comentário (excluir "Compras verificadas", "Item:", "BR")
        const commentLines = lines.filter(l => 
          !l.includes('Compras verificadas') && 
          !l.includes('Item:') && 
          l !== 'BR' && 
          l !== name && 
          !l.match(/^\d{4}-\d{2}-\d{2}$/) &&
          !l.includes('Classificar por') &&
          !l.includes('Exibindo') &&
          !l.includes('Limpar filtros')
        );
        const comment = commentLines.join(' ');

        // Coletar imagens
        const imgs = Array.from(cur.querySelectorAll('img')).map(i => ({
          src: i.src,
          isAvatar: (i.className || '').includes('rounded') || i.width < 50,
          w: i.naturalWidth,
          h: i.naturalHeight
        }));

        const avatar = imgs.find(i => i.isAvatar || i.src.includes('tiktokcdn.com'))?.src || null;
        const photos = imgs.filter(i => !i.isAvatar && i.src.includes('ibyteimg.com')).map(i => i.src);

        // Só manter se tiver fotos reais
        if (photos.length > 0) {
          domReviews.push({
            name,
            avatar,
            date,
            variation,
            comment,
            photos
          });
        }
      }

      return {
        scriptReviewsCount: scriptReviews.length,
        scriptReviews,
        domReviewsCount: domReviews.length,
        domReviews
      };
    });

    console.log(`  DOM Reviews com fotos: ${extractedData.domReviewsCount}`);
    for (const r of extractedData.domReviews) {
      allCapturedReviews.push({
        sourceUrl: url,
        ...r
      });
    }

    if (extractedData.scriptReviewsCount > 0) {
      console.log(`  Script Reviews: ${extractedData.scriptReviewsCount}`);
    }
  }

  await browser.close();

  // Salvar resultados
  fs.writeFileSync('scripts/captured_106_reviews.json', JSON.stringify({
    totalReviewsWithPhotos: allCapturedReviews.length,
    reviews: allCapturedReviews,
    rawResponsesCount: allRawResponses.length
  }, null, 2), 'utf-8');

  console.log(`\n=== FIM DA VARREDURA: ${allCapturedReviews.length} avaliações 100% REAIS com fotos extraídas ===`);
}

run().catch(console.error);
