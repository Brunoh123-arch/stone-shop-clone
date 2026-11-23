const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Achar a última ocorrência de </a> antes dos scripts finais
const lastScript = html.lastIndexOf('<script');
const beforeScript = html.slice(0, lastScript);
const lastA = beforeScript.lastIndexOf('</a>');

console.log('--- AO REDOR DO FINAL DOS PRODUTOS ---');
console.log(beforeScript.slice(lastA - 50, lastA + 300));
