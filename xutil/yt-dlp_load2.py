# -*- coding: utf-8 -*-
__author__ = 'Vit'

import os
import pyperclip
from urllib.parse import urlparse
import yt_dlp
from curl_cffi import requests
from curl_cffi.requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError
from yt_dlp.networking.impersonate import ImpersonateTarget


def get_all_video_urls(url, browser_for_cookies=None):
    """
    Извлекает все доступные форматы и прямые ссылки на видео с обходом 403.

    :param url: Ссылка на страницу с видео
    :param browser_for_cookies: Название браузера для импорта кук, например 'chrome', 'edge', 'firefox' (по умолчанию None)
    """
    # Формируем корректный Origin (например, https://example.com) из переданного URL
    parsed_url = urlparse(url)
    origin = f"{parsed_url.scheme}://{parsed_url.netloc}"

    ydl_opts = {
        'quiet': False,  # Показываем логи, чтобы видеть работу impersonate и причину возможных ошибок
        'no_warnings': False,
        'allow_unplayable_formats': True,

        # Имитация TLS-отпечатка браузера через curl_cffi
        'impersonate': ImpersonateTarget('chrome'),

        # Обязательные заголовки для обхода базовой защиты от хотлинкинга (403)
        'http_headers': {
            'Referer': url,
            'Origin': origin,
        },
    }

    # Если передан браузер, подключаем его куки (помогает против Cloudflare и авторизации)
    if browser_for_cookies:
        ydl_opts['cookiesfrombrowser'] = (browser_for_cookies,)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if not info:
                print("Не удалось получить информацию о странице.")
                return

            formats = info.get('formats')
            if not formats:
                print("Нет доступных форматов или сайт заблокирован.")
                return

            print(f"\nДоступные форматы для: {info.get('title', 'Без названия')}\n")
            for fmt in formats:
                fmt_id = fmt.get('format_id', '?')
                ext = fmt.get('ext', '?')
                resolution = fmt.get('resolution') or f"{fmt.get('width', '?')}x{fmt.get('height', '?')}"
                video_url = fmt.get('url', 'Нет прямой ссылки')

                print(
                    f"ID: {fmt_id} | "
                    f"Тип: {ext} | "
                    f"Качество: {resolution} | "
                    f"URL: {video_url}"
                )

    except yt_dlp.utils.DownloadError as e:
        print(f"Ошибка загрузки yt-dlp: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка в get_all_video_urls: {e}")


import os
from pathlib import Path
from urllib.parse import urlparse
import yt_dlp
from yt_dlp.networking.impersonate import ImpersonateTarget


def get_all_video_urls_from_file(local_html_path, original_url):
    """
    Скармливает yt-dlp уже скачанный локальный HTML-файл, чтобы избежать 403 при повторном запросе.

    :param local_html_path: Путь к сохраненному HTML-файлу (например, 'out/1.html')
    :param original_url: Исходный URL страницы (нужен для заголовка Referer)
    """
    abs_path = os.path.abspath(local_html_path)
    if not os.path.exists(abs_path):
        print(f"Файл {abs_path} не найден.")
        return

    # Формируем корректный URI вида file:///C:/... или file:///home/...
    file_uri = Path(abs_path).as_uri()

    parsed_url = urlparse(original_url)
    origin = f"{parsed_url.scheme}://{parsed_url.netloc}"

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'allow_unplayable_formats': False,

        # Обязательно разрешаем yt-dlp открывать локальные файлы через file://
        'enable_file_urls': True,

        # Оставляем impersonate и Referer на случай, если внутри HTML лежит .m3u8 плейлист,
        # который yt-dlp должен будет подгрузить по сети для чтения списка разрешений
        'impersonate': ImpersonateTarget('chrome'),
        'http_headers': {
            'Referer': original_url,
            'Origin': origin,
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Передаем file_uri вместо сетевого URL
            info = ydl.extract_info(file_uri, download=False)

            if not info or not info.get('formats'):
                print("Нет доступных форматов в локальном файле.")
                return

            print(f"\nДоступные форматы для: {info.get('title', 'Без названия')}\n")
            for fmt in info['formats']:
                fmt_id = fmt.get('format_id', '?')
                ext = fmt.get('ext', '?')
                resolution = fmt.get('resolution') or f"{fmt.get('width', '?')}x{fmt.get('height', '?')}"
                video_url = fmt.get('url', 'Нет прямой ссылки')

                print(
                    f"ID: {fmt_id} | "
                    f"Тип: {ext} | "
                    f"Качество: {resolution} | "
                    f"URL: {video_url}"
                )

    except yt_dlp.utils.DownloadError as e:
        print(f"Ошибка yt-dlp при разборе файла: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


def load(url, fname, cookies=None, headers=None, proxies=None, timeout=10, allow_redirects=True, encoding=None,
         impersonate="chrome"):
    print('Loading', url, 'to', fname)
    try:
        # Создаем папку, если её нет (например, 'out')
        folder = os.path.dirname(fname)
        if folder:
            os.makedirs(folder, exist_ok=True)

        # Важно: при использовании impersonate лучше НЕ задавать User-Agent вручную,
        # так как curl_cffi сам подставит правильный UA под выбранный TLS-отпечаток.
        response = requests.get(
            url,
            cookies=cookies,
            headers=headers,
            proxies=proxies,
            allow_redirects=allow_redirects,
            timeout=timeout,
            impersonate=impersonate
        )

        response.raise_for_status()

        if encoding:
            print("Encoding:", encoding)
            with open(fname, "w", encoding=encoding) as file:
                file.write(response.text)
        else:
            with open(fname, 'wb') as fd:
                # В curl_cffi используется iter_content(chunk_size=...) или response.content
                for chunk in response.iter_content(chunk_size=8192):
                    fd.write(chunk)

    except HTTPError as err:
        status = err.response.status_code if err.response else 'Unknown'
        print(f'HTTP error: {status}')
        return err.response

    except Timeout:
        print('Timeout error (Connect or Read)')

    except ConnectionError:
        print('Connection error')

    except RequestException as e:
        print(f'Request error: {e}')

    except Exception as e:
        print(f'Unknown error in loader: {e}')
    else:
        print('loaded ok!')
        return response


if __name__ == "__main__":
    clipboard_text = pyperclip.paste().strip()
    print("Текст из буфера обмена:", clipboard_text)

    if not clipboard_text.startswith(('http://', 'https://')):
        print("Ошибка: в буфере обмена нет корректной ссылки.")
        exit(1)

    url = clipboard_text
    fname = 'out/1.html'

    # impersonate="chrome" автоматически выберет актуальную версию Chrome, зашитую в curl_cffi
    r = load(url, fname, encoding="utf-8", impersonate="chrome")

    if r is not None:
        print("Status:", r.status_code)
        # В curl_cffi r.history возвращает список редиректов (если были)
        print("History:", r.history)

        print('=======response========')
        for k, v in r.headers.items():
            print(f"{k} : {v}")

        print('========request========')
        # В curl_cffi заголовки запроса доступны через r.request.headers (если объект request сформирован)
        if hasattr(r, 'request') and r.request and r.request.headers:
            for k, v in r.request.headers.items():
                print(f"{k} : {v}")
        else:
            print("Заголовки запроса сформированы автоматически движком impersonate")
        print('=======================')

    # print('========yt_dlp=========')
    # get_all_video_urls(url)
    print('========yt_dlp локально=========')
    get_all_video_urls_from_file(fname, url)
