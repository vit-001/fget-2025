# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class FetishshrineSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('fetishshrine.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        view.add_start_button(picture_filename='model/site/resource/fetishshrine.svg',
                              # menu_items=menu_items,
                              url=URL("https://www.fetishshrine.com/latest-updates/"))

    def get_shrink_name(self):
        return 'FS'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):

        contents = soup.find('div', {'class':'thumbs-list'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class': 'thumb'})):
                # pretty(thumbnail)
                try:

                    xref = thumbnail.find('a', href=True)
                    img = thumbnail.find('img')
                    href = URL(xref.attrs['href'], base_url=url)
                    img_url = img.attrs.get('contenturl', '')
                    thumb_url = URL(img_url, base_url=url)

                    # title = thumbnail.find('div', {'class': 'item_title'})
                    label = img.attrs.get('alt',  '')

                    duration = thumbnail.find('span', {'class': 'length'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('span', {'class': 'hd'})
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
        return soup.find('div',{'class':'paging-area'})


    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'block-player'})
        if video:
            # pretty(video)
            for source in _iter(video.find_all('meta',itemprop="contentUrl")):
                # psp(source)
                self.add_video(source.attrs.get('type','default'), URL(source.attrs['content']))
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):

        for container in _iter(soup.find_all('div', {'class':'player-info'})):
            if container:
                # pretty(container)
                for tag in _iter(container.find_all('a',href=lambda x:'/pornstars/' in str(x))):
                    # pretty(tag)
                    href = tag.attrs.get('href', '')
                    self.add_tag(collect_string(tag), URL(href, base_url=url), style=dict(color='red'))

                for tag in _iter(container.find_all('a',href=lambda x:'/categories/' in str(x))):
                    # pretty(tag)
                    href = tag.attrs.get('href', '')
                    self.add_tag(collect_string(tag), URL(href, base_url=url), style=dict(color='black'))

        for container in _iter(soup.find_all('div', {'class':'video-tags'})):
            if container:
                pretty(container)
                for tag in _iter(container.find_all('a',href=lambda x:'/tags/' in str(x))):
                    # pretty(tag)
                    href = tag.attrs.get('href', '')
                    self.add_tag(collect_string(tag), URL(href, base_url=url), style=dict(color='gray'))


    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass
