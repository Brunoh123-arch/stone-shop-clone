const fs = require('fs');

let html = fs.readFileSync('pages/produto-52.html', 'utf8');
if (!html.includes('tracker.js')) {
  html = html.replace('</body>', '<script src="/tracker.js"></script>\n</body>');
  fs.writeFileSync('pages/produto-52.html', html, 'utf8');
  console.log('Injected tracker.js into produto-52.html!');
} else {
  console.log('tracker.js already in produto-52.html');
}
