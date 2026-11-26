# -*- coding: utf-8 -*-
__author__ = 'Vit'

import requests
import requests.exceptions


def load(url, fname, cookies=None, headers=None, proxies=None, timeout=5, allow_redirects=True, encoding=None):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

    print('Loading', url, 'to', fname)
    try:
        if not headers:
            headers = dict()
        headers['user-agent'] = USER_AGENT

        # print('START')
        response = requests.get(url, cookies=cookies, headers=headers, proxies=proxies, allow_redirects=allow_redirects, timeout=timeout)
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

    url1 = 'https://sickjunk.com/'
    url1a = 'https://ru.anysex.com/video/422235/chocolate-hottie-anne-amari-teases-with-her-perfect-ebony-teen-body-solo-4k/'
    url1b = 'https://www.porndr.com/latest-updates/'
    url2 = 'https://v9.cdnde.com/x9/upload_c5a5030d1a22514e694963b288101017/44327/JOPORN_NET_44327_480p.mp4?video=ZGYzMDk5NTU3N2JmYTFjZGMzMTcwZTQyNTI3YjAxMDI=&time=1766992020&ip=104.23.166.9'
    url3 = 'https://i.prostoporno.monster/contents/videos_screenshots/362000/362190/352x198/1.jpg'

    fname1 = 'out/1.html'
    fname1a = 'out/1a.html'
    fname1b = 'out/1b.html'
    fname1c = 'out/1.html'
    fname2 = 'out/1.mp4'
    fname2a = 'out/2.html'
    fname3 = 'out/3.json'
    fname4 = 'out/1.js'
    fname5 = 'out/1.svg'

    coockies = {'PHPSESSID': 'b5452159d9b0465182078eaecf8c7dcf'}

    headers = {'Referer': 'https://www.heavy-r.com/'}

    # r = load(url1a, fname1a, encoding="utf-8")  # ,headers=headers)#, cookies=coockies)
    # r = load(url2, fname1b)#,headers=headers)
    # r=load(url3,fname1b)#, proxies=proxies)
    # r = load(url1a, fname1a, proxies=proxies)
    r = load(url2, fname2)#, headers=headers)#, proxies=proxies)
    # r = load(url1b, fname1b)  # ,headers=headers)#, cookies=coockies)

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

