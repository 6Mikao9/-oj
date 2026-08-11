@echo off
chcp 65001 >nul

REM 尝试多种Python路径
set PYTHON_CMD=""

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\pythonw.exe" (
    set PYTHON_CMD="C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\pythonw.exe"
) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\pythonw.exe" (
    set PYTHON_CMD="C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\pythonw.exe"
) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\pythonw.exe" (
    set PYTHON_CMD="C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\pythonw.exe"
) else if exist "C:\Python313\pythonw.exe" (
    set PYTHON_CMD="C:\Python313\pythonw.exe"
) else if exist "C:\Python312\pythonw.exe" (
    set PYTHON_CMD="C:\Python312\pythonw.exe"
) else if exist "C:\Python311\pythonw.exe" (
    set PYTHON_CMD="C:\Python311\pythonw.exe"
)

if %PYTHON_CMD%=="" (
    msg * "Python not found! Please install Python first."
    exit /b 1
)

start "" %PYTHON_CMD% "%~dp0buaa_oj_v4.py"
