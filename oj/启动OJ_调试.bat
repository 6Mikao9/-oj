@echo off
cd /d "%~dp0"
echo Starting BUAA OJ with debug output...
echo =========================================
python buaa_oj_v3.py 2>&1
echo =========================================
echo If you see errors above, please copy them and send to me.
pause
