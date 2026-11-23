const fs = require('fs');

const requests = JSON.parse(fs.readFileSync('requests.json', 'utf8'));

// Filter all requests that have shop, ecom, commerce, showcase, product, etc.
const shopMatches = requests.filter(r => {
  const u = r.url.toLowerCase();
  return u.includes('shop') || u.includes('showcase') || u.includes('ecom') || u.includes('product') || u.includes('commerce') || u.includes('seller') || u.includes('merchant');
});

console.log('Matches found for shop/ecom/showcase/product in requests:', shopMatches.length);
shopMatches.forEach(m => console.log(m.method, m.url));
