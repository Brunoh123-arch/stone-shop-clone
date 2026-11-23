with open('js/videos-criadores.js', encoding='utf-8') as f:
    text = f.read()

datasets = [
    'CREATORS_BIKE_GT_20', 'CREATORS_BOLA_PENALTY_21', 'CREATORS_COLCHAO_BESTWAY_22',
    'CREATORS_JBL_BOOMBOX4_35', 'CREATORS_PAD11_52', 'CREATORS_SWITCH_55',
    'CREATORS_JOOG_ONE_57', 'CREATORS_ECHODOT_58', 'CREATORS_STARLINK_59',
    'CREATORS_JOOG_BREAK_61', 'CREATORS_REDMI_WATCH_63', 'CREATORS_SOFA_SENSES_65',
    'CREATORS_SECADORA_MUELLER_70', 'CREATORS_WAAW_HYPERBOOM_73', 'CREATORS_PANIFICADORA_80',
    'CREATORS_JOOG_X2_85', 'CREATORS_MOM_JEANS_87', 'CREATORS_PANELAS_FERRO_89',
    'CREATORS_PIPOQUEIRA_91', 'CREATORS_PANELAS_FERRO_92', 'CREATORS_BIKE_SPINNING_94',
    'CREATORS_MAQUINA_GELO_95', 'CREATORS_APARELHO_RYO_96', 'CREATORS_JOGO_JANTAR_97'
]

existentes = []
faltando = []
for ds in datasets:
    if ds in text:
        existentes.append(ds)
    else:
        faltando.append(ds)

print(f"Existentes no js/videos-criadores.js: {len(existentes)}")
print(f"Faltando no js/videos-criadores.js: {len(faltando)}")
if faltando:
    print("Faltam:", faltando)
