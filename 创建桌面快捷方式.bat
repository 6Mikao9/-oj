@echo off
chcp 65001 >nul
setlocal
set "ROOT=%~dp0"
set "TARGET=%ROOT%Launch_BUAA_OJ.bat"
set "LNK_NAME=BUAA OJ Platform.lnk"
set "ICON_FILE=%ROOT%assets\buaa_oj.ico"
set "ICON_FALLBACK=imageres.dll,109"

if not exist "%TARGET%" (
    echo [ERROR] Missing launcher: %TARGET%
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "$Desktop = [Environment]::GetFolderPath('Desktop'); $Lnk = Join-Path $Desktop '%LNK_NAME%'; $Wsh = New-Object -ComObject WScript.Shell; $S = $Wsh.CreateShortcut($Lnk); $S.TargetPath = '%TARGET%'; $S.WorkingDirectory = '%ROOT%'; if (Test-Path '%ICON_FILE%') { $S.IconLocation = '%ICON_FILE%' } else { $S.IconLocation = '%ICON_FALLBACK%' }; $S.Description = 'BUAA OJ Platform Launcher'; $S.Save(); Write-Output $Lnk"

if exist "%USERPROFILE%\Desktop\%LNK_NAME%" (
    echo [OK] Shortcut created: %USERPROFILE%\Desktop\%LNK_NAME%
) else (
    echo [ERROR] Failed to create desktop shortcut.
)
