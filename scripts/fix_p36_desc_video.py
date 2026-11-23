with open('pages/produto-36.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace vyssbh.mp4 in produto-36.html with cell video
# 8octvc.mp4 is cell video
if 'vyssbh.mp4' in html:
    html = html.replace('https://files.catbox.moe/vyssbh.mp4', 'https://files.catbox.moe/8octvc.mp4')
    with open('pages/produto-36.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Fixed pages/produto-36.html video from vyssbh (JBL) to 8octvc (cell)!')
else:
    print('vyssbh not found in produto-36.html')
