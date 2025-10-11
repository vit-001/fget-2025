# -*- coding: utf-8 -*-
__author__ = 'Vit'
from urllib.parse import urlparse,urlsplit,parse_qs,urlencode
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornoneSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornone.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        view.add_start_button(picture_filename='model/site/resource/pornone.png',
                              # menu_items=menu_items,
                              url=URL("https://pornone.com/newest/"))

    def get_shrink_name(self):
        return 'PO'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'grid'})

        # if contents:
        for contents in _iter(soup.find_all('div', {'class':'grid'})):
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('a', {'class': 'videocard', 'href':True})):
                try:

                    # pretty(thumbnail)
                    # xref = thumbnail.find('a', href=True)
                    img = thumbnail.find('img', {'class': 'thumbimg'})
                    href = URL(thumbnail.attrs['href'], base_url=url)
                    img_url = img.attrs.get('data-src', img.attrs.get('src', ''))
                    thumb_url = URL(img_url, base_url=url)

                    title = thumbnail.find('div', {'class': 'videotitle'})
                    label = '' if title is None else collect_string(title)

                    duration = thumbnail.find('span', {'class': 'durlabel'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('span', {'class': 'item-quality'})
                    hd = '' if hd_tag is None else collect_string(hd_tag)


                    # print(thumb_url,href,label,dur_time,label,hd)
                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                except AttributeError as e:
                    print(e)
                    pass


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        # pretty(soup.find('nav',{'aria-label':'Pagination'}))
        return soup.find('nav',{'aria-label':'Pagination'})

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        # pretty(container)
        if container:
            if url.contain('/search/'):
                for page in _iter(container.find_all('span', {'class': 'linkage'})):
                    onclick=page.attrs.get('onclick', None)
                    if onclick:
                        # print(onclick)
                        pagenum=quotes(onclick,'gosearch(',')')
                        url.add_query([('page',pagenum)])
                        self.add_page(collect_string(page), URL(url.get()))

            for page in _iter(container.find_all('a', {'href': True})):
                # pretty(page)
                # if page.string and str(page.string).strip().isdigit():
                self.add_page(collect_string(page), URL(page.attrs['href'], base_url=url))
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video', {'id': 'pornone-video-player'})
        if video:
            # pretty(video)
            for source in _iter(video.find_all('source')):
                # psp(source)
                self.add_video(source.attrs.get('label','default'), URL(source.attrs['src']))
            # self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):

        for container in _iter(soup.find_all('div', {'class':'container'})):
            if container:
                # pretty(container)
                for item in _iter(container.find_all('a', {'class':'text-md', 'href':lambda x: '/channel/' in str(x)})):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    title = item.attrs.get('title', collect_string(item).strip(','))
                    self.add_tag(title, URL(href, base_url=url), style=dict(color='blue'))

        for container in _iter(soup.find_all('div', {'id':'pageinfo'})):
            if container:
                # pretty(container)
                for item in _iter(container.find_all('a', {'href':True, 'id':lambda x: 'star' in str(x)})):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    title = item.attrs.get('title', collect_string(item).strip(','))
                    self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

                for item in _iter(container.find_all('a', href=lambda x: '/channels/' in str(x))):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    title = item.attrs.get('title', collect_string(item).strip(','))
                    self.add_tag(title, URL(href, base_url=url), style=dict(color='blue'))

                for item in _iter(container.find_all('a', {'class':'links','href':True, 'id':lambda x: 'cat' in str(x)})):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    title = item.attrs.get('title', collect_string(item).strip(','))
                    self.add_tag(title, URL(href, base_url=url))

                for item in _iter(container.find_all('a', {'href':True, 'id':lambda x: 'tag' in str(x)})):
                    # pretty(item)
                    href = item.attrs.get('href', '')
                    title = item.attrs.get('title', collect_string(item).strip(','))
                    self.add_tag(title, URL(href, base_url=url), style=dict(color='gray'))

if __name__ == "__main__":
    pass
