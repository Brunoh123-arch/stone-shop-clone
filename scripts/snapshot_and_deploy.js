const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const description = process.argv.slice(2).join(' ') || 'Alteração sem descrição';
const now = new Date();
const dateStr = now.toLocaleDateString('pt-BR') + ' às ' + now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

const basePath = 'C:/Users/Dell/Downloads/stone_shop_clone';
const dsPath = 'C:/Users/Dell/Downloads/ds';

const currentHtml = fs.readFileSync(path.join(basePath, 'index.html'), 'utf8');

// Ler registro de versões
const jsonPath = path.join(basePath, 'versions', 'index.json');
let versionsList = [];
try {
  versionsList = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
} catch (e) {
  versionsList = [];
}

const nextNum = versionsList.length + 1;
const verId = 'v' + nextNum;
const fileName = `${verId}.html`;

// Desativar anterior e marcar nova como ativa
versionsList.forEach(v => v.ativo = false);

const newEntry = {
  id: verId,
  nome: `${verId} — ${description}`,
  data: dateStr,
  descricao: description,
  arquivo: fileName,
  destaque: 'Design Oficial TikTok Shop (3 Imagens)',
  ativo: true
};

versionsList.unshift(newEntry); // coloca no topo

// Salvar HTML da versão
fs.writeFileSync(path.join(basePath, 'versions', fileName), currentHtml, 'utf8');
fs.writeFileSync(path.join(dsPath, 'versions', fileName), currentHtml, 'utf8');

// Salvar index.json atualizado
fs.writeFileSync(jsonPath, JSON.stringify(versionsList, null, 2), 'utf8');
fs.writeFileSync(path.join(dsPath, 'versions', 'index.json'), JSON.stringify(versionsList, null, 2), 'utf8');

// Atualizar bundle api/_lib/versions_content.js
let bundleObj = {};
versionsList.forEach(v => {
  const filePath = path.join(basePath, 'versions', v.arquivo);
  if (fs.existsSync(filePath)) {
    bundleObj[v.id] = fs.readFileSync(filePath, 'utf8');
  }
});

const versionsContent = `// Gerado automaticamente pelo Time Machine Stone Shop
module.exports = {
${Object.keys(bundleObj).map(k => `  ${k}: ${JSON.stringify(bundleObj[k])}`).join(',\n')},
  list: ${JSON.stringify(versionsList, null, 2)}
};
`;

// Salvar em _lib (para não contar como Serverless Function da Vercel)
fs.writeFileSync(path.join(basePath, 'api', '_lib', 'versions_content.js'), versionsContent, 'utf8');
if (fs.existsSync(path.join(dsPath, 'api', '_lib'))) {
  fs.writeFileSync(path.join(dsPath, 'api', '_lib', 'versions_content.js'), versionsContent, 'utf8');
}

// Salvar stone_content.js
const stoneContent = `module.exports = ${JSON.stringify(currentHtml)};\n`;
fs.writeFileSync(path.join(basePath, 'api', '_lib', 'stone_content.js'), stoneContent, 'utf8');
if (fs.existsSync(path.join(dsPath, 'api', '_lib'))) {
  fs.writeFileSync(path.join(dsPath, 'api', '_lib', 'stone_content.js'), stoneContent, 'utf8');
}

console.log(`✅ Snapshot ${verId} criado com sucesso: "${description}"`);
console.log('🚀 Iniciando deploy automático na Vercel...');

try {
  const deployOut = execSync('npx vercel --scope team_jpSZvSxpTE0zixPUCyjOgLd7 --prod --yes', {
    cwd: basePath,
    encoding: 'utf8'
  });
  console.log(deployOut);

  const urlMatch = deployOut.match(/https:\/\/[a-zA-Z0-9_.-]+\.vercel\.app/);
  if (urlMatch) {
    const prodUrl = urlMatch[0];
    console.log(`Subindo alias para: ${prodUrl}`);
    const aliasOut = execSync(`npx vercel alias set ${prodUrl} stoneshopclone.vercel.app --scope team_jpSZvSxpTE0zixPUCyjOgLd7`, {
      cwd: basePath,
      encoding: 'utf8'
    });
    console.log(aliasOut);
    console.log(`🎯 Alias stoneshopclone.vercel.app atualizado com sucesso!`);
  }
} catch (err) {
  console.error('Erro no deploy:', err.message);
  if (err.stdout) console.log(err.stdout.toString());
  if (err.stderr) console.error(err.stderr.toString());
}
