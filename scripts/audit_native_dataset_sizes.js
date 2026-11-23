const fs = require('fs');
const vm = require('vm');

let code = fs.readFileSync('js/videos-criadores.js', 'utf8');

// Inject extraction of all CREATORS_ and POOL_ variables
const injection = `
  global.__getAllDatasets = function() {
    const data = {};
    const varNames = [
      'CREATORS_JBL_4', 'CREATORS_AIRFRYER_5', 'CREATORS_BIKE_6', 'CREATORS_AIWA_7', 'CREATORS_AIWA_PARTYBOX_8',
      'CREATORS_AR_HQ_9', 'CREATORS_AR_HISENSE_10', 'CREATORS_CLIMATIZADOR_OSTER_11', 'CREATORS_PISCINA_12',
      'CREATORS_PISCINA_PIXLAR_13', 'CREATORS_CHURRASQUEIRA_ARKE_14', 'CREATORS_CHURRASQUEIRA_15', 'CREATORS_CHURRASQUEIRA_MOR_16',
      'CREATORS_KIT_PRAIA_MOR_18', 'CREATORS_BIKE_GT_20', 'CREATORS_BOLA_PENALTY_21', 'CREATORS_COLCHAO_BESTWAY_22',
      'CREATORS_AR_LG_27', 'CREATORS_CHINELO_28', 'CREATORS_AR_HQ_29', 'CREATORS_CLIMATIZADOR_MIDEA_30',
      'CREATORS_SABALA_31', 'CREATORS_CHUVEIRO_32', 'CREATORS_JBL_BOOMBOX4_35', 'CREATORS_POCO_X7_PRO_36',
      'CREATORS_PANIFICADORA_48_84', 'CREATORS_PAD11_52', 'CREATORS_SWITCH_55', 'CREATORS_JOOG_ONE_57',
      'CREATORS_ECHODOT_58', 'CREATORS_STARLINK_59', 'CREATORS_JOOG_BREAK_61', 'CREATORS_REDMI_WATCH_63',
      'CREATORS_SOFA_SENSES_65', 'CREATORS_SECADORA_MUELLER_70', 'CREATORS_WAAW_HYPERBOOM_73', 'CREATORS_WAP_EXTRATORA_78',
      'CREATORS_PANIFICADORA_80', 'CREATORS_JOOG_X2_85', 'CREATORS_MOM_JEANS_87', 'CREATORS_PANELAS_FERRO_89',
      'CREATORS_PANELAS_AVANT_90', 'CREATORS_PIPOQUEIRA_91', 'CREATORS_PANELAS_FERRO_92', 'CREATORS_BIKE_SPINNING_94',
      'CREATORS_MAQUINA_GELO_95', 'CREATORS_APARELHO_RYO_96', 'CREATORS_JOGO_JANTAR_97', 'CREATORS_SCOOTER_102',
      'CREATORS_PROJETOR_28', 'CREATORS_BODY_106', 'CREATORS_ASPIRADOR_107', 'CREATORS_ESCOVA_108', 'CREATORS_MODELADOR_109',
      'CREATORS_KAPPA_110', 'CREATORS_PROJETOR_111', 'CREATORS_CAMINHAO_112', 'CREATORS_COMEDOURO_113', 'CREATORS_ARCADE_114',
      'CREATORS_FORNO_HQ_115', 'CREATORS_SMART_TV_116', 'CREATORS_FOGAO_117', 'CREATORS_MESA_118', 'CREATORS_FRALDAS_119',
      'CREATORS_SOFA_120', 'CREATORS_TRAVESSEIRO_121', 'CREATORS_PANELA_122', 'CREATORS_LAVADORA_123', 'CREATORS_LIVRO_124',
      'CREATORS_TIRES'
    ];
    for (const v of varNames) {
      try {
        const val = eval(v);
        data[v] = Array.isArray(val) ? val.length : 0;
      } catch (e) {
        data[v] = 'undefined';
      }
    }
    return data;
  };
`;

const modifiedCode = code.replace('function initCarousel() {', 'function initCarousel() {}\n' + injection + '\nfunction _origInit() {');

const ctx = {
  window: { location: { pathname: '/pages/produto-1.html' } },
  document: {
    readyState: 'complete',
    head: { appendChild: () => {} },
    querySelector: () => null,
    querySelectorAll: () => [],
    getElementById: () => null,
    createElement: () => ({ style: {}, classList: { add: () => {} } }),
    body: { appendChild: () => {} },
    addEventListener: () => {}
  },
  IntersectionObserver: class { observe() {} unobserve() {} disconnect() {} },
  global: {}
};

vm.createContext(ctx);
vm.runInContext(modifiedCode, ctx);

const sizes = ctx.global.__getAllDatasets();
console.log("=== RAW DATASET SIZES IN JS/VIDEOS-CRIADORES.JS ===");
const singleOrZero = [];
const multi = [];

for (const [k, v] of Object.entries(sizes)) {
  if (v <= 1) {
    singleOrZero.push({ name: k, count: v });
  } else {
    multi.push({ name: k, count: v });
  }
}

console.log(`\nDatasets with <= 1 videos: ${singleOrZero.length}`);
singleOrZero.forEach(d => console.log(`  ${d.name}: ${d.count}`));

console.log(`\nDatasets with 2+ videos: ${multi.length}`);
multi.forEach(d => console.log(`  ${d.name}: ${d.count}`));
