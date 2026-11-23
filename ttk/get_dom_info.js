const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--window-size=1920,1080',
      '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });

  await page.goto('https://www.tiktok.com/@nandaa1332', { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 4000));

  const info = await page.evaluate(() => {
    const textNodes = [];
    document.querySelectorAll('h1, h2, h3, h4, span, p, a, div[data-e2e]').forEach(el => {
      const e2e = el.getAttribute('data-e2e');
      const text = el.innerText ? el.innerText.trim() : '';
      if (text && (e2e || el.tagName.startsWith('H') || ['user-title', 'user-subtitle', 'user-bio'].some(c => el.className?.includes(c)))) {
        textNodes.push({ tag: el.tagName, e2e, class: el.className, text });
      }
    });

    const allLinks = Array.from(document.querySelectorAll('a')).map(a => ({
      href: a.href,
      text: a.innerText?.trim(),
      className: a.className
    }));

    return {
      title: document.title,
      textNodes,
      allLinks: allLinks.filter(l => l.href && !l.href.startsWith('javascript:'))
    };
  });

  fs.writeFileSync('dom_info.json', JSON.stringify(info, null, 2), 'utf8');
  console.log('Saved dom_info.json');
  console.log('Page Title:', info.title);
  console.log('Text Nodes count:', info.textNodes.length);
  console.log('All links count:', info.allLinks.length);
  console.log('Sample links:', JSON.stringify(info.allLinks.slice(0, 10), null, 2));

  await browser.close();
})();
