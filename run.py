import os
import yt_dlp

playlist_url = "https://www.youtube.com/playlist?list=PLnlL14v8ZEzdlPqvRFxbAgOAOFoOnbLMH"

ydl_opts = {
    'extract_flat': True,  # Don't download, just extract info
    'quiet': True,
}

urls:list = []

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    playlist_dict = ydl.extract_info(playlist_url, download=False)

    print(f"Playlist Title: {playlist_dict.get('title')}")
    print(f"Total videos: {len(playlist_dict.get('entries', []))}\n")

    for video in playlist_dict.get('entries', []):
        print(f"https://www.youtube.com/watch?v={video['id']}")
        urls.append(f"https://www.youtube.com/watch?v={video['id']}")

folder_path = "downloaded_audios"
os.makedirs(folder_path, exist_ok=True)

def remove_topic_suffix(text: str) -> str:
    """Remove ' - Topic' from the end of the string if present."""
    return text.replace(" - Topic", "")

# yt_dlp options
ydl_opts = {
    'format': 'bestaudio/best',  # best audio quality
    'extractaudio': True,        # extract audio only
    'audioformat': 'mp3',        # convert to mp3
    'outtmpl': os.path.join(folder_path, '%(title)s-%(uploader)s.%(ext)s'),
    'quiet': False,              # show progress
}

# Download audio files
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for url in urls:
        print(f"🎵 Downloading audio from: {url}")
        ydl.download([url])

for filename in os.listdir(folder_path):
    if filename.lower().endswith(".mp4"):
        old_path = os.path.join(folder_path, filename)
        new_filename = os.path.splitext(filename)[0] + ".mp3"
        new_path = os.path.join(folder_path, new_filename)
        
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")
    if filename.lower().endswith(".webm"):
        old_path = os.path.join(folder_path, filename)
        new_filename = os.path.splitext(filename)[0] + ".mp3"
        new_path = os.path.join(folder_path, new_filename)
        
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")

for filename in os.listdir(folder_path):
    old_path = os.path.join(folder_path, filename)
    new_filename = remove_topic_suffix(filename)
    new_path = os.path.join(folder_path, new_filename)
    os.rename(old_path, new_path)
    print(f"Removed `Topic`: {filename} → {new_filename}")

print("\n✅ All downloads complete!")
