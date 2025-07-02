# -*- coding: utf-8 -*-
__author__ = 'Vit'

from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class UppornxSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('uppornx.com/')

    @staticmethod
    def create_start_button(view: ViewManagerFromModelInterface):  #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/UPporn_white.svg',
                              # menu_items=menu_items,
                              # name='DPI:4',
                              url=URL("https://www.uppornx.com/"))

    def get_shrink_name(self):
        return 'UP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class', 'thumbs'})
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('div', {'class': 'thumb'})):
                # psp(thumbnail.prettify())
                xref = thumbnail.find('a', href=True)
                href = URL(xref.attrs['href'], base_url=url)
                img_url = thumbnail.img.attrs.get('data-src', thumbnail.img.attrs.get('src', ''))
                thumb_url = URL(img_url, base_url=url)

                title_tag = thumbnail.find('div', {'class': 'title'})
                label = '' if title_tag is None else collect_string(title_tag)

                duration = thumbnail.find('div', {'class': 'time'})
                if duration is None:
                    duration = thumbnail.find('span', {'class': 'duration'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_tag = thumbnail.find('div', {'class': 'qualtiy'})
                if hd_tag is None:
                    hd_tag = thumbnail.find('span', {'class': 'hdthumb'})
                hd = '' if hd_tag is None else collect_string(hd_tag)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text': dur_time, 'align': 'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text': label, 'align': 'bottom center'},
                                       {'text': hd, 'align': 'top left'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container = soup.find('nav', {'class': 'menu-inner2'})
        if container:
            # psp(container.prettify())
            for item in _iter(container.find_all('li', {'class': 'cat-item'})):
                # psp(item)
                tag = item.find('a')
                if tag:
                    # psp(tag)
                    self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pagination'})

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            req_base=url.get().split('?mode=')[0]
            # print(req_base)
            for page in _iter(container.find_all('a', {'href': True})):
                if page.string and str(page.string).strip().isdigit():
                    if page.attrs.get('data-action') == 'ajax':
                        data_block_id = page.attrs.get('data-block-id')
                        data_parameters = page.attrs.get('data-parameters').replace(':','=').replace(';','&')

                        req_addr = req_base + '?mode=async&function=get_block&block_id={0}&{1}'.format(
                            data_block_id, data_parameters)
                        self.add_page(str(page.string).strip(), URL(req_addr))
                    else:
                        self.add_page(str(page.string).strip(), URL(page.attrs['href'], base_url=url))
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video', {'id': 'video-id'})
        if video:
            pretty(video)
            for source in _iter(video.find_all('source')):
                # psp(source)
                if 'http' in source.attrs.get('src', ''):
                    self.add_video(source.attrs.get('title', 'default'), URL(source.attrs['src']))
            # self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for container in _iter(soup.find_all('div', {'class':'video-holder'})):
            if container:
                # pretty(container)
                for tag in _iter(container.find_all('a',href=lambda x:'/models/' in str(x))):
                    # pretty(tag)
                    href = tag.attrs.get('href', '')
                    self.add_tag(collect_string(tag), URL(href, base_url=url), style=dict(color='red'))

                for tag in _iter(container.find_all('a',href=lambda x:'/tags/' in str(x))):
                    # pretty(tag)
                    href = tag.attrs.get('href', '')
                    self.add_tag(collect_string(tag), URL(href, base_url=url), style=dict(color='black'))


        models = soup.find('div', {'class': 'meta-item'})
        if models:
            # pretty(models)
            for xref in _iter(models.find_all('a', href=lambda x: not 'javascript' in str(x))):
                # psp(xref)
                href = xref.attrs.get('href', '')
                self.add_tag(collect_string(xref), URL(href, base_url=url), style=dict(color='blue'))

        categories = soup.find('div', {'class': 'full-category'})
        if categories:
            # pretty(categories)
            for xref in _iter(categories.find_all('a', href=lambda x: not 'javascript' in str(x))):
                # psp(xref)
                href = xref.attrs.get('href', '')
                self.add_tag(collect_string(xref), URL(href, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head = soup.find('head')
        title = collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass
