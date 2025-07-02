# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class ErothotsSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('erothots1.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/erothots1.png',
                              # menu_items=menu_items,
                              url=URL("https://erothots1.com/videos/hot"))

    def get_shrink_name(self):
        return 'EH'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'videos'})
        # pretty(contents)
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('a', {'class': 'video-media'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail
                    href = URL(xref.attrs['href'], base_url=url)
                    # style=xref.attrs.get('style')
                    # psp(style)
                    img = thumbnail.find('img')
                    img_url = thumbnail.img.attrs.get('data-src', thumbnail.img.attrs.get('src', ''))
                    # img_url = quotes(str(style),"('","')")
                    # psp(img_url)
                    thumb_url = URL(img_url, base_url=url)
                    label = img.attrs.get('alt')

                    duration = thumbnail.find('span', {'class': 'caption'})
                    dur_time = '' if duration is None else collect_string(duration)

                    # hd_tag = thumbnail.find('div', {'class': 'quality'})
                    # hd = '' if hd_tag is None else collect_string(hd_tag)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           # {'text': hd, 'align': 'top left'}
                                           ])
                    # ])

                    # print('Adding', thumb_url,href,label,dur_time)
                except AttributeError as e:
                    pass


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'loadmore-menu'})

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            pretty(container)
            for page in _iter(container.find_all('a', {'href': True})):
                # if page.string and str(page.string).strip().isdigit():
                    self.add_page(str(page.string).strip(), URL(page.attrs['href'], base_url=url))
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video', {'class': 'v-player'})
        if video:
            # pretty(video)

            for source in _iter(video.find_all('source')):
                # psp(source)
                if 'http' in source.attrs.get('src',''):
                    self.add_video(source.attrs.get('type','default'), URL(source.attrs['src']))
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class':'list-btn'})
        if container:
            pretty(container)
            # for item in _iter(container.find_all('a', href=lambda x:'/videos/' in str(x))):
            #     # pretty(item)
            #     href = item.attrs.get('href', '')
            #     title = item.attrs.get('title', collect_string(item))
            #     self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))
            #
            # for item in _iter(container.find_all('a', href=lambda x:not ('/pornstar/' in str(x) or '/tag/' in str(x)))):
            #     # pretty(item)
            #     href = item.attrs.get('href', '')
            #     title = item.attrs.get('title', collect_string(item))
            #     self.add_tag(title, URL(href, base_url=url), style=dict(color='green'))


            for item in _iter(container.find_all('a', href=lambda x:'/videos/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))



        container=soup.find('div', {'class':'tags-container'})
        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/performerb/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/topic/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass
