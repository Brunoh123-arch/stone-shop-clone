Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$code = @"
using System;
using System.Runtime.InteropServices;
using System.Drawing;
using System.Windows.Forms;

public class WinMouse {
    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);

    public static void ClickAt(int x, int y) {
        Cursor.Position = new Point(x, y);
        System.Threading.Thread.Sleep(100);
        mouse_event(0x0002, 0, 0, 0, UIntPtr.Zero); // Left Down
        System.Threading.Thread.Sleep(50);
        mouse_event(0x0004, 0, 0, 0, UIntPtr.Zero); // Left Up
    }
}
"@

Add-Type -TypeDefinition $code -ReferencedAssemblies System.Windows.Forms, System.Drawing

Write-Host "1. Fechando o balao de restaurar paginas..."
[WinMouse]::ClickAt(1035, 132)
Start-Sleep -Milliseconds 600

Write-Host "2. Clicando na barra de endereco do Chrome..."
[WinMouse]::ClickAt(400, 110)
Start-Sleep -Milliseconds 500

Write-Host "3. Selecionando tudo e digitando a busca..."
[System.Windows.Forms.SendKeys]::SendWait("^a")
Start-Sleep -Milliseconds 200
[System.Windows.Forms.SendKeys]::SendWait("https://www.tiktok.com/search?q=piscina+1000+litros{ENTER}")

Write-Host "Navegacao automatica concluida com sucesso na tela do usuario!"
