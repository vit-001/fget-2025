# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class SextubeNlSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('sextube.nl/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(New=URL('http://www.sextube.nl/videos/nieuw*'),
                    Videos_Top_Rated=URL('http://www.sextube.nl/videos/hoog-gewaardeerd*'),
                    Popular=URL('http://www.sextube.nl/videos/populair*'),
                    HD=URL('http://www.sextube.nl/videos/hd*'))

        view.add_start_button(picture_filename='model/site/resource/sextube_nl.png',
                              menu_items=menu_items,
                              url=URL("http://www.sextube.nl/videos/nieuw*"))

    def get_shrink_name(self):
        return 'NL'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class':'video-loop'})
        if container:
            # psp(contents.prettify())
            for thumbnail in _iter(container.find_all('div', {'class': 'col-6'})):

                pretty(thumbnail)
                xref=thumbnail.find('a',href=True)
                href = URL(xref.attrs['href'], base_url=url)
                img_url=thumbnail.img.attrs.get('data-src',thumbnail.img.attrs.get('src',''))
                thumb_url = URL(img_url, base_url=url)

                title_tag = thumbnail.find('span', {'class': 'title'})
                label = collect_string(title_tag)

                duration = thumbnail.find('span', {'class': 'duration'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_tag = thumbnail.find('svg', {'class': 'hd-icon'})
                hd = '' if hd_tag is None else "HD"

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('ul',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'video-player'})
        if container:
            # pretty(container)
            source=container.find('meta',{'itemprop':'contentURL'}, content=True)
            if source:
                # psp(source)
                self.add_video('default',URL(source.attrs['content']))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'video-cat-tag'})
        if container:
            for tag in container.find_all('a',href=True,title=True):
                self.add_tag(tag.attrs['title'],URL(tag.attrs['href'],base_url=url))

if __name__ == "__main__":
    pass
