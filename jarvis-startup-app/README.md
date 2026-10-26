# Jarvis Startup App

No login, no account. On login, it plays welcome.mp4 fullscreen,
closes it by itself, then plays your music folder on loop.

## What is in this folder

- app.py - the whole app, Windows and Mac, Python only.
- welcome.mp4 - your Jarvis welcome video, 62 seconds, sharpened.
- music/ - put your songs in here. It starts empty on purpose,
  add your own songs, they loop.
- settings.json - created the first time you press Save in the app.

## Run it (test first)

Open a terminal IN this folder, then run:

Windows: python app.py
Mac: python3 app.py

You need VLC installed first, free from videolan.org.

In the window: pick your video and music folder, press Save,
then press Run Startup Sequence to test. It plays the video
fullscreen, closes it, then loops your music. Close VLC to stop
the music.

## Run it on login

In the window, press Install to Startup, then restart to test.
Press Remove from Startup to stop it running on login.

Windows uses a Run key for your user only.
Mac uses a LaunchAgent in ~/Library/LaunchAgents.

## Make it a real app file for friends

Build it separately on each system, you cannot cross-build:

pip install pyinstaller
pyinstaller --onefile --windowed app.py

Windows build gives a .exe, Mac build gives a .app.
Copy the whole folder (app file, welcome.mp4, music folder)
to your friend, and they press Install to Startup in the app.

On a Mac, the first time you open an unsigned app, right-click
it and choose Open, then Open again. That is normal for a
student app that is not signed by Apple.
