const { execSync } = require('child_process');

console.log('--- Iniciando Deploy Vercel ---');
try {
  const output = execSync('npx vercel --prod --yes', { encoding: 'utf8', cwd: __dirname });
  console.log(output);
  const match = output.match(/https:\/\/[a-zA-Z0-9-]+\.vercel\.app/);
  if (match) {
    const deployUrl = match[0];
    console.log(`Deploy URL: ${deployUrl}`);
    console.log('--- Vinculando Alias stoneshopclone.vercel.app ---');
    const aliasOut = execSync(`npx vercel alias set ${deployUrl} stoneshopclone.vercel.app`, { encoding: 'utf8', cwd: __dirname });
    console.log(aliasOut);
  } else {
    console.log('Nao foi possivel extrair a URL de deploy, mas o comando rodou.');
  }
} catch (err) {
  console.error('Erro no deploy:', err.message);
  if (err.stdout) console.log('Stdout:', err.stdout);
  if (err.stderr) console.error('Stderr:', err.stderr);
}
