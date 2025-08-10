import os
import yt_dlp

# Path to your input file with URLs
url_file = "video_urls.txt"

# Output folder for audio files
output_folder = "downloaded_audios"
os.makedirs(output_folder, exist_ok=True)

# Read URLs from file
with open(url_file, "r") as f:
    urls = [line.strip() for line in f if line.strip()]

# yt_dlp options
ydl_opts = {
    'format': 'bestaudio/best',  # best audio quality
    'extractaudio': True,        # extract audio only
    'audioformat': 'mp3',        # convert to mp3
    'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
    'quiet': False,              # show progress
}

# Download audio files
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for url in urls:
        print(f"🎵 Downloading audio from: {url}")
        ydl.download([url])

print("\n✅ All downloads complete!")
