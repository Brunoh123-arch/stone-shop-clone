const { execSync } = require('child_process');
const fs = require('fs');

// ffmpeg extrai a regiao de 'sem juros' em raw RGB24
// Em crop_flash_bar.png (460x300):
// A barra laranja vai de y=0 ate cerca de y=100
// A linha de parcelamento fica logo abaixo, cerca de y=110 ate y=145
// O texto 'sem juros' fica em x=135..220, y=120..140
const raw = execSync('ffmpeg -v error -i "C:/Users/Dell/.gemini/antigravity/brain/40253795-724e-4836-a8ee-923b78213fd5/crop_flash_bar.png" -filter:v "crop=90:24:135:120" -f rawvideo -pix_fmt rgb24 -', { maxBuffer: 10*1024*1024 });

const colors = [];
for (let i = 0; i < raw.length; i += 3) {
  const r = raw[i];
  const g = raw[i+1];
  const b = raw[i+2];
  if (r < 240 || g < 240 || b < 240) {
    colors.push({ r, g, b, hex: '#' + [r, g, b].map(x => x.toString(16).padStart(2, '0')).join('') });
  }
}

const freq = {};
colors.forEach(c => { freq[c.hex] = (freq[c.hex] || 0) + 1; });
const sorted = Object.entries(freq).sort((a, b) => b[1] - a[1]);
console.log('Cores encontradas em sem juros:', sorted.slice(0, 15));
