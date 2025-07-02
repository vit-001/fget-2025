# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class IncestflixSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('incestflix.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/incestflix.png',
                              # menu_items=menu_items,
                              url=URL("https://www.incestflix.com/page/1"))

    def get_shrink_name(self):
        return 'IF'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'id':'incflix-indexwrap'})
        # pretty(contents)
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('a', {'id': 'videolink'}, href=True)):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail
                    href = URL(xref.attrs['href'], base_url=url)
                    img = thumbnail.find('div', {'class':'img-overflow'})
                    style=img.attrs.get('style').replace(' ','')
                    # psp(style)
                    # psp(quotes(style,'url(',')'))
                    thumb_url = URL(quotes(style,'url(',')'))
                    label = collect_string(img)

                    # title = thumbnail.find('div', {'class': 'item_title'})
                    # label = '' if title is None else collect_string(title)

                    duration = thumbnail.find('span', {'class': 'minutos'})
                    dur_time = '' if duration is None else collect_string(duration)

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
        return soup.find('table',{'id':'incflix-pager'})

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            # pretty(container)
            for page in _iter(container.find_all('a', {'href': True})):
                if page.string:# and str(page.string).strip().isdigit():
                    self.add_page(str(page.string).strip(), URL(page.attrs['href'], base_url=url))
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])


    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'id': 'incflix-stream'})
        if video:
            # pretty(video)
            for source in _iter(video.find_all('source')):
                # psp(source)
                self.add_video(source.attrs.get('type','default'), URL(source.attrs['src']))
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):

        for container in _iter(soup.find_all('div', {'id':'videotags'})):
            if container:
                # pretty(container)
                for tag in _iter(container.find_all('a',href=lambda x:'/tag/' in str(x))):
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
