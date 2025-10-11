from urllib.parse import urlsplit, parse_qs, urlencode


def modify_and_reconstruct_url(url, modifications=None):
    modifications = modifications or {}

    # Разбираем URL
    parsed = urlsplit(url)
    query_dict = parse_qs(parsed.query)

    # Применяем изменения к параметрам
    for key, value in modifications.items():
        query_dict[key] = [value]

    # Собираем новую строку запроса
    new_query = urlencode(query_dict, doseq=True)
    print(new_query)

    # Собираем URL
    reconstructed_url = (
            f"{parsed.scheme}://{parsed.netloc}{parsed.path}" +
            (f"?{new_query}" if new_query else "") +
            (f"#{parsed.fragment}" if parsed.fragment else "")
    )
    return reconstructed_url


# Пример использования
url = "https://example.com/search?q=python&lang=en"
new_url = modify_and_reconstruct_url(url, {"page": "2", "lang": "ru"})
print(new_url)  # https://example.com/search?q=python&lang=ru&page=2