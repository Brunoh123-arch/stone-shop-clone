const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const scriptMatches = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/gi)];
const s3 = scriptMatches[2][1];

console.log('Script 3 completo:');
console.log(s3);
