param([string]$Gcc='C:\mingw64\bin\gcc.exe')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
Push-Location $root
try {
 New-Item -ItemType Directory -Force -Path BuildLogs,Previews | Out-Null
 & $Gcc -std=c99 -Wall -Wextra -Wno-unused-function -DMAZE_HOST_VIEW -IHardware -IUser tests/test_base.c Hardware/display.c Hardware/ui_assets.c Hardware/ui_pages.c Hardware/ui_actions.c -o BuildLogs/test_base.exe
 if($LASTEXITCODE -ne 0){throw 'Host compile failed'}
 & .\BuildLogs\test_base.exe | Tee-Object -FilePath BuildLogs\host_tests.log
 if($LASTEXITCODE -ne 0){throw 'Host tests failed'}
} finally {Pop-Location}
