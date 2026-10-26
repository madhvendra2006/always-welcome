# always-welcome
This one i made for my own satisfaction

# Jarvis Startup

A no-login startup app for Windows and Mac.

On login, it plays your welcome video fullscreen, closes it by itself, then plays your music in the background on loop until you stop it. No account, no cloud, no data sent anywhere. All settings are saved locally in `settings.json`, next to the app.

## What it does

1. Welcome video plays fullscreen.
2. It closes automatically, no click needed, and your wallpaper comes back.
3. Background music starts minimized and loops until you stop it.

## Features

- Start: welcome video, then background music.
- Start Music: background music only, no video.
- Stop Music: stops the music instantly, even if the app window was closed.
- Run Startup Sequence: test the full login flow.
- Install to Startup / Remove from Startup: run on login, or stop running on login.
- Choose VLC: point the app to VLC if it is not in the default location.
- Choose your own video, music folder, and video length.
- Works on Windows and Mac with the same folder layout.

## Requirements

- Python 3
- VLC media player, free from videolan.org

The app does not play video or music itself. It tells VLC what to play. That keeps it simple and the same on both systems.

## Quick start

### Windows

1. Download this repo, Extract All, open the `jarvis-startup-app` folder.
2. Install VLC.
3. Put your welcome video in the folder as `welcome.mp4`.
4. Put your songs directly in the `music` folder, not in a subfolder inside it. Keep the startup list small, a very large folder makes VLC slow to start.
5. Double-click `run-windows.bat`, or open a terminal in this folder and run:
   ```
   py app.py
   ```
   If `py` does not work, use `python app.py`.
6. Press Save, then Start to test.

### Mac

1. Download this repo, open the `jarvis-startup-app` folder.
2. Install VLC for Mac.
3. Put your welcome video in the folder as `welcome.mp4`.
4. Put your songs directly in the `music` folder.
5. Double-click `run-mac.command`, or open Terminal in this folder and run:
   ```
   python3 app.py
   ```
6. Press Save, then Start to test.

On first run on Mac, if macOS blocks the unsigned file, right-click it and choose Open.

## Run on login

Press Install to Startup in the app, then restart and log in to test.

- Windows: this adds a Run key for the current user only.
- Mac: this adds a LaunchAgent at `~/Library/LaunchAgents/com.jarvisstartup.plist`.

On login the app runs with `--run`, so there is no settings window, only the video, then the music.

Press Remove from Startup to stop it running on login.

Closing the app window does not stop the music, because the music runs as its own VLC process. Press Stop Music in the app, or close VLC, to stop it.

## Buttons

| Button | What it does |
| --- | --- |
| Save | Saves your video, music folder, VLC path, and video length |
| Start | Plays the welcome video, then background music |
| Run Startup Sequence | Same as Start, for testing |
| Start Music | Background music only, no video |
| Stop Music | Stops background music |
| Install to Startup | Runs on login |
| Remove from Startup | Stops running on login |

## Project structure

```
jarvis-startup-app/
  app.py              The app
  welcome.mp4         Your welcome video, add your own
  music/              Your songs, add your own
  settings.json       Created when you press Save
  run-windows.bat     Double-click launcher for Windows
  run-mac.command     Double-click launcher for Mac
  build-windows.bat   Build a Windows .exe
  build-mac.sh        Build a Mac .app
```

## Build a real app

A `.exe` must be built on Windows, and a `.app` must be built on Mac. You cannot build one from the other system.

Windows: double-click `build-windows.bat`. Your `.exe` will be in the `dist` folder.

Mac: run `build-mac.sh`. Your `.app` will be in the `dist` folder.

VLC still has to be installed on that computer, it is not included in the build.

## Troubleshooting

- `Python was not found` on Windows: use `py app.py` instead of `python app.py`.
- App says VLC is not installed, but VLC opens videos: press Choose VLC, pick `vlc.exe` from wherever VLC is installed, press Save, then Start.
- Music plays twice: press Stop Music first, then Start Music. The app now stops old music before starting new music.
- Music starts slowly: your music folder is too large. Keep only your startup songs in it.
- Video does not close: check the video length in seconds in the app matches your video. The app closes VLC after that many seconds.
- After closing the app, music keeps playing: that is VLC, not the app. Press Stop Music, or in a terminal run `taskkill /IM vlc.exe /F` on Windows.

## Privacy

No login, no account, no tracking, no uploads. Your video, music, and settings stay on your computer.

## Add your own media

Add your own welcome video and your own music. Do not upload videos or songs you do not own the rights to in a public repo.

## Built with

Python, Tkinter, and VLC.
