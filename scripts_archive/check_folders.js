const fs = require('fs');
const path = require('path');

const root = 'C:\\Users\\Dell\\Downloads\\stone_shop_clone';
const candidateFolders = [
  'avaliacaodospneus', 'avaliacoesesteira', 'AVALIACOESFOTOS', 'botoesdecarrinhioechat',
  'decalque', 'esteirafotos', 'esteiramodelos2fotos', 'fotodeperfildoscriadores',
  'fotosavaliacaoscooter', 'FOTOSDEPERFIL', 'fotosduascamisa', 'fotosqueapareceramnocarrinhoenoresumo',
  'imagemscooteramarela', 'imagemscooterazul', 'imagemscooterbranca', 'imagemscooterbronze',
  'imagemscootercinzaescuro', 'imagemscooterlaranja', 'imagemscooterprateado', 'imagemscooterpreta',
  'imagemscooterrosa', 'imagemscooterverde', 'imagemscooterverdelimao', 'imagemscootervermelho',
  'logoorderbumps', 'logopirelli', 'logopix', 'modalprotecaodocliente', 'pumalogo',
  'Temp', 'videoscooterintroducao', 'videosdoscriadorespneu', 'videosprodutos'
];

function getAllFiles(dir, exts, list = []) {
  const items = fs.readdirSync(dir);
  for (const item of items) {
    if (item === 'node_modules' || item === '.git' || item === 'scripts_archive' || item === '.vercel') continue;
    const full = path.join(dir, item);
    const st = fs.statSync(full);
    if (st.isDirectory()) {
      if (!candidateFolders.includes(item)) {
        getAllFiles(full, exts, list);
      }
    } else {
      if (exts.some(ext => item.endsWith(ext))) list.push(full);
    }
  }
  return list;
}

const codeFiles = getAllFiles(root, ['.html', '.js', '.css', '.json']);
console.log('Total de arquivos de código escaneados:', codeFiles.length);

const references = {};
for (const folder of candidateFolders) {
  references[folder] = 0;
}

for (const f of codeFiles) {
  const content = fs.readFileSync(f, 'utf8');
  for (const folder of candidateFolders) {
    const regex = new RegExp(folder, 'i');
    if (regex.test(content)) {
      references[folder]++;
    }
  }
}

console.log('Resultados de referências nas páginas/scripts:');
for (const [folder, count] of Object.entries(references)) {
  console.log(folder + ': ' + count + ' arquivos referenciam');
}
