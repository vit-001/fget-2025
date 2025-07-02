import yt_dlp
from pprint import pprint

def get_all_video_urls(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            pprint(info)

            if not info.get('formats'):
                print("Нет доступных форматов или сайт заблокирован.")
                return

            print(f"Доступные форматы для: {info['title']}\n")
            for fmt in info['formats']:
                print(
                    f"ID: {fmt['format_id']} | "
                    f"Тип: {fmt['ext']} | "
                    f"Качество: {fmt.get('resolution', '?')} | "
                    f"URL: {fmt['url']}"
                )
    except Exception as e:
        pass


if __name__ == "__main__":
    get_all_video_urls("https://vps404.strip2.co/video/8811355/?Li=2134311049&Lii=8811355&Lt=29&Sn=9&tid=96076390")
