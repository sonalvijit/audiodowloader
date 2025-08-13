import os
import yt_dlp
import logging
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TCOM
from dotenv import load_dotenv

load_dotenv()

playlist_tag = os.getenv("TAG")

# === Logging Setup ===
log_file = "download_log.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

playlist_url = f"https://www.youtube.com/playlist?list={playlist_tag}"

# === Step 1: Extract playlist ===
ydl_opts_extract = {
    'extract_flat': True,
    'quiet': True,
}

urls = []
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

# === Step 2: Prepare folder ===
folder_path = "downloads"
os.makedirs(folder_path, exist_ok=True)

# === Step 3: Clean title ===
def sanitize_title(text: str) -> str:
    """Remove ' - Topic' and strip whitespace."""
    return text.replace(" - Topic", "").strip()

# === Step 4: Metadata tag function ===
def add_metadata(file_path, title, uploader):
    try:
        audio = EasyID3(file_path)
    except Exception:
        audio = EasyID3()
    
    audio["title"] = title
    audio["artist"] = uploader
    audio["albumartist"] = uploader

    # Composer needs a special tag
    audio.save(file_path)
    id3 = ID3(file_path)
    id3.add(TCOM(encoding=3, text=[uploader]))
    id3.save(file_path)

    logging.info(f"🎼 Added metadata → Title: {title}, Artist/Album Artist/Composer: {uploader}")

# === Step 5: Custom logging class ===
class MyLogger:
    def debug(self, msg):
        pass
    def warning(self, msg):
        logging.warning(msg)
    def error(self, msg):
        logging.error(msg)

def progress_hook(d):
    if d['status'] == 'finished':
        logging.info(f"✅ Finished downloading: {d['filename']}")

# === Step 6: Download with metadata ===
ydl_opts_download = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(folder_path, '%(title)s-%(uploader)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'ffmpeg_location': r'C:\ffmpeg\bin',
    'logger': MyLogger(),
    'progress_hooks': [progress_hook]
}

with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
    for url in urls:
        try:
            info = ydl.extract_info(url, download=False)
            title_clean = sanitize_title(info['title'])
            uploader_clean = sanitize_title(info.get('uploader', 'Unknown'))

            # Update info for clean filename
            info['title'] = title_clean
            info['uploader'] = uploader_clean

            # Download
            filename = ydl.prepare_filename(info)
            ydl.process_info(info)

            # Convert extension to .mp3
            mp3_file = os.path.splitext(filename)[0] + ".mp3"

            # Add metadata
            if os.path.exists(mp3_file):
                add_metadata(mp3_file, title_clean, uploader_clean)

        except Exception as e:
            logging.error(f"Failed to download {url} - {e}")

logging.info("🎯 All downloads complete with metadata!")
