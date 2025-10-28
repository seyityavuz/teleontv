import subprocess
import os

URL = "https://kick.com/teleontv"
OUTPUT_PATH = "playlist.m3u8"

# Dosya yolu varsa klasörünü oluştur
os.makedirs(os.path.dirname(OUTPUT_PATH) or ".", exist_ok=True)

def update_m3u8():
    result = subprocess.run(
        ["streamlink", "--stream-url", URL, "best"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        stream_url = result.stdout.strip()
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(stream_url + "\n")
        print("Güncellendi:", stream_url)
    else:
        print("Streamlink hatası:", result.stderr.strip())

update_m3u8()
