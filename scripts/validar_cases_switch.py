with open('js/videos-criadores.js', encoding='utf-8') as f:
    text = f.read()

cases_to_add = [
    (4, 'CREATORS_JBL_4', 'jbl_4'),
    (5, 'CREATORS_AIRFRYER_5', 'airfryer_5'),
    (6, 'CREATORS_BIKE_6', 'bike_6'),
    (7, 'CREATORS_AIWA_7', 'aiwa_7'),
    (8, 'CREATORS_AIWA_PARTYBOX_8', 'aiwa_partybox_8'),
    (9, 'CREATORS_AR_HQ_9', 'ar_hq_9'),
    (10, 'CREATORS_AR_HISENSE_10', 'ar_hisense_10'),
    (11, 'CREATORS_CLIMATIZADOR_OSTER_11', 'climatizador_oster_11'),
    (12, 'CREATORS_PISCINA_12', 'piscina_12'),
    (13, 'CREATORS_PISCINA_PIXLAR_13', 'piscina_pixlar_13'),
    (16, 'CREATORS_CHURRASQUEIRA_RODEIO_16', 'churrasqueira_rodeio_16'),
    (17, 'CREATORS_CADEIRAS_PRAIA_MOR_17', 'cadeiras_praia_mor_17'),
    (18, 'CREATORS_KIT_PRAIA_MOR_18', 'kit_praia_mor_18'),
    (20, 'CREATORS_BIKE_GT_20', 'bike_gt_20'),
    (21, 'CREATORS_BOLA_PENALTY_21', 'bola_penalty_21'),
    (22, 'CREATORS_COLCHAO_BESTWAY_22', 'colchao_bestway_22'),
    (27, 'CREATORS_AR_LG_27', 'ar_lg_27'),
    (28, 'CREATORS_REBECCA_BONBON_28', 'rebecca_bonbon_28'),
    (29, 'CREATORS_AR_HQ_29', 'ar_hq_29'),
    (30, 'CREATORS_CLIMATIZADOR_MIDEA_30', 'climatizador_midea_30'),
    (31, 'CREATORS_SABALA_31', 'sabala_31'),
    (32, 'CREATORS_CHUVEIRO_32', 'chuveiro_32'),
    (35, 'CREATORS_JBL_BOOMBOX4_35', 'jbl_boombox4_35'),
    (36, 'CREATORS_POCO_X7_PRO_36', 'poco_x7_pro_36'),
    (44, 'CREATORS_CLIMATIZADOR_VENTISOL_44', 'climatizador_ventisol_44'),
    (47, 'CREATORS_WAP_EXTRATORA_78', 'wap_extratora_47'),
    (48, 'CREATORS_PANIFICADORA_48_84', 'panificadora_48'),
    (52, 'CREATORS_PAD11_52', 'pad11_52'),
    (55, 'CREATORS_SWITCH_55', 'switch_55'),
    (56, 'CREATORS_ESTEIRA_56', 'esteira_56'),
    (57, 'CREATORS_JOOG_ONE_57', 'joog_one_57'),
    (58, 'CREATORS_ECHODOT_58', 'echodot_58'),
    (59, 'CREATORS_STARLINK_59', 'starlink_59'),
    (61, 'CREATORS_JOOG_BREAK_61', 'joog_break_61'),
    (63, 'CREATORS_REDMI_WATCH_63', 'redmi_watch_63'),
    (65, 'CREATORS_SOFA_SENSES_65', 'sofa_senses_65'),
    (70, 'CREATORS_SECADORA_MUELLER_70', 'secadora_mueller_70'),
    (73, 'CREATORS_WAAW_HYPERBOOM_73', 'waaw_hyperboom_73'),
    (78, 'CREATORS_WAP_EXTRATORA_78', 'wap_extratora_78'),
    (80, 'CREATORS_PANIFICADORA_80', 'panificadora_80'),
    (85, 'CREATORS_JOOG_X2_85', 'joog_x2_85'),
    (87, 'CREATORS_MOM_JEANS_87', 'mom_jeans_87'),
    (89, 'CREATORS_PANELAS_FERRO_89', 'panelas_ferro_89'),
    (90, 'CREATORS_PANELAS_AVANT_90', 'panelas_avant_90'),
    (91, 'CREATORS_PIPOQUEIRA_91', 'pipoqueira_91'),
    (92, 'CREATORS_PANELAS_FERRO_92', 'panelas_ferro_92'),
    (94, 'CREATORS_BIKE_SPINNING_94', 'bike_spinning_94'),
    (95, 'CREATORS_MAQUINA_GELO_95', 'maquina_gelo_95'),
    (96, 'CREATORS_APARELHO_RYO_96', 'aparelho_ryo_96'),
    (97, 'CREATORS_JOGO_JANTAR_97', 'jogo_jantar_97'),
    (102, 'CREATORS_SCOOTER_102', 'scooter_102'),
    (111, 'CREATORS_PROJETOR_111', 'projetor_111'),
    (113, 'CREATORS_COMEDOURO_113', 'comedouro_113'),
    (114, 'CREATORS_ARCADE_114', 'arcade_114'),
    (116, 'CREATORS_SMART_TV_116', 'smart_tv_116'),
]

print("Validando presença das variáveis:")
missing = []
for pid, var, ctx in cases_to_add:
    if f"const {var}" not in text:
        missing.append((pid, var))

print(f"Total validados: {len(cases_to_add) - len(missing)} de {len(cases_to_add)}")
if missing:
    print("Faltam declarações const para:", missing)
else:
    print("100% DAS CONSTANTES EXISTEM E ESTÃO PRONTAS PARA O SWITCH!")
