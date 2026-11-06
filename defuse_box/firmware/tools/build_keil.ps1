param([string]$Uv4='E:\keil5\UV4\UV4.exe')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
& (Join-Path $PSScriptRoot 'fix_keil_encoding.ps1') -ProjectDirectory $root
foreach($dir in @('BuildLogs','release','Objects','Listings')){New-Item -ItemType Directory -Force -Path (Join-Path $root $dir) | Out-Null}
$p=Start-Process -FilePath $Uv4 -ArgumentList '-r Project.uvprojx -t Defuse_Base -j0 -o BuildLogs\Keil_Defuse_Base.log' -WorkingDirectory $root -WindowStyle Hidden -Wait -PassThru
Get-Content -LiteralPath (Join-Path $root 'BuildLogs\Keil_Defuse_Base.log')
if($p.ExitCode -ne 0){throw "Build failed: $($p.ExitCode)"}
Copy-Item -LiteralPath (Join-Path $root 'Objects\Defuse_Base\Defuse_Base.hex') -Destination (Join-Path $root 'release\Defuse_Base.hex')
