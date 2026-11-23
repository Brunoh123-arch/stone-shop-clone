const fs = require('fs');
const path = require('path');

const sampleFiles = ['produto-10.html', 'produto-100.html', 'produto-101.html', 'produto-102.html', 'produto-103.html'];

sampleFiles.forEach(file => {
  const p = path.join(__dirname, 'pages', file);
  if (fs.existsSync(p)) {
    const html = fs.readFileSync(p, 'utf8');
    console.log('=== FILE:', file, '===');
    // find product-title
    const titleMatch = html.match(/<h1[^>]*class="[^"]*product-title[^"]*"[^>]*>[\s\S]*?<\/h1>/);
    console.log('Title match:', titleMatch ? titleMatch[0].trim() : 'NONE');
    
    // find ratings-row
    const ratingMatch = html.match(/<div[^>]*class="[^"]*ratings-row[^"]*"[^>]*>[\s\S]*?<\/div>\s*<\/div>/);
    if (!ratingMatch) {
      const altRating = html.match(/<div[^>]*class="[^"]*ratings-row[^"]*"[^>]*>[\s\S]*?<\/div>/);
      console.log('Rating match (single):', altRating ? altRating[0].trim().slice(0, 300) : 'NONE');
    } else {
      console.log('Rating match:', ratingMatch[0].trim().slice(0, 300));
    }
  }
});
