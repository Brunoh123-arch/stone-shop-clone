const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

console.log('Existe categorias-section?', html.includes('id="categorias-section"'));

// Onde termina recommended-grid?
const rStart = html.indexOf('id="recommended-grid"');
console.log('recommended-grid start:', rStart);

// Encontrar as últimas tags antes de <script>
const scriptStart = html.indexOf('<script');
console.log('Últimos 1000 caracteres antes do primeiro script:');
console.log(html.slice(scriptStart - 1000, scriptStart));
