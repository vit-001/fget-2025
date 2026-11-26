# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class FreeonestubeSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('freeonestube.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):

        view.add_start_button(picture_filename='model/site/resource/freeonestube.jpg',
                              # menu_items=menu_items,
                              url=URL("https://freeonestube.com/?sorting=latest*"))

    def get_shrink_name(self):
        return 'FO'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'class':'video-loop'})

        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class': 'video-block-wrapper'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)

                    img = thumbnail.find('img')
                    thumb_url = URL(img.attrs.get('src',img.attrs.get('data-webp')), base_url=url)
                    # label = img.attrs.get('alt')

                    title_tag = thumbnail.find('span', {'class': 'title'})
                    label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('span', {'class': 'duration'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('span', {'class': 'hd-video'})
                    hd = '' if hd_tag is None else collect_string(hd_tag)

                    # psp(thumb_url,href,label,dur_time,hd)
                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                except AttributeError as e:
                    print('AttributeError',e.name)
                    pass

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('ul',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'responsive-player'})
        if video:
            # pretty(video)
            script=video.find('script',text=lambda x: 'playerOptions' in str(x))
            # psp(script)

            sources = quotes(str(script).replace(' ', ''), "sources:[{", "}]")
            if sources:
                # psp(sources)
                split=sources.split('},{')
                # psp(split)
                for item in split:
                    # psp(item)
                    label=quotes(item,'"label":"','"')
                    src=quotes(item,'"src":"','"').replace('\/','/')
                    # psp(label,src)
                    self.add_video(label, URL(src, base_url=url))

                # self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'id': 'video-about'})

        # pretty(container)
        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/actor/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = collect_string(item)
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/studios/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='blue'))

            for item in _iter(container.find_all('a', href=lambda x:'/category/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))

            for item in _iter(container.find_all('a', href=lambda x:'/tag/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url),style=dict(color='gray'))


    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass
