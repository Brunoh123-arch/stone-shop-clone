const https = require('https');
const fs = require('fs');

https.get('https://lista.mercadolivre.com.br/projetor-hy300', {
  headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' }
}, res => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const urls = [...new Set(data.match(/https:\/\/http2\.mlstatic\.com\/D_NQ_NP_[^"'\\s]+\.webp/g) || [])];
    console.log('Found', urls.length, 'images:');
    urls.slice(0, 15).forEach(u => console.log(u));
  });
});
