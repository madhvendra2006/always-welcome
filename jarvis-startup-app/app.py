#!/usr/bin/env python3
"""
Jarvis Startup App - Windows and Mac, no login, no account.

What it does:
  On run, it plays welcome.mp4 fullscreen, closes it by itself,
  then plays your music folder on loop in the background.

How to use it:
  1. Put this file, welcome.mp4, and a music folder in one folder.
     Example: JarvisStartup/app.py, JarvisStartup/welcome.mp4,
              JarvisStartup/music/your-songs-here.mp3
  2. Windows: open a terminal IN that folder, run: python app.py
     Mac: open Terminal IN that folder, run: python3 app.py
  3. In the window, pick your video and music folder, press Save,
     then press Run Startup Sequence to test it.
  4. Press Install to Startup to make it run on login.
     Press Remove from Startup to stop it running on login.
     On login it runs with --run, so it plays the video and music
     without opening this settings window.

You need VLC installed (free, videolan.org). This app does not
play video itself, it tells VLC what to play. That keeps the app
simple and the same on Windows and Mac.

Settings are saved in settings.json, in the same folder as this
file, so each person keeps their own video and music choices.
No data is sent anywhere. There is no login.
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

# The folder this file lives in. All paths below are relative to it,
# so you can move the whole JarvisStartup folder and it still works.
BASE_DIR = Path(__file__).resolve().parent
SETTINGS_FILE = BASE_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "welcome_video": str(BASE_DIR / "welcome.mp4"),
    "music_folder": str(BASE_DIR / "music"),
    "welcome_seconds": 62,
}


def load_settings():
    """Read settings.json, or use the defaults if it is missing."""
    try:
        saved = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        settings = dict(DEFAULT_SETTINGS)
        settings.update(saved)
        return settings
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(settings):
    SETTINGS_FILE.write_text(
        json.dumps(settings, indent=2), encoding="utf-8"
    )


def find_vlc():
    """Find the VLC player for the system you are on."""
    system = platform.system()
    if system == "Windows":
        candidate = Path(r"C:\Program Files\VideoLAN\VLC\vlc.exe")
        if candidate.exists():
            return str(candidate)
        candidate = Path(r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe")
        if candidate.exists():
            return str(candidate)
    elif system == "Darwin":  # Mac
        candidate = Path("/Applications/VLC.app/Contents/MacOS/VLC")
        if candidate.exists():
            return str(candidate)
    found = shutil.which("vlc")
    if found:
        return found
    return None


def get_video_seconds(settings):
    """How long the welcome video lasts, in seconds.

    Tries ffprobe if it is installed, otherwise uses the number
    saved in settings. The video in this folder is 62 seconds.
    """
    video = Path(settings["welcome_video"])
    ffprobe = shutil.which("ffprobe")
    if ffprobe and video.exists():
        try:
            out = subprocess.run(
                [ffprobe, "-v", "error", "-show_entries",
                 "format=duration", "-of", "csv=p=0", str(video)],
                capture_output=True, text=True, timeout=10,
            )
            return int(float(out.stdout.strip()))
        except Exception:
            pass
    try:
        return int(settings.get("welcome_seconds", 62))
    except Exception:
        return 62


def run_startup_sequence(settings):
    """Play the welcome video fullscreen, then loop the music.

    Returns True if it started, False if something is missing.
    This is the part that runs on login, with --run.
    """
    vlc = find_vlc()
    if not vlc:
        print("VLC is not installed. Install it free from videolan.org.")
        return False
    video = Path(settings["welcome_video"])
    music = Path(settings["music_folder"])
    if not video.exists():
        print(f"Welcome video not found: {video}")
        return False
    if not music.exists() or not any(music.iterdir()):
        print(f"Music folder is empty or missing: {music}")
        return False

    print("Starting welcome video...")
    video_process = subprocess.Popen([vlc, "--fullscreen", str(video)])
    time.sleep(get_video_seconds(settings))
    video_process.terminate()
    try:
        video_process.wait(timeout=5)
    except Exception:
        video_process.kill()
    print("Welcome done, wallpaper is back. Starting music...")
    start_music(settings)
    print("Music is playing on loop in the background. Press Stop Music to stop it.")
    return True


def start_music(settings):
    """Start background music only, no welcome video.

    Stops any music already playing first, so starting it twice
    does not play two copies at once. VLC starts minimized, so
    your wallpaper and desktop stay in front.
    Returns False if VLC or the music folder is missing.
    """
    vlc = find_vlc()
    if not vlc:
        print("VLC is not installed. Install it free from videolan.org.")
        return False
    music = Path(settings["music_folder"])
    if not music.exists() or not any(music.iterdir()):
        print(f"Music folder is empty or missing: {music}")
        return False
    stop_music()
    music_args = [vlc, "--loop", "--qt-start-minimized", str(music)]
    if platform.system() == "Windows":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 6  # minimized
        subprocess.Popen(music_args, startupinfo=startupinfo)
    else:
        subprocess.Popen(music_args)
    return True


# --- Start on login -------------------------------------------------
# Windows: a Run key in the registry for the current user only.
# Mac: a LaunchAgent file that runs this app with --run on login.
# Both only affect the person who pressed the button.

def install_startup():
    system = platform.system()
    app_path = Path(__file__).resolve()
    if system == "Windows":
        import winreg
        python = sys.executable
        if python.endswith("python.exe"):
            pythonw = python[:-4] + "w.exe"
        else:
            pythonw = python
        command = f'"{pythonw}" "{app_path}" --run'
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE,
        )
        winreg.SetValueEx(key, "JarvisStartup", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        return True
    if system == "Darwin":
        plist_dir = Path.home() / "Library" / "LaunchAgents"
        plist_dir.mkdir(parents=True, exist_ok=True)
        plist = plist_dir / "com.jarvisstartup.plist"
        plist.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
            '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
            "<plist version=\"1.0\">\n<dict>\n"
            "  <key>Label</key><string>com.jarvisstartup</string>\n"
            "  <key>ProgramArguments</key>\n  <array>\n"
            f"    <string>{sys.executable}</string>\n"
            f"    <string>{app_path}</string>\n"
            "    <string>--run</string>\n  </array>\n"
            "  <key>RunAtLoad</key><true/>\n"
            "</dict>\n</plist>\n",
            encoding="utf-8",
        )
        subprocess.run(["launchctl", "load", str(plist)])
        return True
    return False


def remove_startup():
    system = platform.system()
    if system == "Windows":
        import winreg
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE,
            )
            winreg.DeleteValue(key, "JarvisStartup")
            winreg.CloseKey(key)
        except FileNotFoundError:
            pass
        return True
    if system == "Darwin":
        plist = Path.home() / "Library" / "LaunchAgents" / "com.jarvisstartup.plist"
        subprocess.run(["launchctl", "unload", str(plist)])
        if plist.exists():
            plist.unlink()
        return True
    return False


def stop_music():
    """Stop the background music by closing VLC.

    The music runs as its own VLC process, so closing the app
    window does not stop it. This is the button that stops it.
    """
    system = platform.system()
    if system == "Windows":
        subprocess.run(
            ["taskkill", "/IM", "vlc.exe", "/F"],
            capture_output=True,
        )
    elif system == "Darwin":
        subprocess.run(["pkill", "vlc"], capture_output=True)
    else:
        subprocess.run(["pkill", "vlc"], capture_output=True)


# --- Settings window ------------------------------------------------

def run_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox

    settings = load_settings()
    root = tk.Tk()
    root.title("Jarvis Startup")
    root.geometry("520x540")

    tk.Label(root, text="Welcome video").pack(anchor="w", padx=12, pady=(12, 0))
    video_var = tk.StringVar(value=settings["welcome_video"])
    tk.Entry(root, textvariable=video_var, width=60).pack(padx=12, fill="x")
    tk.Button(
        root, text="Choose video",
        command=lambda: video_var.set(
            filedialog.askopenfilename(
                filetypes=[("Video", "*.mp4 *.mov *.mkv"), ("All files", "*.*")]
            ) or video_var.get()
        ),
    ).pack(anchor="w", padx=12, pady=4)

    tk.Label(root, text="Music folder").pack(anchor="w", padx=12, pady=(8, 0))
    music_var = tk.StringVar(value=settings["music_folder"])
    tk.Entry(root, textvariable=music_var, width=60).pack(padx=12, fill="x")
    tk.Button(
        root, text="Choose music folder",
        command=lambda: music_var.set(
            filedialog.askdirectory() or music_var.get()
        ),
    ).pack(anchor="w", padx=12, pady=4)

    tk.Label(root, text="Welcome video length (seconds)").pack(
        anchor="w", padx=12, pady=(8, 0)
    )
    seconds_var = tk.StringVar(value=str(settings["welcome_seconds"]))
    tk.Entry(root, textvariable=seconds_var, width=10).pack(anchor="w", padx=12)

    status = tk.StringVar(value="Pick your video and music, then Save.")
    tk.Label(root, textvariable=status, wraplength=480).pack(padx=12, pady=12)

    def current_settings():
        try:
            seconds = int(seconds_var.get())
        except Exception:
            seconds = 62
        return {
            "welcome_video": video_var.get(),
            "music_folder": music_var.get(),
            "welcome_seconds": seconds,
        }

    def do_save():
        save_settings(current_settings())
        status.set("Saved. Your choices are in settings.json.")

    def do_run():
        do_save()
        status.set("Playing welcome video, then music. Close VLC to stop music.")
        root.update()
        if not run_startup_sequence(current_settings()):
            messagebox.showerror(
                "Jarvis Startup",
                "Could not start. Check VLC is installed, the video exists, "
                "and the music folder has songs in it.",
            )
            status.set("Could not start. Check VLC, video, and music folder.")

    def do_install():
        try:
            install_startup()
            status.set("Installed to run on login.")
        except Exception as exc:
            messagebox.showerror("Jarvis Startup", str(exc))

    def do_remove():
        try:
            remove_startup()
            status.set("Removed from login.")
        except Exception as exc:
            messagebox.showerror("Jarvis Startup", str(exc))

    def do_start_music():
        do_save()
        if start_music(current_settings()):
            status.set("Music started in the background. Press Stop Music to stop it.")
        else:
            status.set("Could not start music. Check VLC and the music folder.")

    def do_stop_music():
        stop_music()
        status.set("Music stopped.")

    tk.Button(root, text="Save", command=do_save).pack(pady=2)
    tk.Button(root, text="Start", command=do_run).pack(pady=2)
    tk.Button(root, text="Run Startup Sequence (test)", command=do_run).pack(pady=2)
    tk.Button(root, text="Start Music", command=do_start_music).pack(pady=2)
    tk.Button(root, text="Stop Music", command=do_stop_music).pack(pady=2)
    tk.Button(root, text="Install to Startup (run on login)", command=do_install).pack(pady=2)
    tk.Button(root, text="Remove from Startup", command=do_remove).pack(pady=2)
    root.mainloop()


if __name__ == "__main__":
    if "--run" in sys.argv:
        # Login mode: no window, just video, then music.
        run_startup_sequence(load_settings())
    else:
        run_gui()
