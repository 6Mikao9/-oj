@echo off
cd /d "%~dp0"

echo ========================================
echo BUAA OJ System Initialization
echo ========================================
echo.

REM Create directory structure
echo Creating directories...
mkdir data\years 2>nul
mkdir data\submissions 2>nul
mkdir data\solutions 2>nul
mkdir problems 2>nul

echo.
echo Initialization complete!
echo.
echo You can now:
echo 1. Run GUI: python buaa_gui.py
echo 2. Run CLI: python buaa_oj.py
echo.

pause
