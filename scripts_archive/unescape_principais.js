const fs = require('fs');

let c = fs.readFileSync('original_principais.html', 'utf8');

// Desescapa
c = c.replace(/\\"/g, '"').replace(/\\\n/g, '\n').replace(/\\/g, '');

fs.writeFileSync('original_principais.html', c, 'utf8');
console.log('✅ original_principais.html desescapado com sucesso!');
