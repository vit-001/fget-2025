# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class MotherlessSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('motherless.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/motherless.png',
                              # menu_items=menu_items,
                              url=URL("https://motherless.com/videos/recent", test_string='porn'))

    def get_shrink_name(self):
        return 'VT'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'content-inner'})
        # pretty(contents)
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('div', {'class': 'thumb-container video'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)
                    # style=xref.attrs.get('style')
                    # psp(style)
                    img = thumbnail.find('img',{'class': 'static'})
                    # pretty(img)
                    img_url = img.attrs.get('src')
                    # img_url = quotes(str(style),"('","')")
                    # psp(img_url)
                    thumb_url = URL(img_url, base_url=url)
                    label = img.attrs.get('alt')

                    duration = thumbnail.find('span', {'class': 'size'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('div', {'class': 'quality'})
                    hd = '' if hd_tag is None else collect_string(hd_tag)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                    # ])
                except AttributeError as e:
                    print(e.name)
                    pass


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'pagination_link'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'id': 'content'})
        script = soup.find('script', text=lambda x: '__fileurl' in str(x))
        if script:
            # pretty(script)
            addr = quotes(str(script).replace(' ', ''), "__fileurl='", "'")

            self.add_video('default', URL(addr))
            # self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class':'media-meta-member'})
        if container:
            pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/m/' in str(x))):
                pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                videos_addr=href.replace('/m/','/u/')+'?t=v'
                self.add_tag(title, URL(videos_addr, base_url=url), style=dict(color='red'))


        container=soup.find('div', {'class':'media-meta-tags'})
        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/term/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                videos_addr=href.replace('/term/','/term/videos/')
                # print(videos_addr,'https://motherless.com/term/videos/teen?term=teen&range=0&size=0&sort=relevance')
                self.add_tag(title, URL(videos_addr, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass
