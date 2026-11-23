Add-Type -AssemblyName System.Drawing

$srcPath = "C:\Users\Dell\.gemini\antigravity\brain\40253795-724e-4836-a8ee-923b78213fd5\.user_uploaded\media_1791962538144_cbbc0f9c.png"
$src = [System.Drawing.Bitmap]::FromFile($srcPath)

function Crop-Exact($x, $y, $w, $h, $destPath) {
    $rect = New-Object System.Drawing.Rectangle($x, $y, $w, $h)
    $bmp = New-Object System.Drawing.Bitmap($w, $h)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.DrawImage($src, 0, 0, $rect, [System.Drawing.GraphicsUnit]::Pixel)
    $bmp.Save($destPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
    $g.Dispose()
    $bmp.Dispose()
    Write-Output "Recortado com sucesso: $destPath ($w x $h)"
}

# Coordenadas exatas das 3 fotos (sem o texto 'Chinelo' embaixo!)
# Na imagem 394x427:
# TOP 1 (Cruzada Glitter)
Crop-Exact 16 138 114 114 "C:\Users\Dell\Downloads\stone_shop_clone\img\real-top1.jpg"

# TOP 2 (NO STRASS)
Crop-Exact 141 138 114 114 "C:\Users\Dell\Downloads\stone_shop_clone\img\real-top2.jpg"

# TOP 3 (LUXO STRASS)
Crop-Exact 265 138 114 114 "C:\Users\Dell\Downloads\stone_shop_clone\img\real-top3.jpg"

$src.Dispose()
Write-Output "✅ Todas as fotos dos Principais Produtos recortadas 100% limpas!"
