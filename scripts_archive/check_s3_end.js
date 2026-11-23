const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const scriptMatches = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/gi)];
const s3 = scriptMatches[2][1];

console.log('Últimos 600 caracteres do Script 3:');
console.log(s3.slice(s3.length - 600));
