import os
import yt_dlp
import logging

# === Logging Setup ===
log_file = "download_log.txt"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()  # also print to console
    ]
)

playlist_url = "https://www.youtube.com/playlist?list=PLnlL14v8ZEzc-MMJ6wLj-Xr7Xx8lKzYRx"

ydl_opts_extract = {
    'extract_flat': True,
    'quiet': True,
}

urls: list = []

with yt_dlp.YoutubeDL(ydl_opts_extract) as ydl:
    playlist_dict = ydl.extract_info(playlist_url, download=False)

    playlist_title = playlist_dict.get('title')
    total_videos = len(playlist_dict.get('entries', []))

    logging.info(f"Playlist Title: {playlist_title}")
    logging.info(f"Total videos: {total_videos}")

    for video in playlist_dict.get('entries', []):
        video_url = f"https://www.youtube.com/watch?v={video['id']}"
        logging.info(f"Extracted URL: {video_url}")
        urls.append(video_url)

folder_path = "downloaded_audios"
os.makedirs(folder_path, exist_ok=True)

def remove_topic_suffix(text: str) -> str:
    """Remove ' - Topic' from the end of the string if present."""
    return text.replace(" - Topic", "")

# yt_dlp options for download
ydl_opts_download = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': os.path.join(folder_path, '%(title)s-%(uploader)s.%(ext)s'),
    'quiet': False,
}

# Download audio files
with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
    for url in urls:
        logging.info(f"🎵 Downloading audio from: {url}")
        try:
            ydl.download([url])
        except Exception as e:
            logging.error(f"Failed to download {url} - {e}")

# Rename downloaded files
for filename in os.listdir(folder_path):
    if filename.lower().endswith((".mp4", ".webm")):
        old_path = os.path.join(folder_path, filename)
        new_filename = os.path.splitext(filename)[0] + ".mp3"
        new_path = os.path.join(folder_path, new_filename)
        os.rename(old_path, new_path)
        logging.info(f"Renamed: {filename} -> {new_filename}")

for filename in os.listdir(folder_path):
    old_path = os.path.join(folder_path, filename)
    new_filename = remove_topic_suffix(filename)
    new_path = os.path.join(folder_path, new_filename)
    os.rename(old_path, new_path)
    logging.info(f"Removed 'Topic': {filename} → {new_filename}")

logging.info("✅ All downloads complete!")
