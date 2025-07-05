# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup
import yt_dlp

import logging

from data_format.url import URL
from model.site.base_site import BaseSite
from interface.model_interface import ModelFromSiteInterface
from common.util import _iter, quotes, psp, sp, collect_string, pretty

class BaseSiteParser(BaseSite):

    def parse_soup(self, soup:BeautifulSoup, url:URL):
        try:
            self.parse_video(soup, url)
            if self.need_yt_dlp:
                self.parse_video_with_yt_dlp(soup, url)
            if self.is_video:
                self.parse_video_tags(soup, url)
                self.title=self.parse_video_title(soup,url)
                self.generate_video_view()
                return
            self.parse_pictures(soup, url)
            if self.is_pictures:
                self.parse_pictures_tags(soup, url)
                self.title=self.parse_pictures_title(soup,url)
                self.generate_pictures_view()
                return
            self.parse_thumbs(soup, url)
            if self.is_no_result:
                self.parse_others(soup, url)
                self.parse_pagination(soup, url)
            if self.is_thumbs:
                self.parse_thumbs_tags(soup, url)
                self.parse_pagination(soup, url)
                self.title=self.parse_thumb_title(soup,url)
                self.generate_thumb_view()
        except AttributeError as e:
            logging.exception(e.__repr__())
            # print(e.__repr__())

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        self.parse_video_thumbs(soup,url)
        if self.is_thumbs:
            return
        self.parse_picture_thumbs(soup,url)

    def parse_video_thumbs(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_picture_thumbs(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_video(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_video_with_yt_dlp(self, soup:BeautifulSoup, url:URL):
        print("Parcing with yt-dlp")
        ydl_opts = {'quiet': True,'no_warnings': True}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url.get(), download=False)

                if not info.get('formats'):
                    print("Нет доступных форматов или сайт заблокирован.")
                    return

                self.title=info['title']

                for fmt in info['formats']:
                    self.add_video(fmt['format_id'], URL(fmt['url'],redirect=self.redirect))

        except Exception as e:
            pass

    def parse_pictures(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_others(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            for page in _iter(container.find_all('a', {'href': True})):
                if page.string and str(page.string).strip().isdigit():
                    self.add_page(str(page.string).strip(), URL(page.attrs['href'], base_url=url))
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pagination'})

    def parse_thumbs_tags(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_video_tags(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_pictures_tags(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_thumb_title(self, soup:BeautifulSoup, url:URL)->str:
        return self.get_shrink_name().strip()+' '+self.get_thumb_label(url)

    def parse_video_title(self, soup:BeautifulSoup, url:URL)->str:
        if self.title:
            return self.title
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]

    def parse_pictures_title(self, soup:BeautifulSoup, url:URL)->str:
        return self.get_full_label(url)

    @staticmethod
    def get_thumb_label(url: URL) -> str:
        return url.get().partition(url.domain())[2].strip('/')

    @staticmethod
    def get_full_label(url: URL) -> str:
        return url.get().strip('/').rpartition('/')[2].partition('.')[0]

    def get_shrink_name(self):
        return '*'


if __name__ == "__main__":
    pass