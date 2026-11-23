const fs = require('fs');
const path = require('path');

const syncFile = path.join(__dirname, '..', 'sync_all.js');
let text = fs.readFileSync(syncFile, 'utf8');

text = text.replace(/const cacheBuster = '[^']+';/, "const cacheBuster = '1111_v17_modalbannerfinal';");

fs.writeFileSync(syncFile, text, 'utf8');
console.log('✅ sync_all.js cache buster atualizado para 1111_v17_modalbannerfinal!');
