const fs = require('fs');
const path = require('path');

const realPath = path.join(__dirname, 'real.html');
let realHtml = fs.readFileSync(realPath, 'utf8');

if (!realHtml.includes('tracker.js')) {
  realHtml = realHtml.replace('</body>', '<script src="/tracker.js"></script>\n</body>');
  fs.writeFileSync(realPath, realHtml, 'utf8');
  console.log('tracker.js injected into real.html');
} else {
  console.log('tracker.js already in real.html');
}
