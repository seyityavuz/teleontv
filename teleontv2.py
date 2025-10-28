#!/usr/bin/env bash
set -e

URL="https://kick.com/teleontv"
OUTPUT_DIR="linkler"
OUTPUT_FILE="$OUTPUT_DIR/teleontvlinki.m3u"
COMMIT_MESSAGE="M3U güncellendi: $(date -u)"

echo "[LOG] Stream URL alınıyor..."
STREAM_URL=$(streamlink --stream-url "$URL" best | tr -d '\n')

if [[ -z "$STREAM_URL" ]]; then
  echo "[HATA] Streamlink URL döndüremedi."
  exit 1
fi

echo "[LOG] M3U dosyası oluşturuluyor..."
mkdir -p "$OUTPUT_DIR"
echo -e "#EXTM3U\n#EXTINF:-1,teleontv\n$STREAM_URL" > "$OUTPUT_FILE"

echo "[LOG] Git yapılandırması..."
git config --global user.name "github-actions"
git config --global user.email "github-actions@github.com"
git pull --rebase

echo "[LOG] Değişiklik kontrolü..."
if ! git diff --quiet "$OUTPUT_FILE"; then
  git add "$OUTPUT_FILE"
  git commit -m "$COMMIT_MESSAGE"
  git push
  echo "[BAŞARILI] Commit ve push işlemi tamamlandı."
else
  echo "[BİLGİ] Dosyada değişiklik yok, commit atlanıyor."
fi

exit 0
