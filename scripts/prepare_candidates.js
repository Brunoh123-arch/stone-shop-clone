const fs = require('fs');

const escovaUrls = [
  "https://www.tiktok.com/@carolinymadona/video/7699510255767555336",
  "https://www.tiktok.com/@cassaofertas/video/7688582692266462482",
  "https://www.tiktok.com/@nina.creator/video/7672528731218464018",
  "https://www.tiktok.com/@aksjdjfjdd/video/7534389321105919238",
  "https://www.tiktok.com/@friendspromo_/video/7480033464507436294",
  "https://www.tiktok.com/@chuvadeofertinha/video/7679278678294957330",
  "https://www.tiktok.com/@achoulevoupravoce/video/7694300719251197204",
  "https://www.tiktok.com/@anapaulanoletto/video/7603511245060197653",
  "https://www.tiktok.com/@giiu.achadinhos/video/7694827852407278869",
  "https://www.tiktok.com/@nrnaiachadinhos/video/7692528077791841588",
  "https://www.tiktok.com/@ache_itendencia/video/7411163695687994629",
  "https://www.tiktok.com/@biaemoises_/video/7665735924449348885",
  "https://www.tiktok.com/@naydiroldi/video/7693143578817694996",
  "https://www.tiktok.com/@dicasdamony25/video/7625412455199493397",
  "https://www.tiktok.com/@luisasoaress11/video/7654708823088745748",
  "https://www.tiktok.com/@topachadosdacarla/video/7649402550914960648",
  "https://www.tiktok.com/@natalierose.oficial/video/7662123993545116935",
  "https://www.tiktok.com/@jackeshopofc/video/7652830821597957384",
  "https://www.tiktok.com/@irisinspira/video/7639394369937919250",
  "https://www.tiktok.com/@drih_ramos69/video/7691484994119748872",
  "https://www.tiktok.com/@amalludicas/video/7614599661831097607",
  "https://www.tiktok.com/@fernandaliveshop/video/7596740955852655892",
  "https://www.tiktok.com/@alinedescobriu1/video/7694397314135379218",
  "https://www.tiktok.com/@tassindica/video/7692284605872770311",
  "https://www.tiktok.com/@isaaoliveiral/video/7523238722087718150",
  "https://www.tiktok.com/@samaracardozo/video/7511446713601658168",
  "https://www.tiktok.com/@danisampaio/video/7647255448785063188",
  "https://www.tiktok.com/@lucieneindica/video/7694094775431073042",
  "https://www.tiktok.com/@ingridcreator/video/7700805818912017685",
  "https://www.tiktok.com/@camilanunees/video/7686173158738627860",
  "https://www.tiktok.com/@caroldelvecchio/video/7694019409014230279",
  "https://www.tiktok.com/@lscarpelly/video/7688336546201652501",
  "https://www.tiktok.com/@luizacorsato/video/7680623652122987783",
  "https://www.tiktok.com/@liquidapromo/video/7603729307445366032",
  "https://www.tiktok.com/@luagustini.indica/video/7703315628953767189",
  "https://www.tiktok.com/@robertakguilherme/video/7700970641557671176",
  "https://www.tiktok.com/@daniidorca/video/7703900347223362836",
  "https://www.tiktok.com/@alliyahblm_/video/7618127574538964244",
  "https://www.tiktok.com/@cintiapeople/video/7704293104727248135",
  "https://www.tiktok.com/@elojacobi/video/7659818920936819969"
];

const modeladorUrls = [
  "https://www.tiktok.com/@meeduardasantos/video/7617231540463865096",
  "https://www.tiktok.com/@ritafregolente/video/7674794944145460500",
  "https://www.tiktok.com/@fernandatanakaoficial/video/7672087101680192776",
  "https://www.tiktok.com/@_milynovaes/video/7702588685518277896",
  "https://www.tiktok.com/@julyefajardotomio/video/7601527476363267348",
  "https://www.tiktok.com/@allanamenezzes/video/7679195634691247380",
  "https://www.tiktok.com/@cisavilasboas/video/7695088448067079442",
  "https://www.tiktok.com/@4hi5en0p/video/7633084149280083221",
  "https://www.tiktok.com/@deborapaviani/video/7658314215622462738",
  "https://www.tiktok.com/@klleyaaa/video/7692800997592206599",
  "https://www.tiktok.com/@brunarodrigoshop/video/7635085922635107605",
  "https://www.tiktok.com/@carolinymadona/video/7695602038285028626",
  "https://www.tiktok.com/@danirodriguescreator/video/7641327190784822548",
  "https://www.tiktok.com/@suzanastrazzer/video/7664956566533115157",
  "https://www.tiktok.com/@kaahtrends/video/7691384889379163410",
  "https://www.tiktok.com/@tamyssilvaaa/video/7688843315915066631",
  "https://www.tiktok.com/@biamartinne/video/7665520924937964807",
  "https://www.tiktok.com/@alara.costa/video/7644279910055431431",
  "https://www.tiktok.com/@viacheibaratoo/video/7694366859100966165",
  "https://www.tiktok.com/@juliarossi01_/video/7696524864655461652",
  "https://www.tiktok.com/@jenniferdarosa2/video/7661950681229643026",
  "https://www.tiktok.com/@anakarolline.r/video/7636541468810693895",
  "https://www.tiktok.com/@steeolliveira/video/7613856993886883080",
  "https://www.tiktok.com/@encontradinhos3/video/7576020751787068680",
  "https://www.tiktok.com/@tay.diasc/video/7700703161270521109",
  "https://www.tiktok.com/@raniisilvaa/video/7702271671826140434",
  "https://www.tiktok.com/@diary.jully/video/7664972577684655380",
  "https://www.tiktok.com/@achadinhos.da.kak2/video/7646738571507911957",
  "https://www.tiktok.com/@maariadanielle/video/7564055933937126663",
  "https://www.tiktok.com/@michellypontess/video/7663515849726233876",
  "https://www.tiktok.com/@loyslanetoledo/video/7531009860641623302",
  "https://www.tiktok.com/@anarecomendaa/video/7679810671202012424",
  "https://www.tiktok.com/@tassos.shop/video/7701261264659565832",
  "https://www.tiktok.com/@thaisgermno/video/7646434089377090834",
  "https://www.tiktok.com/@laguardiaindica/video/7704087253286505746",
  "https://www.tiktok.com/@cassia_hair/video/7680586982313200917",
  "https://www.tiktok.com/@milenarauujoo/video/7630804808617774356",
  "https://www.tiktok.com/@josilaineballand/video/7703764223611964693",
  "https://www.tiktok.com/@raquel.hsn/video/7677748532681461010",
  "https://www.tiktok.com/@dudapjdicas/video/7670182729660632340",
  "https://www.tiktok.com/@thaisgodynha/video/7657962583017671944"
];

// Já temos 8 criadoras de cada, que NÃO devem ser repetidas:
const existingEscovaUsers = ['dailykarenm', 'danielefogassa', 'dicascomjaque', 'marcellaromero', 'dayanemarcheseli', 'cheiadetruques_', 'cassaofertas', 'dayalvesoficial'];
const existingModeladorUsers = ['gabimodestoo', 'achadinhos.daluah', 'yasmin.aoliveira', 'samara_fontele', 'dirio.da.lili5', 'laizisantiago', 'helofrasao', 'rafaella.samara'];

function filterUrls(urls, existing) {
  const seenAuthors = new Set(existing);
  const result = [];
  for (const u of urls) {
    const author = u.split('/@')[1]?.split('/')[0];
    if (author && !seenAuthors.has(author.toLowerCase())) {
      seenAuthors.add(author.toLowerCase());
      result.push(u);
    }
  }
  return result;
}

const filteredEscova = filterUrls(escovaUrls, existingEscovaUsers);
const filteredModelador = filterUrls(modeladorUrls, existingModeladorUsers);

console.log('Novas criadoras únicas Escova:', filteredEscova.length);
console.log('Novas criadoras únicas Modelador:', filteredModelador.length);

fs.writeFileSync('scripts/candidates_escova.json', JSON.stringify(filteredEscova, null, 2), 'utf8');
fs.writeFileSync('scripts/candidates_modelador.json', JSON.stringify(filteredModelador, null, 2), 'utf8');
