# -*- coding: utf-8 -*-
__author__ = 'Vit'

import requests
import requests.exceptions

import yt_dlp
from pprint import pprint


def get_all_video_urls(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        "allow_unplayable_formats": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # pprint(info)

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


def load(url, fname, cookies=None, headers=None, proxies=None, timeout=5, allow_redirects=True, encoding=None):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

    print('Loading', url, 'to', fname)
    try:
        if not headers:
            headers = dict()
        headers['user-agent'] = USER_AGENT

        # print('START')
        response = requests.get(url, cookies=cookies, headers=headers, proxies=proxies, allow_redirects=allow_redirects,
                                timeout=timeout)
        # print('END')
        response.raise_for_status()
        if encoding:
            print("Encoding:", encoding)
            with open(fname, "w", encoding=encoding) as file:
                file.write(response.text)
        else:
            with open(fname, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=128):
                    fd.write(chunk)

    except requests.exceptions.HTTPError as err:
        print('HTTP error: {0}'.format(err.response.status_code))
        # return response

    except requests.exceptions.ConnectTimeout:
        print('Connection timeout')

    except requests.exceptions.ReadTimeout:
        print('Read timeout')

    except requests.exceptions.ConnectionError:
        print('Connection error')

    except:
        print('Unknown error in loader')
    else:
        print('loaded ok!')
        return response


if __name__ == "__main__":
    import pyperclip

    # Получить текст из буфера обмена
    clipboard_text = pyperclip.paste()
    print("Текст из буфера обмена:", clipboard_text)

    if clipboard_text.startswith('https://'):
        url = clipboard_text
    else:
        url = ""

    fname = 'out/1.html'

    r = load(url, fname, encoding="utf-8")

    if r:
        print(r.status_code)
        print("History:", r.history)

        print('=======response========')
        for item in r.headers:
            print(item, ':', r.headers[item])

        print('========request========')
        for item in r.request.headers:
            print(item, ':', r.request.headers[item])
        print('=======================')

    print('========yt_dlp=========')
    get_all_video_urls(url)
