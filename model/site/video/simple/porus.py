# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PorusSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('po0.hd.vg/') or url.contain('porus.cam/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/porus.jpg',
                              # menu_items=menu_items,
                              url=URL("https://po0.hd.vg/"))

    def get_shrink_name(self):
        return 'IF'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'id':'m'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class': 'v'})):
                # pretty(thumbnail)
                try:

                    xref = thumbnail.find('a', href=True)
                    img = thumbnail.find('img')
                    href = URL(xref.attrs['href'], base_url=url)
                    img_url = img.attrs.get('data-src', img.attrs.get('src', ''))
                    thumb_url = URL(img_url, base_url=url)

                    # title = thumbnail.find('div', {'class': 'item_title'})
                    label = img.attrs.get('alt',  '')

                    duration = thumbnail.find('b')
                    dur_time = '' if duration is None else collect_string(duration).split('/')[-1]

                    hd_tag = thumbnail.find('span', {'class': 'hd sprite'})
                    hd = '' if hd_tag is None else "HD"

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                except AttributeError as e:
                    # print(e)
                    pass


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'p'})

    # def parse_pagination(self, soup: BeautifulSoup, url: URL):
    #     container = self.get_pagination_container(soup)
    #     if container:
    #         # pretty(container)
    #         for page in _iter(container.find_all('a', {'href': True})):
    #             if page.string:# and str(page.string).strip().isdigit():
    #                 self.add_page(str(page.string).strip(), URL(page.attrs['href'], base_url=url))
    #                 # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])


    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video', {'id': 'vp'})
        if video:
            # pretty(video)
            for source in _iter(video.find_all('source')):
                # psp(source)
                self.add_video(source.attrs.get('type','default'), URL(source.attrs['src']))
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):

        for container in _iter(soup.find_all('ul', {'id':'vc'})):
            if container:
                # pretty(container)
                for tag in _iter(container.find_all('a',href=lambda x:'/t/' in str(x))):
                    # pretty(tag)
                    href = tag.attrs.get('href', '')
                    self.add_tag(collect_string(tag), URL(href, base_url=url), style=dict(color='blue'))

                for tag in _iter(container.find_all('a',href=lambda x:'/c/' in str(x))):
                    # pretty(tag)
                    href = tag.attrs.get('href', '')
                    self.add_tag(collect_string(tag), URL(href, base_url=url), style=dict(color='black'))




    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass
