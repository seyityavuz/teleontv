import subprocess
import os
import sys

URL = "https://kick.com/teleontv"
OUTPUT_PATH = "linkler/teleontvlinki.m3u"
COMMIT_MESSAGE = "Güncel teleontv linki eklendi"

def log(msg):
    print(f"[LOG] {msg}")

def run_cmd(cmd, check=False):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        log(f"Hata: {result.stderr.strip()}")
        sys.exit(result.returncode)
    return result

def update_m3u():
    os.makedirs("linkler", exist_ok=True)
    result = run_cmd(["streamlink", "--stream-url", URL, "best"], check=True)
    stream_url = result.stdout.strip()
    m3u_content = f"#EXTM3U\n#EXTINF:-1,teleontv\n{stream_url}\n"
    with open(OUTPUT_PATH, "w") as f:
        f.write(m3u_content)
    log(f"Link güncellendi: {stream_url}")

def has_changes():
    result = subprocess.run(["git", "diff", "--quiet", OUTPUT_PATH])
    return result.returncode != 0  # 0 = no changes, 1 = changes

def git_commit():
    run_cmd(["git", "config", "--global", "user.name", "github-actions"])
    run_cmd(["git", "config", "--global", "user.email", "github-actions@github.com"])
    run_cmd(["git", "add", OUTPUT_PATH])
    run_cmd(["git", "commit", "-m", COMMIT_MESSAGE])
    run_cmd(["git", "push"])
    log("Git commit ve push işlemi tamamlandı.")

def main():
    update_m3u()
    if has_changes():
        git_commit()
    else:
        log("Dosyada değişiklik yok, commit atlanıyor.")

if __name__ == "__main__":
    main()
