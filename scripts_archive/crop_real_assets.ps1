Add-Type -AssemblyName System.Drawing

$srcPath = "C:\Users\Dell\.gemini\antigravity\brain\40253795-724e-4836-a8ee-923b78213fd5\.user_uploaded\media_1791955477749_4cc57179.png"
$src = [System.Drawing.Bitmap]::FromFile($srcPath)

function Crop-Image($x, $y, $w, $h, $destPath) {
    $rect = New-Object System.Drawing.Rectangle($x, $y, $w, $h)
    $bmp = New-Object System.Drawing.Bitmap($w, $h)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.DrawImage($src, 0, 0, $rect, [System.Drawing.GraphicsUnit]::Pixel)
    $bmp.Save($destPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
    $g.Dispose()
    $bmp.Dispose()
    Write-Output "Salvo: $destPath ($w x $h)"
}

# Avatar da loja
Crop-Image 26 100 64 64 "img\essencia-avatar.jpg"

# Top 1
Crop-Image 17 406 117 117 "img\real-top1.jpg"

# Top 2
Crop-Image 142 406 117 117 "img\real-top2.jpg"

# Top 3
Crop-Image 268 406 117 117 "img\real-top3.jpg"

# Novos lançamentos
Crop-Image 17 760 122 122 "img\real-novo.jpg"

$src.Dispose()
Write-Output "Recorte concluído com sucesso!"
