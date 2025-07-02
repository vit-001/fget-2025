__author__ = 'Vit'
from bs4 import BeautifulSoup
import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornvideobbSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornvideobb.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict()
            # dict(New=URL('https://pornwild.to/ru/latest-updates/'),
            #         TopRated=URL('https://pornwild.to/ru/top-rated/'),
            #         Popular=URL('https://pornwild.to/ru/most-popular/')
            #         )

        view.add_start_button(picture_filename='model/site/resource/pvbb.png',
                              menu_items=menu_items,
                              url=URL("https://2023.pornvideobb.com/home/?d=11&sort=date&page=1"))

    def get_shrink_name(self):
        return 'EB'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('ul', {'id':'ul-porn-set'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('li', {'id':'li-porn-video-set'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)

                    img = xref.find('img')
                    img_url = img.attrs.get('src')
                    thumb_url = URL(img_url, base_url=url)

                    # title_tag = thumbnail.find('a', {'class': 'video-item-title'})
                    # label = '' if title_tag is None else collect_string(title_tag)

                    label=img.attrs.get('alt')

                    duration = thumbnail.find('i', {'class': 'cifra-time-set'})
                    dur_time = '' if duration is None else collect_string(duration)

                    quality = thumbnail.find('span', {'class': "hd-video"})
                    qual = '' if quality is None else collect_string(quality)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': qual, 'align': 'top left'},
                                           {'text': label, 'align': 'bottom center'},
                                           ])
                except AttributeError:
                    print('AttributeError')
                    pass

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        # pretty(soup.find('div',{'class':'pagination-holder'}))
        return soup.find('div',{'class':'pstrnav'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        script = soup.find('script', text=lambda x: 'Playerjs' in str(x))
        # container=soup.find('div',{'class':'video-player'})
        if script:
            pretty(script)

            video_url = quotes(str(script), 'file:"', '"')
            self.add_video('default', URL(video_url, base_url=url))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'block-porn-category'})

        # pretty(container)
        if container:
            pretty(container)

            for item in _iter(container.find_all('a', href=lambda x:'/zone_actor/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/zone_video/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))

            for item in _iter(container.find_all('a', href=lambda x:'/tags_page' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))

if __name__ == "__main__":
    pass
