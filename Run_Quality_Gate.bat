@echo off
cd /d "%~dp0"
set SCOPE=%1
if "%SCOPE%"=="" set SCOPE=all
if exist ".venv\Scripts\python.exe" (
  .venv\Scripts\python.exe scripts\quality_guard.py --mode full --scope %SCOPE%
) else (
  python scripts\quality_guard.py --mode full --scope %SCOPE%
)
