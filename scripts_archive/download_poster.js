const https = require('https');
const fs = require('fs');
const path = require('path');

const posterUrl = 'https://p16-common-sign.tiktokcdn.com/tos-alisg-v-f466fc-sg/okQBrjATirsAI6igp1QDc9fflv7FBVC1XEBIGO~tplv-noop.image?dr=18692&refresh_token=4db81e6a&x-expires=1791991163&x-signature=pL2TVhaBTS5ZYekETyQ3vMZRYzY%3D&t=9276707c&ps=14f1eb3e&shp=9e36835a&shcp=6ce186a1&idc=my3&VideoID=v10c21g50000d7bvfavog65rihjgsglg';

const dest = path.join(__dirname, 'img', 'poster-chinelo-oficial.jpg');
const file = fs.createWriteStream(dest);

https.get(posterUrl, {
  headers: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://shop.tiktok.com/'
  }
}, (res) => {
  res.pipe(file);
  file.on('finish', () => {
    file.close();
    console.log('Poster baixado! Tamanho:', fs.statSync(dest).size);
  });
});
