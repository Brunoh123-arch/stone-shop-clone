const fs = require('fs');

async function extractAllLoaders() {
  const url = 'https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/webapp/main/react-v18/webapp-desktop/static/assets/styles.814f3d15.css';
  const res = await fetch(url);
  const text = await res.text();

  // Search for animation, spinner, skeleton, loading, buffer
  const matches = [];
  const regex = /@(keyframes\s+([a-zA-Z0-9_\-]+)\s*\{[^}]+\})/g;
  let m;
  while ((m = regex.exec(text)) !== null) {
    if (m[2].toLowerCase().includes('load') || m[2].toLowerCase().includes('spin') || m[2].toLowerCase().includes('skel') || m[2].toLowerCase().includes('anim') || m[2].toLowerCase().includes('rotat') || m[2].toLowerCase().includes('flash')) {
      matches.push({ name: m[2], rule: m[1] });
    }
  }

  console.log('Loader keyframes found:', matches.map(x => x.name));

  // Search for skeleton classes
  const skelMatches = text.match(/\.TUXSkeleton[a-zA-Z0-9_\-\:]+\s*\{[^}]+\}/g);
  console.log('Skeleton classes count:', skelMatches ? skelMatches.length : 0);

  // Search for other spinner classes
  const spinClasses = text.match(/\.[a-zA-Z0-9_\-]*([sS]pinner|[lL]oading)[a-zA-Z0-9_\-]*\s*\{[^}]+\}/g);
  console.log('Spinner classes found:', spinClasses ? spinClasses.slice(0, 10) : []);
}

extractAllLoaders();
