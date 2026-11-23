$wshell = New-Object -ComObject wscript.shell
$success = $wshell.AppActivate(6992)
Write-Host "AppActivate PID 6992: $success"
Start-Sleep -Milliseconds 800
$wshell.SendKeys('{ESC}')
Start-Sleep -Milliseconds 500
$wshell.SendKeys('^l')
Start-Sleep -Milliseconds 500
$wshell.SendKeys('https://www.tiktok.com/search?q=piscina+1000+litros~')
Write-Host "Comando enviado com sucesso para a tela do Chrome!"
