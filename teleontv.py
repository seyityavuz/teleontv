import subprocess
import os

URL = "https://kick.com/teleontv"
OUTPUT_PATH = "playlist.m3u8"

# Klasör oluşturmak istersen:
# os.makedirs("linkler", exist_ok=True)

def update_m3u():
    result = subprocess.run(
        ["streamlink", "--stream-url", URL, "best"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        stream_url = result.stdout.strip()
        m3u_content = (
            "#EXTM3U\n"
            '#EXTINF:-1 tvg-id="" tvg-name="TeleonTV" tvg-logo="" group-title="Kick",TeleonTV\n'
            f"{stream_url}\n"
        )
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Güncellendi:", stream_url)
    else:
        print("Streamlink hatası:", result.stderr.strip())

update_m3u()
