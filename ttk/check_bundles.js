const fs = require('fs');

const requests = JSON.parse(fs.readFileSync('requests.json', 'utf8'));

// Filter all script requests from static CDN
const jsRequests = requests.filter(r => r.url.endsWith('.js') && r.url.includes('tiktok/webapp'));

console.log('Total JS bundles loaded by page:', jsRequests.length);

async function inspectBundles() {
  const shopKeywords = ['showcase', 'shop', 'ecommerce', 'oec', 'vitrine'];
  const matches = [];

  for (const req of jsRequests.slice(0, 30)) {
    try {
      const res = await fetch(req.url);
      const text = await res.text();
      for (const kw of shopKeywords) {
        if (text.toLowerCase().includes(kw)) {
          // Find context
          const idx = text.toLowerCase().indexOf(kw);
          const snippet = text.substring(Math.max(0, idx - 50), Math.min(text.length, idx + 100));
          matches.push({
            url: req.url.split('/').pop(),
            keyword: kw,
            snippet: snippet.replace(/\n/g, ' ')
          });
          break;
        }
      }
    } catch (e) {
      // ignore
    }
  }

  console.log(`Found ${matches.length} bundle matches:`);
  matches.forEach(m => console.log(`[${m.url}] kw: ${m.keyword} -> ${m.snippet}\n`));
}

inspectBundles();
