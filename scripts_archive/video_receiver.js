const http = require('http');
const fs = require('fs');
const path = require('path');

const targetFile = path.join(__dirname, 'img', 'video-chinelo-tiktok-2.webm');

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  if (req.url === '/upload' && req.method === 'POST') {
    const fileStream = fs.createWriteStream(targetFile);
    req.pipe(fileStream);
    req.on('end', () => {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true, size: fs.statSync(targetFile).size }));
      console.log('Vídeo gravado no disco com sucesso! Tamanho:', fs.statSync(targetFile).size);
      setTimeout(() => process.exit(0), 1000);
    });
  } else {
    res.writeHead(404);
    res.end();
  }
});

server.listen(9876, () => {
  console.log('Servidor receptor de vídeo ativo na porta 9876');
});
