from PyQt6.QtWidgets import QWidget

import requests
import requests.exceptions

from data_format.url import URL
from common.util import _iter, quotes, psp, sp, collect_string, pretty
from common.setting import Setting

from view_qt6.widgets.hls_async_loader import HlsLoader

class M3u8():
    def __init__(self):
        self.urls = list()
        self.captions = list()
        self.positions= list()

    def clear(self):
        self.urls = list()
        self.captions= list()
        self.positions = list()
        self.stream=False
        self.playlist=False

    def open(self, text:str, base_url:URL):
        self.urls = list()
        lines=text.split('\n')
        # print('==')
        for line in lines:
            if line.startswith('#EXT-X-STREAM-INF'):
                self.parce_playlist(lines,base_url)
                break

            if line.startswith('#EXT-X-MEDIA-SEQUENCE'):
                self.parce_stream(lines,base_url)
                break
        # print('==')

    def parce_playlist(self, lines:list, base_url:URL):
        # print('parce_playlist')
        self.playlist=True
        skip=False
        for i in range(len(lines)):
            if skip:
                skip=False
                continue
            # print(i, lines[i])
            if lines[i].startswith('#EXT-X-STREAM-INF'):
                caption=quotes(lines[i],'RESOLUTION=',',')
                url = URL(lines[i+1].strip(), base_url=base_url, m3u8=True)
                self.urls.append(url)
                self.captions.append(caption)
                # print(caption, url)
                skip=True

        for caption, url in zip(self.captions, self.urls):
            # print(caption, url)
            pass


    def parce_stream(self, lines:list, base_url:URL):
        # print('parce_stream')
        self.stream=True
        skip=False
        current_position=0
        for i in range(len(lines)):
            if skip:
                skip=False
                continue
            # print(i, lines[i])
            if lines[i].startswith('#EXTINF'):
                pos=quotes(lines[i],'EXTINF:',',')
                url = URL(lines[i+1].strip(), base_url=base_url, m3u8=True)
                self.urls.append(url)
                self.positions.append(current_position)
                current_position=current_position+int(float(pos)*1000)
                # print(pos, url)
                skip=True

        for position, url in zip(self.positions, self.urls):
            # print(position, url)
            pass

class Stream():
    def __init__(self, url:URL):
        self.url = url

    def get(self) -> str:
        url_get = self.url.get()
        if self.url.redirect:
            r=requests.get(self.url.get(), allow_redirects=False)
            url_get= r.headers.get('Location', self.url.get())
            print('Player redirect to', url_get)
        return url_get

# class HlsStream(Stream):
#     def __init__(self, url:URL):
#         super().__init__(url)
#
#     def get(self, start=0) -> str:
#         url_get = self.url.get()
#         print('Starting stream', url_get)
#         r = requests.get(self.url.get())
#         # print(r.text)
#         self.m3u = M3u8()
#         self.m3u.open(r.text, base_url=self.url)
#
#
#
#         return self.m3u.get(start)
#
#     def play(self, start=0):
#         pass
#
#     def get_next(self):
#         return self.m3u.get_next()

class Playlist():
    def __init__(self, player_widget:QWidget, allow_hls=False):
        self.player = player_widget
        self.allow_hls = allow_hls
        self.clear()

    # def update(self):
    #     print('..update')

    def clear(self):
        # self.urls=list()
        self.streams=list()
        self.captions=list()
        self.player.init_quality_menu()
        self.current_stream=None

    def add_resolution_url(self, caption:str, url:URL)->None:
        if self.allow_hls and url.m3u8:
            # print('Adding m3u8')
            try:
                r=requests.get(url.get())
                # print(r.text)
                m3u=M3u8()
                m3u.open(r.text, base_url=url)
                # stream = HlsStream()
                if m3u.playlist:
                    for caption, url in zip(m3u.captions, m3u.urls):
                        # print('   ',caption, url)
                        stream=Stream(url)
                        self.streams.append(stream)
                        self.captions.append(caption)
                        self.player.add_quality_menu_item(caption, len(self.streams) - 1)
                    return
            except requests.RequestException as e:
                print('Playlist error:', e)
        stream=Stream(url)
        self.streams.append(stream)
        self.captions.append(caption)
        # print('   ', caption, url)
        self.player.add_quality_menu_item(caption, len(self.streams)-1)

    def set_resolution(self, n)->None:

        # print('set_res',n)
        if type(n) is not int:
            # print('No resolution selected')
            n=0
            max=0
            for i,caption in enumerate(self.captions):
                # print(i, caption)
                digits = ''
                for char in caption.strip():
                    if char.isdigit():
                        digits += char
                    else:
                        break

                if digits:
                    number = int(digits)
                    if number > max:
                        max=number
                        n=i
                    # print(number)

        print('Current', self.captions[n], self.streams[n].url)

        self._set_stream(self.streams[n])
        # print(self.captions)

    def get_stream(self, stream_no:int)->str:
        # print('get_stream')
        self.current_stream=self.streams[stream_no]
        return self.current_stream.get()


    def _set_stream(self, stream:Stream):
        # print('_set_stream')
        self.current_stream=stream
        self.player.set_url(stream.get())

    # def next_part(self)->str:
    #     return self.current_stream.get_next()

if __name__ == '__main__':
    pass
