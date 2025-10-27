import requests
import re
import subprocess

url = "https://kick.com/teleontv"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
html = response.text

m3u8_matches = re.findall(r'https://[^"]+\.m3u8', html)
if m3u8_matches:
    stream_url = m3u8_matches[0]
    print("Yayın bulundu:", stream_url)
    subprocess.run(["vlc", stream_url])
else:
    print("Yayın bağlantısı bulunamadı.")
