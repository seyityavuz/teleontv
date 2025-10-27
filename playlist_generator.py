import json

def generate_m3u8(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        channels = json.load(f)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            f.write(f'#EXTINF:-1 group-title="{ch["group"]}",{ch["name"]}\n')
            f.write(f'{ch["url"]}\n')

if __name__ == "__main__":
    generate_m3u8("channels.json", "playlist.m3u8")
    print("playlist.m3u8 başarıyla oluşturuldu.")
