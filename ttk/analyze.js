const fs = require('fs');

const apis = JSON.parse(fs.readFileSync('api_responses.json', 'utf8'));
const doc = apis[1] ? apis[1].body : '';
if (doc) {
  fs.writeFileSync('hydrated_page.html', doc, 'utf8');
  console.log('Saved hydrated_page.html, size:', doc.length);

  // Find __UNIVERSAL_DATA_FOR_REHYDRATION__
  const uniMatch = doc.match(/<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>([\s\S]*?)<\/script>/);
  if (uniMatch) {
    try {
      const parsed = JSON.parse(uniMatch[1]);
      fs.writeFileSync('universal_data.json', JSON.stringify(parsed, null, 2), 'utf8');
      console.log('Saved universal_data.json');
      console.log('Universal Data top-level keys:', Object.keys(parsed));
      if (parsed['__DEFAULT_SCOPE__']) {
        console.log('__DEFAULT_SCOPE__ keys:', Object.keys(parsed['__DEFAULT_SCOPE__']));
        const userDetail = parsed['__DEFAULT_SCOPE__']['webapp.user-detail'];
        if (userDetail) {
          console.log('User detail keys:', Object.keys(userDetail));
          console.log('User info:', JSON.stringify(userDetail.userInfo, null, 2));
        }
      }
    } catch (e) {
      console.log('Error parsing universal data:', e.message);
    }
  } else {
    console.log('__UNIVERSAL_DATA_FOR_REHYDRATION__ not found in doc');
  }

  // Find SIGI_STATE
  const sigiMatch = doc.match(/<script id="SIGI_STATE"[^>]*>([\s\S]*?)<\/script>/);
  if (sigiMatch) {
    console.log('Found SIGI_STATE!');
  }
}
