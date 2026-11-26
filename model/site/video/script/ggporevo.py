# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class GgporevoSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('ggporevo.art/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):

        view.add_start_button(picture_filename='model/site/resource/ggporevo.webp',
                              # menu_items=menu_items,
                              url=URL("https://aaa.ggporevo.art/latest-updates/"))

    def get_shrink_name(self):
        return 'GP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'class':'list-videos'})

        if contents:
            pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class': 'item'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)

                    img = thumbnail.find('img')
                    thumb_url = URL(img.attrs.get('data-src',img.attrs.get('data-webp')), base_url=url)
                    label = img.attrs.get('alt')

                    # title_tag = thumbnail.find('span', {'class': 'title'})
                    # label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('div', {'class': 'duration'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('span', {'class': 'is-hd'})
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
        return soup.find('div',{'class':'load-more'})

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            # pretty(container)
            for page in _iter(container.find_all('a', {'href': True})):
                pretty(page)

                if '#' in page.attrs['href']:
                    self.add_page(str(page.string).strip(), URL(url.get().rstrip('/1234567890') + '/' + page.attrs['data-parameters'].split('from:')[1] + '/'))
                else:
                    self.add_page(str(page.string).strip(), URL(page.attrs['href'], base_url=url))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'block-video'})
        if video:
            # pretty(video)
            script=video.find('script',text=lambda x: 'video_url:' in str(x))
            # psp(script)

            item = quotes(str(script).replace(' ', ''), "video_url:'", "'")

            # psp(item)
            label = 'default'
            # src = quotes(item, '"src":"', '"').replace('\/', '/')
            # psp(label,src)
            self.add_video(label, URL(item, base_url=url))

            # if sources:
            #     # psp(sources)
            #     split=sources.split('},{')
            #     # psp(split)
            #     for item in split:
            #         # psp(item)
            #         label=quotes(item,'"label":"','"')
            #         src=quotes(item,'"src":"','"').replace('\/','/')
            #         # psp(label,src)
            #         self.add_video(label, URL(src, base_url=url))

                # self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'block-details'})

        # pretty(container)
        if container:
            pretty(container)
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

            for item in _iter(container.find_all('a', href=lambda x:'/categories/' in str(x))):
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
