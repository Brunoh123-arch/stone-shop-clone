param(
  [int]$Port = 3333,
  [int]$DaemonPort = 3334,
  [switch]$Detach
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$BinDir = Join-Path $Root '.studio-bin'
$RuntimeDir = Join-Path $env:LOCALAPPDATA 'stone-studio'

foreach ($d in @($BinDir, $RuntimeDir)) {
  if (-not (Test-Path $d)) {
    New-Item -ItemType Directory -Path $d -Force | Out-Null
  }
}

# Limpa processos anteriores nas portas 3333 / 3334 para nunca dar EADDRINUSE
foreach ($p in @($Port, $DaemonPort)) {
  $conns = Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue
  foreach ($c in $conns) {
    if ($c.OwningProcess -gt 4) {
      Stop-Process -Id $c.OwningProcess -Force -ErrorAction SilentlyContinue
    }
  }
}
Get-Process -Name 'cloudflared' -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Localiza ou baixa cloudflared oficial
$CfCmd = Get-Command cloudflared -ErrorAction SilentlyContinue
if ($CfCmd) {
  $CloudflaredExe = $CfCmd.Source
} else {
  $CloudflaredExe = Join-Path $BinDir 'cloudflared.exe'
  if (-not (Test-Path $CloudflaredExe)) {
    Write-Host '☁️ Baixando binário oficial do Cloudflare Tunnel...' -ForegroundColor Cyan
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile $CloudflaredExe -UseBasicParsing
  }
}

# Gera token criptográfico da sessão
if (-not $env:STUDIO_TOKEN) {
  $bytes = New-Object byte[] 12
  [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
  $Token = ($bytes | ForEach-Object { $_.ToString('x2') }) -join ''
} else {
  $Token = $env:STUDIO_TOKEN
}

$env:STUDIO_MODE = '1'
$env:STUDIO_TOKEN = $Token
$env:STUDIO_PORT = "$Port"
$env:STUDIO_DAEMON_PORT = "$DaemonPort"
$env:PORT = "$Port"

# Logs e URL ativa ficam em %LOCALAPPDATA%\stone-studio (fora do webroot!)
$DaemonLog = Join-Path $RuntimeDir 'daemon.log'
$DaemonErr = Join-Path $RuntimeDir 'daemon.err.log'
$ServerLog = Join-Path $RuntimeDir 'server.log'
$ServerErr = Join-Path $RuntimeDir 'server.err.log'
$CfLog = Join-Path $RuntimeDir 'cloudflared.log'
$CfErr = Join-Path $RuntimeDir 'cloudflared.err.log'
$UrlFile = Join-Path $RuntimeDir 'active-url.txt'
if (Test-Path $UrlFile) { Remove-Item $UrlFile -Force -ErrorAction SilentlyContinue }

$DaemonProc = $null
$ServerProc = $null
$CfProc = $null

try {
  Write-Host '🔥 Subindo Daemon Aquecido Zero-Áudio (Playwright + Catbox 4x)...' -ForegroundColor Yellow
  $DaemonProc = Start-Process -FilePath 'python' -ArgumentList @('scripts/studio/studio_daemon.py') -WorkingDirectory $Root -WindowStyle Hidden -RedirectStandardOutput $DaemonLog -RedirectStandardError $DaemonErr -PassThru

  for ($h = 0; $h -lt 25; $h++) {
    Start-Sleep -Milliseconds 500
    try {
      $resp = Invoke-WebRequest -Uri "http://127.0.0.1:$DaemonPort/health" -UseBasicParsing -TimeoutSec 2
      if ($resp.StatusCode -eq 200) { break }
    } catch {}
  }

  Write-Host '⚡ Subindo Stone Studio Engine...' -ForegroundColor Yellow
  $ServerProc = Start-Process -FilePath 'node' -ArgumentList @('server.js') -WorkingDirectory $Root -WindowStyle Hidden -RedirectStandardOutput $ServerLog -RedirectStandardError $ServerErr -PassThru

  for ($s = 0; $s -lt 20; $s++) {
    Start-Sleep -Milliseconds 400
    try {
      $resp = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/importador?key=$Token" -UseBasicParsing -TimeoutSec 2
      if ($resp.StatusCode -eq 200) { break }
    } catch {}
  }

  Write-Host '🌐 Abrindo Túnel HTTPS Público na Cloudflare...' -ForegroundColor Cyan
  $CfProc = Start-Process -FilePath $CloudflaredExe -ArgumentList @('tunnel', '--no-autoupdate', '--url', "http://127.0.0.1:$Port") -WorkingDirectory $Root -WindowStyle Hidden -RedirectStandardOutput $CfLog -RedirectStandardError $CfErr -PassThru

  $TunnelBase = $null
  for ($i = 0; $i -lt 40; $i++) {
    Start-Sleep -Milliseconds 750
    foreach ($lf in @($CfErr, $CfLog)) {
      if (Test-Path $lf) {
        $raw = Get-Content $lf -Raw -ErrorAction SilentlyContinue
        if ($raw -match '(https://[a-z0-9-]+\.trycloudflare\.com)') {
          $TunnelBase = $Matches[1]
          break
        }
      }
    }
    if ($TunnelBase) { break }
  }

  if (-not $TunnelBase) {
    throw 'Não foi possível capturar a URL do Cloudflare Tunnel em 30s.'
  }

  $StudioUrl = "$TunnelBase/importador?key=$Token"
  Set-Content -Path $UrlFile -Value $StudioUrl -Encoding UTF8
  try { Set-Clipboard -Value $StudioUrl } catch {}

  Write-Host ''
  Write-Host '====================================================================' -ForegroundColor Green
  Write-Host '🚀 STONE STUDIO AO VIVO (PC + CELULAR VIA CLOUDFLARE HTTPS)' -ForegroundColor Green
  Write-Host "👉 $StudioUrl" -ForegroundColor White
  Write-Host '📋 (Link já copiado automático pro seu Ctrl+V!)' -ForegroundColor DarkGray
  Write-Host '====================================================================' -ForegroundColor Green
  Write-Host ''

  if ($Detach) {
    return
  }

  while (-not $ServerProc.HasExited -and -not $CfProc.HasExited) {
    Start-Sleep -Seconds 3
  }
} finally {
  if (-not $Detach) {
    foreach ($proc in @($CfProc, $ServerProc, $DaemonProc)) {
      if ($proc -and -not $proc.HasExited) {
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
      }
    }
  }
}
