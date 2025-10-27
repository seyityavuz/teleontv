import subprocess
import os

KICK_URL = "https://kick.com/teleontv"
OUTPUT_FILE = "playlist.m3u8"

def get_stream_url(kick_url):
    result = subprocess.run(
        ["streamlink", "--stream-url", kick_url, "best"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        print("Streamlink hatası:", result.stderr.strip())
        return None

def write_m3u8(stream_url, output_path):
    m3u_content = (
        "#EXTM3U\n"
        "#EXTINF:-1,TeleonTV\n"
        f"{stream_url}\n"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Gerçek M3U8 playlist oluşturuldu:", output_path)

def main():
    stream_url = get_stream_url(KICK_URL)
    if stream_url:
        write_m3u8(stream_url, OUTPUT_FILE)

if __name__ == "__main__":
    main()
