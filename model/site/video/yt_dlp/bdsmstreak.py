# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty, collect_string_to_array

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class BdsmstreakSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('bdsmstreak.com')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/bdsmstreak.png',
                              # menu_items=menu_items,
                              url=URL("https://bdsmstreak.com/newest*"))

    def get_shrink_name(self):
        return 'CS'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        # Main format
        contents = soup.find('div', {'class':'grid'})
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('a', {'class': 'block'})):
                try:
                    # pretty(thumbnail)
                    xref = thumbnail
                    href = URL(xref.attrs['href'], base_url=url)

                    img = thumbnail.find('img')
                    img_url = img.attrs.get('src')
                    thumb_url = URL(img_url, base_url=url)
                    label = img.attrs.get('alt')

                    duration = thumbnail.find('span', {'class': 'duration-pill'})
                    dur_time = '' if duration is None else collect_string(duration)
                    #
                    hd_tag = thumbnail.find('img', {'class': 'hd'})
                    hd = 'HD' if hd_tag else ''

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}
                    ])
                except AttributeError as e:
                    print(e)

        # Another format
        # contents = soup.find('div', {'class':'contentIndex'})
        # if contents:
        #     # psp(contents.prettify())
        #     for thumbnail in _iter(contents.find_all('a', href=True)):
        #         try:
        #             pretty(thumbnail)
        #             xref = thumbnail
        #             href = URL(xref.attrs['href'], base_url=url)
        #
        #             img = thumbnail.find('img',{'class': 'thumbnails'})
        #             img_url = img.attrs.get('src')
        #             thumb_url = URL(img_url, base_url=url)
        #             label_container= thumbnail.find('div', {'class': 'videotitle'})
        #             label = collect_string(label_container)
        #
        #             duration = thumbnail.find('div', {'class': 'duration'})
        #             dur_time = '' if duration is None else collect_string(duration)
        #             #
        #             hd_tag = thumbnail.find('img', {'class': 'hd'})
        #             hd = 'HD' if hd_tag else ''
        #
        #             self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
        #                            labels=[{'text': dur_time, 'align': 'top right'},
        #                                    # {'text': count, 'align': 'top right'},
        #                                    {'text': label, 'align': 'bottom center'},
        #                                    {'text': hd, 'align': 'top left'}
        #             ])
        #         except AttributeError as e:
        #             print(e)


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('nav',{'role':'navigation'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('video', {'id': 'v2-player'})
        if container:
            # pretty(container)
            self.set_video_get_from_yt_dlp()
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('main')

        # pretty(container)
        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/c/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = collect_string(item)
                self.add_tag(title, URL(href, base_url=url), style=dict(color='blue'))

            for item in _iter(container.find_all('a', href=lambda x:'/search?q=' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url),style=dict(color='gray'))


if __name__ == "__main__":
    pass
