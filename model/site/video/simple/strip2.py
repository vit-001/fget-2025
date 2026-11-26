# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class Strip2Site(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('strip2.co/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/strip2.png',
                              # menu_items=menu_items,
                              url=URL("https://vps404.strip2.co/videocat/new/"))

    def get_shrink_name(self):
        return 'PXP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'tiles_wrapper'})
        # pretty(contents)
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('div', {'class': 'tile'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)
                    img = thumbnail.find('img')
                    # psp(img.attrs.get('src'))
                    thumb_url = URL(img.attrs.get('data-s',img.attrs.get('src')), base_url=url,redirect=True)
                    label = img.attrs.get('alt')

                    # title = thumbnail.find('div', {'class': 'item_title'})
                    # label = '' if title is None else collect_string(title)

                    duration = thumbnail.find('span', {'class': 'fd'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('div', {'class': 'hd-text-icon'})
                    hd = '' if hd_tag is None else collect_string(hd_tag)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                except AttributeError as e:
                    # print(e)
                    pass


    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('nav',{'class':'menu-inner2'})
        if container:
            # psp(container.prettify())
            for item in _iter(container.find_all('li',{'class':'cat-item'})):
                # psp(item)
                tag=item.find('a')
                if tag:
                    # psp(tag)
                    self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('table',{'class':'table__nums'})


    def parse_video(self, soup: BeautifulSoup, url: URL):
        # pretty(soup)
        video = soup.find('div', {'class': 'video-player-container'})
        if video:
            # pretty(video)
            sources=video.attrs.get('data-sources')
            # print(sources)
            data_list = json.loads(sources)
            # print(data_list)
            if data_list:
                for data in data_list:
                    res=str(data['res'])
                    link=data['link']

                    print(res,link)
            # for source in _iter(video.find_all('source')):
            #     # psp(source)
                    self.add_video(res, URL(link,referer=url))
            #     curr+=1
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for container in _iter(soup.find_all('div', {'class':'break-word'})):
            if container:
                # pretty(container)


                for item in _iter(container.find_all('a', href=lambda x: '/videos/' in str(x))):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    self.add_tag(collect_string(item), URL(href, base_url=url), style=dict(color='red'))

                for item in _iter(container.find_all('a', href=lambda x: '/videocat/' in str(x))):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    self.add_tag(collect_string(item), URL(href, base_url=url), style=dict(color='black'))


        # for container in _iter(soup.find_all('div', {'class':'video-tags'})):
        #     if container:
        #         # pretty(container)
        #         for tag in _iter(container.find_all('a', {'href':True})):
        #             pretty(tag)
        #             href = tag.attrs.get('href', '')
        #             if '/tag/' in href:
        #                 self.add_tag(collect_string(tag), URL(href, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass
