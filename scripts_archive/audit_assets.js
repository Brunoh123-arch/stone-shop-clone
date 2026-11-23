const fs = require('fs');
const https = require('https');

const html = fs.readFileSync('real.html', 'utf8');

const linkMatches = html.match(/<link[^>]+href=["']([^"']+)["']/gi) || [];
const scriptMatches = html.match(/<script[^>]+src=["']([^"']+)["']/gi) || [];

const links = linkMatches.map(m => m.match(/href=["']([^"']+)["']/)[1]);
const scripts = scriptMatches.map(m => m.match(/src=["']([^"']+)["']/)[1]);

console.log('LINKS:', links);
console.log('SCRIPTS:', scripts);

const localAssets = [...links, ...scripts].filter(u => !u.startsWith('http') && !u.startsWith('//') && !u.startsWith('data:'));

console.log('LOCAL ASSETS TO CHECK:', localAssets);

localAssets.forEach(a => {
  const url = 'https://stoneshopclone.vercel.app/' + a.replace(/^\//, '');
  https.get(url, res => {
    console.log(a, '->', res.statusCode);
  }).on('error', e => console.error(a, e.message));
});
