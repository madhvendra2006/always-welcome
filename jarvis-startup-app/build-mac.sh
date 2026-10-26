#!/bin/bash
cd "$(dirname "$0")"
pip3 install pyinstaller
pyinstaller --onefile --windowed --name JarvisStartup app.py
echo "Done. Your app is in the dist folder."
