const fs = require('fs');
const path = require('path');

const cssPath = path.join(__dirname, 'css', 'style.css');
let css = fs.readFileSync(cssPath, 'utf8');

const importRule = "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');\n\n";

if (!css.includes('Plus+Jakarta+Sans')) {
  css = importRule + css;
}

// Replace --font-main
css = css.replace(
  /--font-main:\s*[^;]+;/,
  '--font-main: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "TikTok Sans", "Plus Jakarta Sans", "Inter", sans-serif;'
);

// Add input, button font inheritance if not present
if (!css.includes('input, button, select, textarea, optgroup {')) {
  const resetAnchor = '/* ===== RESET ===== */';
  if (css.includes(resetAnchor)) {
    css = css.replace(
      resetAnchor,
      resetAnchor + '\ninput, button, select, textarea, optgroup {\n  font-family: inherit;\n  -webkit-font-smoothing: antialiased;\n  -moz-osx-font-smoothing: grayscale;\n}'
    );
  }
}

// Add body smoothing and letter spacing if not present
css = css.replace(
  /body\s*\{([^}]+)\}/,
  (match, p1) => {
    let inner = p1;
    if (!inner.includes('-webkit-font-smoothing')) {
      inner = '\n  -webkit-font-smoothing: antialiased;\n  -moz-osx-font-smoothing: grayscale;\n  text-rendering: optimizeLegibility;\n  letter-spacing: -0.2px;' + inner;
    }
    return 'body {' + inner + '}';
  }
);

fs.writeFileSync(cssPath, css, 'utf8');
console.log('style.css updated successfully!');

// Also sync with ds/css/style.css if it exists
const dsCss = path.join('C:', 'Users', 'Dell', 'Downloads', 'ds', 'css', 'style.css');
if (fs.existsSync(dsCss)) {
  fs.writeFileSync(dsCss, css, 'utf8');
  console.log('ds/css/style.css synchronized!');
}
