@echo off
cd /d "%~dp0"
pip install pyinstaller
pyinstaller --onefile --windowed --name JarvisStartup app.py
echo Done. Your exe is in the dist folder.
pause
