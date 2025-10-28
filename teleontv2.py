import subprocess
import os
import sys

URL = "https://kick.com/teleontv"
OUTPUT_PATH = "playlist.m3u8"
COMMIT_MESSAGE = "playlist.m3u8 güncellendi: " + subprocess.getoutput("date -u")

def log(msg):
    print(f"[LOG] {msg}")

def run_cmd(cmd, check=False):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        log(f"[HATA] Komut başarısız: {' '.join(cmd)}")
        log(result.stderr.strip())
        sys.exit(result.returncode)
    return result

def update_m3u8():
    os.makedirs(os.path.dirname(OUTPUT_PATH) or ".", exist_ok=True)
    result = run_cmd(["streamlink", "--stream-url", URL, "best"], check=True)
    stream_url = result.stdout.strip()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(stream_url + "\n")
    log(f"[BAŞARILI] Güncellendi: {stream_url}")

def has_changes():
    result = subprocess.run(["git", "diff", "--quiet", OUTPUT_PATH])
    return result.returncode != 0  # 0 = değişiklik yok, 1 = değişiklik var

def git_commit():
    run_cmd(["git", "config", "--global", "user.name", "github-actions"])
    run_cmd(["git", "config", "--global", "user.email", "github-actions@github.com"])
    run_cmd(["git", "pull", "--rebase"])
    if has_changes():
        run_cmd(["git", "add", OUTPUT_PATH])
        run_cmd(["git", "commit", "-m", COMMIT_MESSAGE])
        run_cmd(["git", "push"])
        log("[BAŞARILI] Git commit ve push tamamlandı.")
    else:
        log("[BİLGİ] Dosyada değişiklik yok, commit atlanıyor.")

def main():
    try:
        update_m3u8()
        git_commit()
        sys.exit(0)
    except Exception as e:
        log(f"[HATA] Beklenmeyen hata: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
