const puppeteer = require('../ttk/node_modules/puppeteer-core');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    ]
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });

  const queries = [
    'site:tiktok.com "jbl boombox 3"',
    'site:tiktok.com "boombox 3" unboxing som'
  ];

  const foundLinks = new Set();

  for (const q of queries) {
    console.log('Searching Google for:', q);
    const googleUrl = 'https://www.google.com/search?q=' + encodeURIComponent(q) + '&num=20&hl=pt-BR';
    try {
      await page.goto(googleUrl, { waitUntil: 'domcontentloaded', timeout: 25000 });
      await new Promise(r => setTimeout(r, 2000));
      const links = await page.evaluate(() => {
        const anchors = Array.from(document.querySelectorAll('a[href]'));
        return anchors
          .map(a => a.href)
          .filter(h => h.includes('tiktok.com/@') && h.includes('/video/'));
      });
      console.log(`Found ${links.length} links for query:`, q);
      links.forEach(l => {
        const clean = l.split('?')[0];
        foundLinks.add(clean);
        console.log('  ->', clean);
      });
    } catch (e) {
      console.log('Search error:', e.message);
    }
  }

  await browser.close();

  const arr = Array.from(foundLinks);
  console.log(`Total unique links found: ${arr.length}`);
  fs.writeFileSync('scripts/jbl_tiktok_candidates.txt', arr.join('\n'), 'utf-8');
})();
