# -*- coding: utf-8 -*-
__author__ = 'Vit'
import json

from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class UserspornSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('usersporn.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        view.add_start_button(picture_filename='model/site/resource/usersporn.png',
                              # menu_items=menu_items,
                              url=URL("https://usersporn.com/videocat/new/"))

    def get_shrink_name(self):
        return 'UP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'tiles_block'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class': 'tile'})):
                # pretty(thumbnail)
                try:

                    xref = thumbnail.find('a', href=True)
                    img = thumbnail.find('img')
                    href = URL(xref.attrs['href'], base_url=url)
                    img_url = img.attrs.get('data-s', img.attrs.get('src', ''))
                    thumb_url = URL(img_url, base_url=url)

                    # title = thumbnail.find('div', {'class': 'item_title'})
                    # label = img.attrs.get('alt',  '')

                    title = thumbnail.find('div', {'class': 'tile_descr_2l'})
                    label = '' if title is None else collect_string(title)

                    duration = thumbnail.find('span', {'class': 'fd'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('span', {'class': 'item-quality'})
                    hd = '' if hd_tag is None else collect_string(hd_tag)

                    # psp(img_url)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                except AttributeError as e:
                    # print(e)
                    pass


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('table',{'class':'table__nums'})


    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'video-player-container'})
        if video:
            # pretty(video)
            try:
                sources = video.attrs['data-sources']
                # psp(sources)

                data = json.loads(sources)
                for item in data:
                    self.add_video(str(item['res']), URL(item['link'], redirect=False, referer=''))

                self.set_default_video(-1)

            except AttributeError as e:
                print(e)
                pass


    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for container in _iter(soup.find_all('div', {'class':'content-item3'})):
            if container:
                # pretty(container)
                for item in _iter(container.find_all('a', href=lambda x: '/models/' in str(x))):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    title = item.attrs.get('title', collect_string(item,divider='/'))
                    self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

                for item in _iter(container.find_all('a', href=lambda x: '/channels/' in str(x))):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    title = item.attrs.get('title', collect_string(item,divider='/'))
                    self.add_tag(title, URL(href, base_url=url), style=dict(color='blue'))

                for item in _iter(container.find_all('a', href=lambda x: '/videocat/' in str(x))):
                    pretty(item)
                    href = item.attrs.get('href', '')+'new/'
                    title = collect_string(item)
                    if not '/tag/' in href:
                        self.add_tag(title, URL(href, base_url=url))

                for item in _iter(container.find_all('a', href=lambda x: '/videocat/' in str(x))):
                    pretty(item)
                    href = item.attrs.get('href', '')+'new/'
                    title = collect_string(item)
                    if '/tag/' in href:
                        self.add_tag(title, URL(href, base_url=url),style=dict(color='gray'))

                for item in _iter(container.find_all('a', href=lambda x:'/tags/' in str(x))):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    title = item.attrs.get('title', collect_string(item))
                    self.add_tag(title, URL(href, base_url=url), style=dict(color='gray'))

if __name__ == "__main__":
    pass
