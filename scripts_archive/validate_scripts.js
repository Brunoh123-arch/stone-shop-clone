const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Extrai todos os scripts dentro de <script> e testa sintaxe
const scriptMatches = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/gi)];
console.log('Scripts inline encontrados:', scriptMatches.length);

scriptMatches.forEach((s, idx) => {
  try {
    new Function(s[1]);
    console.log(`Script ${idx + 1}: SINTAXE OK`);
  } catch (err) {
    console.error(`❌ Script ${idx + 1} COM ERRO DE SINTAXE:`, err.message);
  }
});
