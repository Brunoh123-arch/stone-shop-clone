const fs = require('fs');

if (fs.existsSync('pages/produto-103.html')) {
  const html103 = fs.readFileSync('pages/produto-103.html', 'utf8');
  const imgs103 = [...html103.matchAll(/src="([^"]+ibyteimg[^"]+)"/g)].map(m => m[1]);
  console.log('Imagens em 103:', imgs103.slice(0, 3));
} else {
  console.log('produto-103 não existe');
}

const html104 = fs.readFileSync('pages/produto-104.html', 'utf8');
const imgs104 = [...html104.matchAll(/src="([^"]+ibyteimg[^"]+)"/g)].map(m => m[1]);
console.log('Imagens em 104:', imgs104.slice(0, 5));
