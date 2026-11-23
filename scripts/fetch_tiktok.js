const https = require('https');

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8'
      }
    }, res => {
      console.log('Status for', url, ':', res.statusCode, res.headers.location || '');
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return resolve(fetchUrl(res.headers.location));
      }
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve(body));
    }).on('error', reject);
  });
}

async function main() {
  const urls = [
    'https://shop.tiktok.com/br/pdp/1733651206797493907',
    'https://shop.tiktok.com/br/c/shapewear/601259'
  ];
  for (const u of urls) {
    try {
      const html = await fetchUrl(u);
      console.log(u, 'len:', html.length);
      const matches = html.match(/https:\/\/[^"'\s<>]+\.ibyteimg\.com[^"'\s<>]+/g);
      if (matches) {
        console.log('Found ibyteimg count:', matches.length);
        const unique = [...new Set(matches)];
        console.log('Unique:', unique.slice(0, 10));
      } else {
        console.log('No ibyteimg images found directly.');
      }
    } catch (e) {
      console.error('Error for', u, e.message);
    }
  }
}

main();
