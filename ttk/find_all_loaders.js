const fs = require('fs');

async function findAllLoadersInCode() {
  const cssUrl = 'https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/webapp/main/react-v18/webapp-desktop/static/assets/styles.814f3d15.css';
  const jsUrl = 'https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/webapp/main/react-v18/webapp-desktop/static/js/cache.tux.1abe1f5f.js';
  const webappJsUrl = 'https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/webapp/main/react-v18/webapp-desktop/static/js/webapp-desktop.1c486a57.js';

  const [css, tuxJs, webappJs] = await Promise.all([
    (await fetch(cssUrl)).text(),
    (await fetch(jsUrl)).text(),
    (await fetch(webappJsUrl)).text()
  ]);

  const allCode = css + ' ' + tuxJs + ' ' + webappJs;

  // Find all TUX components starting with TUXLoading or TUXSkeleton or TUXProgress
  const tuxComponents = [...new Set(allCode.match(/TUX(Loading|Skeleton|Progress|Spinner|Indicator|Toast|Shimmer|Wait)[a-zA-Z0-9_\-]*/g) || [])];
  console.log('TUX Loading/Progress Components:', tuxComponents);

  // Search all @keyframes animations in CSS
  const keyframes = [...new Set(css.match(/@keyframes\s+([a-zA-Z0-9_\-]+)/g) || [])];
  console.log('\nAll Keyframes in styles.css:', keyframes);

  // Search for Progress indicators
  const progressMatches = [...new Set(allCode.match(/[a-zA-Z0-9_\-]*(progress|Progress|progressBar|ProgressBar)[a-zA-Z0-9_\-]*/g) || [])];
  console.log('\nProgress related names (sample):', progressMatches.slice(0, 20));

  // Search for Lottie or SVG animations
  const lottieMatches = allCode.includes('lottie') || allCode.includes('Lottie');
  console.log('\nHas Lottie animations:', lottieMatches);
}

findAllLoadersInCode();
