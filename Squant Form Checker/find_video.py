"""
╔══════════════════════════════════════════════════════════════╗
║       AI GYM REP COUNTER & FORM COACH                       ║
║       VIDEO FINDER / DOWNLOADER                              ║
║       Dev/Creator: tubakhxn                                  ║
║       GitHub: https://github.com/tubakhxn                   ║
╚══════════════════════════════════════════════════════════════╝

Run this FIRST to download the best workout video for the AI system.
It tries yt-dlp (YouTube), then falls back to a free sample video.
"""

import subprocess
import sys
import os
import urllib.request
from pathlib import Path

def print_banner():
    print("\033[95m")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║       AI GYM REP COUNTER — VIDEO FINDER                     ║")
    print("║       Dev/Creator: tubakhxn                                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("\033[0m")

def install_ytdlp():
    try:
        import yt_dlp
        return True
    except ImportError:
        print("\033[93m[*] Installing yt-dlp...\033[0m")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "-q"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True

# ─── BEST VIDEOS (ranked by quality + visibility for AI pose detection) ──────
# These are the best public workout videos for pose/rep detection demos
CANDIDATE_VIDEOS = [
    # Squat tutorial — clear side view, perfect for angle detection
    ("https://www.youtube.com/watch?v=ultWZbUMPL8", "squat_workout.mp4"),
    # Push-up form — front/side angle, great for elbow tracking
    ("https://www.youtube.com/watch?v=IODxDxX7oi4", "pushup_workout.mp4"),
    # Full body workout — multiple exercises, more complex demo
    ("https://www.youtube.com/watch?v=UBMk30rjy0o", "fullbody_workout.mp4"),
]

# Royalty-free fallback — Pexels public domain workout clip
FALLBACK_URL = "https://www.pexels.com/download/video/3996838/"
FALLBACK_FILE = "gym_sample.mp4"

def try_youtube_download(url, filename):
    try:
        import yt_dlp
        ydl_opts = {
            'outtmpl': filename,
            'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\033[93m[*] Trying: {url}\033[0m")
            ydl.download([url])
        if os.path.exists(filename) and os.path.getsize(filename) > 100000:
            print(f"\033[92m[✓] Downloaded: {filename}\033[0m")
            return True
    except Exception as e:
        print(f"\033[91m[!] Failed: {e}\033[0m")
    return False

def download_fallback():
    """Download a royalty-free gym video from public sources."""
    # Try multiple free sources
    sources = [
        # Pixabay free workout video (no auth needed)
        ("https://cdn.pixabay.com/video/2016/12/30/6872-197634410_large.mp4", "gym_sample.mp4"),
        # Coverr free fitness video
        ("https://d2lcr29g0bmwz9.cloudfront.net/videos/woman-working-out_v3.mp4", "gym_sample.mp4"),
    ]
    for url, fname in sources:
        try:
            print(f"\033[93m[*] Downloading fallback from: {url[:60]}...\033[0m")
            urllib.request.urlretrieve(url, fname,
                reporthook=lambda b,bs,ts: print(
                    f"\r  {min(100,int(b*bs/ts*100)) if ts>0 else 0}%", end="", flush=True))
            print()
            if os.path.exists(fname) and os.path.getsize(fname) > 100000:
                print(f"\033[92m[✓] Fallback downloaded: {fname}\033[0m")
                return fname
        except Exception as e:
            print(f"\033[91m[!] Fallback failed: {e}\033[0m")
    return None

def main():
    print_banner()
    print("\033[94m[INFO] This script finds the best gym/workout video for the AI Rep Counter.\033[0m")
    print("\033[94m[INFO] Trying YouTube (yt-dlp) first, then free fallback sources.\033[0m\n")

    install_ytdlp()

    # Try YouTube candidates in order
    for url, fname in CANDIDATE_VIDEOS:
        if try_youtube_download(url, fname):
            print(f"\n\033[92m[✓] SUCCESS! Video ready: {fname}\033[0m")
            print(f"\033[92m[→] Now run: python main.py {fname}\033[0m")
            return

    # Fallback
    print("\033[93m[*] YouTube unavailable, trying royalty-free sources...\033[0m")
    result = download_fallback()

    if result:
        print(f"\n\033[92m[✓] SUCCESS! Video ready: {result}\033[0m")
        print(f"\033[92m[→] Now run: python main.py {result}\033[0m")
    else:
        print("\n\033[91m[!] Auto-download failed. Please manually place a workout video as 'gym_video.mp4'\033[0m")
        print("\033[93m[TIP] Best sources:\033[0m")
        print("  • https://www.pexels.com/search/videos/workout/")
        print("  • https://pixabay.com/videos/search/exercise/")
        print("  • https://coverr.co/search?q=workout")
        print("\033[92m[→] Then run: python main.py gym_video.mp4\033[0m")

if __name__ == "__main__":
    main()
