import subprocess
import os

# Path to your input file with URLs
url_file = "video_urls.txt"

# Output folder for audio files
output_folder = "downloaded_audios"
os.makedirs(output_folder, exist_ok=True)

# Read URLs from file
with open(url_file, "r") as f:
    urls = [line.strip() for line in f if line.strip()]

# Download audio for each URL
for url in urls:
    print(f"Downloading audio from: {url}")
    command = [
        "yt-dlp",
        "-x",  # extract audio
        "--audio-format", "mp3",  # convert to mp3
        "-o", os.path.join(output_folder, "%(title)s.mp3"),
        url
    ]
    print(command)
    subprocess.run(command)

print("\n✅ All downloads complete!")
