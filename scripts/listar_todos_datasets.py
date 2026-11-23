import re

with open('js/videos-criadores.js', encoding='utf-8') as f:
    text = f.read()

# Pegar todos os const CREATORS_... = [
all_datasets = re.findall(r'const\s+(CREATORS_[A-Z0-9_]+)\s*=\s*\[', text)
print(f"Total de datasets const CREATORS_ definidos: {len(all_datasets)}")

# Pegar os cases no switch
cases = set(re.findall(r'case\s+(\d+):', text))
print(f"Total de cases no switch: {len(cases)}")

print("\nDatasets definidos no arquivo:")
for ds in all_datasets:
    # Ver se está no switch
    in_switch = ds in text[text.find('switch (prodId)'):text.find('default:')]
    print(f"  {ds}: {'ATIVO NO SWITCH' if in_switch else 'DESCONECTADO'}")
