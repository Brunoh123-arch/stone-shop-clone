import re

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the closing of the IIFE
iife_close_pattern = r'(\s*if\s*\(document\.readyState\s*===\s*[\'"]loading[\'"]\)\s*\{\s*document\.addEventListener\([\'"]DOMContentLoaded[\'"],\s*init\);\s*\}\s*else\s*\{\s*init\(\);\s*\}\s*\}\)\(\);)'
match = re.search(iife_close_pattern, content)

if not match:
    print("Error: Could not locate IIFE close pattern!")
    exit(1)

iife_close_pos = match.start(1)
before_close = content[:iife_close_pos]
iife_close_str = match.group(1)
after_close = content[match.end(1):].strip()

print(f"Before close len: {len(before_close)}")
print(f"After close len: {len(after_close)} (this is the appended datasets)")

# We need to insert after_close BEFORE `function initCarousel()`
target_anchor = "function initCarousel() {"
if target_anchor not in before_close:
    print("Error: target anchor initCarousel not found!")
    exit(1)

# Now prepare the else if branches to add inside initCarousel
dispatch_branches = """
    } else if (prodId === 9 || pageText.includes('split hq 8500') || pageText.includes('ar condicionado hq')) {
      activeDataset = CREATORS_AR_HQ_9;
      contextType = 'ar_hq_9';
    } else if (prodId === 10 || pageText.includes('hisense 12000') || pageText.includes('inverter hisense')) {
      activeDataset = CREATORS_AR_HISENSE_10;
      contextType = 'hisense_10';
    } else if (prodId === 11 || pageText.includes('climatizador oster') || pageText.includes('oster 4 em 1')) {
      activeDataset = CREATORS_CLIMATIZADOR_OSTER_11;
      contextType = 'climatizador_11';
    } else if (prodId === 13 || pageText.includes('piscina pixlar') || pageText.includes('pixlar')) {
      activeDataset = CREATORS_PISCINA_PIXLAR_13;
      contextType = 'piscina_13';
    } else if (prodId === 14 || pageText.includes('churrasqueira arke') || pageText.includes('arke')) {
      activeDataset = CREATORS_CHURRASQUEIRA_ARKE_14;
      contextType = 'churrasqueira_14';
    } else if (prodId === 15 || pageText.includes('churrasqueira biscuitt') || pageText.includes('biscuitt')) {
      activeDataset = CREATORS_CHURRASQUEIRA_BISCUITT_15;
      contextType = 'churrasqueira_15';
    } else if (prodId === 17 || pageText.includes('cadeiras praia mor') || (pageText.includes('cadeira') && pageText.includes('mor') && !pageText.includes('kit'))) {
      activeDataset = CREATORS_CADEIRAS_PRAIA_MOR_17;
      contextType = 'cadeiras_mor_17';
    } else if (prodId === 18 || pageText.includes('kit praia') || (pageText.includes('kit') && pageText.includes('praia'))) {
      activeDataset = CREATORS_KIT_PRAIA_MOR_18;
      contextType = 'kit_praia_18';
    } else if (prodId === 21 || pageText.includes('bola penalty') || pageText.includes('penalty')) {
      activeDataset = CREATORS_BOLA_PENALTY_21;
      contextType = 'bola_21';
    } else if (prodId === 22 || pageText.includes('colchao bestway') || pageText.includes('bestway')) {
      activeDataset = CREATORS_COLCHAO_BESTWAY_22;
      contextType = 'colchao_22';
"""

# Insert the datasets before initCarousel
parts = before_close.split(target_anchor, 1)
new_before_close = parts[0] + "\n\n  // ===== DATASETS DOS PRODUTOS 9, 10, 11, 13, 14, 15, 17, 18, 21, 22 =====\n" + after_close + "\n\n  " + target_anchor + parts[1]

# Now insert dispatch_branches into initCarousel right before `} else {`
else_anchor = "} else {\n      const realVideos = getProductRealVideos(prodId, pageTitle);"
if else_anchor not in new_before_close:
    print("Notice: looking for alternative else anchor...")
    alt_anchor = "} else {\r\n      const realVideos = getProductRealVideos(prodId, pageTitle);"
    if alt_anchor in new_before_close:
        else_anchor = alt_anchor
    else:
        print("Error: else anchor not found!")
        exit(1)

new_before_close = new_before_close.replace(else_anchor, dispatch_branches + "    " + else_anchor, 1)

# Reassemble the file so that iife_close is AT THE VERY END
new_content = new_before_close + "\n" + iife_close_str + "\n"

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("SUCCESS: Refactored js/videos-criadores.js!")
