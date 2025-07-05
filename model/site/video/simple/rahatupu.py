# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class RahatupuSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('rahatupu.net/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/rahatupu.png',
                              # menu_items=menu_items,
                              url=URL("https://rahatupu.net/?filter=latest*"))

    def get_shrink_name(self):
        return 'RT'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'videos-list'})
        # pretty(contents)
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('article', {'class': 'thumb-block'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)
                    img = thumbnail.find('img')
                    thumb_url = URL(img.attrs.get('data-src'), base_url=url,redirect=True)
                    label = img.attrs.get('alt')

                    # title = thumbnail.find('div', {'class': 'item_title'})
                    # label = '' if title is None else collect_string(title)

                    duration = thumbnail.find('span', {'class': 'duration'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('div', {'class': 'hd-text-icon'})
                    hd = '' if hd_tag is None else collect_string(hd_tag)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                except AttributeError as e:
                    print(e)
                    pass

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'pagination'})


    def parse_video(self, soup: BeautifulSoup, url: URL):
        # pretty(soup)
        video = soup.find('div', {'class': 'video-player'})
        if video:
            # pretty(video)
            content=soup.find('meta', {'itemprop': 'contentURL'})
            # pretty(content)
            if content:
                self.add_video('default', URL(content.attrs.get('content'),referer=url))

            # self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for container in _iter(soup.find_all('div', {'id':'video-about'})):
            if container:
                # pretty(container)
                for item in _iter(container.find_all('a', href=lambda x: '/sites/' in str(x))):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    self.add_tag(collect_string(item), URL(href, base_url=url), style=dict(color='blue'))

                for item in _iter(container.find_all('a', href=lambda x: '/models/' in str(x))):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    self.add_tag(collect_string(item), URL(href, base_url=url), style=dict(color='red'))

                for item in _iter(container.find_all('a', href=lambda x: '/category/' in str(x))):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    self.add_tag(collect_string(item), URL(href, base_url=url))

                for item in _iter(container.find_all('a', href=lambda x: '/tag/' in str(x))):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    self.add_tag(collect_string(item), URL(href, base_url=url), style=dict(color='gray'))

if __name__ == "__main__":
    pass
