@echo off
cd /d "%~dp0"
set PYTHONNOUSERSITE=1
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -X utf8 server.py
) else (
  python -X utf8 server.py
)
pause
