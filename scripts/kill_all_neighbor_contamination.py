import re

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Reescrever a funcao buildNichePool para nunca mais usar fallback de outro nicho
pattern_pool_func = r'function buildNichePool\(primaryList, fallbackNicheList\)\s*\{.*?return result;\s*\}'
replacement_pool_func = """function buildNichePool(primaryList, fallbackNicheList) {
      // BLINDAGEM SOBERANA ZIKA: ISOLAMENTO 1:1 ESTRITO
      // PROIBICAO ABSOLUTA DE EMPRESTAR MIDIA DO VIZINHO
      if (!primaryList || !Array.isArray(primaryList) || primaryList.length === 0) {
        return [];
      }
      return primaryList;
    }"""

new_code, n_subs = re.subn(pattern_pool_func, replacement_pool_func, code, flags=re.DOTALL)
print(f"Substituicao buildNichePool: {n_subs}")

# 2. Corrigir casos no switch (prodId) que apontavam para produtos vizinhos bizarros
# Mapeamento de correcões estritas
bad_cases = {
    'case 16:': "case 16:\n        activeDataset = CREATORS_CHURRASQUEIRA_RODEIO_16;\n        contextType = 'churrasqueira_16';\n        break;",
    'case 23:': "case 23:\n        activeDataset = [];\n        contextType = 'potes_23';\n        break;",
    'case 24:': "case 24:\n        activeDataset = [];\n        contextType = 'triciclo_24';\n        break;",
    'case 26:': "case 26:\n        activeDataset = [];\n        contextType = 'carrinho_26';\n        break;",
    'case 40:': "case 40:\n        activeDataset = [];\n        contextType = 'microondas_40';\n        break;",
    'case 54:': "case 54:\n        activeDataset = [];\n        contextType = 'purificador_54';\n        break;",
    'case 64:': "case 64:\n        activeDataset = [];\n        contextType = 'bateria_64';\n        break;",
    'case 79:': "case 79:\n        activeDataset = [];\n        contextType = 'lavaloucas_79';\n        break;",
    'case 82:': "case 82:\n        activeDataset = [];\n        contextType = 'lavaeseca_82';\n        break;",
    'case 99:': "case 99:\n        activeDataset = [];\n        contextType = 'portugal_99';\n        break;",
    'case 100:': "case 100:\n        activeDataset = [];\n        contextType = 'iphone_100';\n        break;",
    'case 103:': "case 103:\n        activeDataset = [];\n        contextType = 'vestido_103';\n        break;",
    'case 88:': "case 88:\n        activeDataset = [];\n        contextType = 'alfaiataria_88';\n        break;",
    'case 48:': "case 48:\n        activeDataset = [];\n        contextType = 'panificadora_48';\n        break;",
    'case 45:': "case 45:\n        activeDataset = [];\n        contextType = 'prancha_45';\n        break;",
}

for case_tag, clean_block in bad_cases.items():
    pattern = re.escape(case_tag) + r'.*?break;'
    new_code, count = re.subn(pattern, clean_block, new_code, flags=re.DOTALL)
    print(f"Corrigido {case_tag}: {count}")

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("js/videos-criadores.js BLINDADO COM ISOLAMENTO 1:1 ESTRITO!")
