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
    import pyperclip

    # Получить текст из буфера обмена
    clipboard_text = pyperclip.paste()
    print("Текст из буфера обмена:", clipboard_text)

    if clipboard_text.startswith('https://'):
        get_all_video_urls(clipboard_text)
    else:

        get_all_video_urls("")
