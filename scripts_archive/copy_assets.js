const fs = require('fs');
const path = require('path');

const base = 'C:/Users/Dell/Downloads/stone_shop_clone';
const dsBase = 'C:/Users/Dell/Downloads/ds';

const filesToCopy = [
  'video-chinelo-oficial.mp4',
  'video-chinelo-completo.mp4',
  'video-chinelo-kethellen1.mp4',
  'video-chinelo-kethellen2.mp4',
  'video-chinelo-juju.mp4',
  'video-chinelo-real-1.mp4',
  'video-chinelo-real-2.mp4',
  'video-chinelo-real-3.mp4',
  'video-chinelo-real-4.mp4',
  'video-chinelo-real-5.mp4',
  'poster-chinelo-real-1.jpg',
  'poster-chinelo-real-2.jpg',
  'poster-chinelo-real-3.jpg',
  'poster-chinelo-real-4.jpg',
  'poster-chinelo-real-5.jpg'
];

const targets = [
  path.join(base, 'pages', 'img'),
  path.join(dsBase, 'img'),
  path.join(dsBase, 'pages', 'img')
];

for (const t of targets) {
  if (!fs.existsSync(t)) {
    fs.mkdirSync(t, { recursive: true });
  }
}

for (const file of filesToCopy) {
  const src = path.join(base, 'img', file);
  if (fs.existsSync(src)) {
    for (const t of targets) {
      const dest = path.join(t, file);
      fs.copyFileSync(src, dest);
    }
    console.log(`Copied ${file} to all destinations.`);
  } else {
    console.warn(`Source not found: ${src}`);
  }
}
