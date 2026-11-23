const fs = require('fs');
const path = require('path');

const dir = 'C:/Users/Dell/Downloads/stone_shop_clone/videosprodutos';
const files = fs.readdirSync(dir);
console.log('Arquivos em videosprodutos:', files);
