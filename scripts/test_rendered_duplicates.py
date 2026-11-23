import asyncio, glob, os
from playwright.async_api import async_playwright

async def test_pages():
    files = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(os.path.basename(x).split('-')[1].split('.')[0]))
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 390, 'height': 844})
        page = await context.new_page()
        
        results = []
        # Test all files
        for fpath in files:
            abs_path = os.path.abspath(fpath).replace('\\', '/')
            url = f'file:///{abs_path}'
            try:
                await page.goto(url, wait_until='domcontentloaded', timeout=10000)
                await page.wait_for_timeout(300) # wait for app.js execution
                
                # Check counts of info rows and protections
                data = await page.evaluate('''() => {
                    const protections = Array.from(document.querySelectorAll('.info-row-item-protection, .protection-section'))
                        .filter(el => el.textContent.includes('Proteção do cliente'));
                    const pRows = document.querySelectorAll('.product-info-rows');
                    const fretes = Array.from(document.querySelectorAll('.info-row-item, .info-row-envio'))
                        .filter(el => el.textContent.includes('Frete') || el.textContent.includes('Receba'));
                    const opcoes = Array.from(document.querySelectorAll('.info-row-item, .info-row-opcoes'))
                        .filter(el => el.textContent.includes('opç') || el.textContent.includes('Opç'));
                    const creators = document.querySelectorAll('#creators-section, .creators-section');
                    
                    return {
                        protectionsCount: protections.length,
                        pRowsCount: pRows.length,
                        fretesCount: fretes.length,
                        opcoesCount: opcoes.length,
                        creatorsCount: creators.length
                    };
                }''')
                
                if data['protectionsCount'] > 1 or data['pRowsCount'] > 1 or data['fretesCount'] > 1 or data['opcoesCount'] > 1 or data['creatorsCount'] > 1:
                    results.append((os.path.basename(fpath), data))
            except Exception as e:
                results.append((os.path.basename(fpath), f'ERROR: {e}'))
                
        await browser.close()
        
        print(f'Total tested: {len(files)}')
        print(f'Total with duplicates: {len(results)}')
        for name, res in results:
            print(f'{name}: {res}')

asyncio.run(test_pages())
