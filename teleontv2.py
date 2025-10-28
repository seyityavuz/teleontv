import subprocess
import os

URL = "https://kick.com/teleontv"
OUTPUT_PATH = "linkler/teleontvlinki.m3u"
COMMIT_MESSAGE = "Güncel teleontv linki eklendi"

# Klasör yoksa oluştur
os.makedirs("linkler", exist_ok=True)

def update_m3u():
    result = subprocess.run(
        ["streamlink", "--stream-url", URL, "best"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        stream_url = result.stdout.strip()
        m3u_content = f"#EXTM3U\n#EXTINF:-1,teleontv\n{stream_url}\n"
        with open(OUTPUT_PATH, "w") as f:
            f.write(m3u_content)
        print("Güncellendi:", stream_url)
        return True
    else:
        print("Streamlink hatası:", result.stderr.strip())
        return False

def git_commit():
    subprocess.run(["git", "config", "--global", "user.name", "github-actions"])
    subprocess.run(["git", "config", "--global", "user.email", "github-actions@github.com"])
    subprocess.run(["git", "add", OUTPUT_PATH])
    subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE])
    subprocess.run(["git", "push"])

if update_m3u():
    git_commit()
