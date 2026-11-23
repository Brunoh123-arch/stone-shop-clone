with open('js/videos-criadores.js', encoding='utf-8') as f:
    text = f.read()

switch_pos = text.find('switch (prodId)')
print(f"Posição do switch (prodId): {switch_pos}")

datasets = [
    'CREATORS_AIRFRYER_5', 'CREATORS_AIWA_7', 'CREATORS_AIWA_PARTYBOX_8',
    'CREATORS_BIKE_6', 'CREATORS_BIKE_GT_20', 'CREATORS_BIKE_SPINNING_94',
    'CREATORS_BOLA_PENALTY_21', 'CREATORS_CADEIRAS_PRAIA_MOR_17',
    'CREATORS_CHURRASQUEIRA_RODEIO_16', 'CREATORS_CHUVEIRO_32',
    'CREATORS_COLCHAO_BESTWAY_22', 'CREATORS_COMEDOURO_113',
    'CREATORS_ECHODOT_58', 'CREATORS_ESTEIRA_56',
    'CREATORS_JBL_4', 'CREATORS_JBL_BOOMBOX4_35', 'CREATORS_JOGO_JANTAR_97',
    'CREATORS_JOOG_BREAK_61', 'CREATORS_JOOG_ONE_57', 'CREATORS_JOOG_X2_85',
    'CREATORS_KIT_PRAIA_MOR_18', 'CREATORS_MAQUINA_GELO_95',
    'CREATORS_MOM_JEANS_87', 'CREATORS_PAD11_52', 'CREATORS_PANELAS_AVANT_90',
    'CREATORS_PANELAS_FERRO_89', 'CREATORS_PANELAS_FERRO_92',
    'CREATORS_PANIFICADORA_48_84', 'CREATORS_PANIFICADORA_80',
    'CREATORS_PIPOQUEIRA_91', 'CREATORS_PISCINA_12', 'CREATORS_PISCINA_PIXLAR_13',
    'CREATORS_POCO_X7_PRO_36', 'CREATORS_PROJETOR_111', 'CREATORS_REBECCA_BONBON_28',
    'CREATORS_REDMI_WATCH_63', 'CREATORS_SABALA_31', 'CREATORS_SCOOTER_102',
    'CREATORS_SECADORA_MUELLER_70', 'CREATORS_SMART_TV_116', 'CREATORS_SOFA_SENSES_65',
    'CREATORS_STARLINK_59', 'CREATORS_SWITCH_55', 'CREATORS_WAAW_HYPERBOOM_73',
    'CREATORS_WAP_EXTRATORA_78', 'CREATORS_APARELHO_RYO_96', 'CREATORS_ARCADE_114'
]

after_switch = []
before_switch = []
for ds in datasets:
    p = text.find(f'const {ds}')
    if p == -1:
        p = text.find(ds)
    if p > switch_pos:
        after_switch.append((ds, p))
    else:
        before_switch.append((ds, p))

print(f"Datasets declarados ANTES do switch: {len(before_switch)}")
print(f"Datasets declarados DEPOIS do switch: {len(after_switch)}")
if after_switch:
    print("Primeiros declarados depois do switch:")
    for ds, p in after_switch[:5]:
        print(f"  {ds} na posição {p} (switch está em {switch_pos})")
