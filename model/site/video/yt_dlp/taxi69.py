__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.parser import BaseSiteParser

class Taxi69Site(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('taxi69.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict()
        view.add_start_button(picture_filename='model/site/resource/taxi69.png',
                              menu_items=menu_items,
                              url=URL("https://taxi69.com/"))

    def get_shrink_name(self):
        return 'T69'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'vue_cosmponents'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class':'videoBlock'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    if xref:
                        href = URL(xref.attrs['href'], base_url=url)

                        img = thumbnail.find('img')
                        thumb_url = URL(img.attrs.get('src',img.attrs.get('data-webp')), base_url=url)
                        label = collect_string(thumbnail)

                        # title_tag = thumbnail.find('a', {'class': 'video-item-title'})
                        # label = '' if title_tag is None else collect_string(title_tag)

                        duration = thumbnail.find('div', {'class': 'time'})
                        dur_time = '' if duration is None else collect_string(duration, only_last=True)

                        hd_tag = thumbnail.find('span', {'class': 'hd-badge'})
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
        # pretty(soup.find('div',{'class':'pagination-holder'}))
        return soup.find('ul',{'class':'pagination'})

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            for page in _iter(container.find_all('a', {'href': True})):
                if page.string and str(page.string).strip().isdigit():
                    self.add_page(str(page.string).strip(), URL(url.get().partition('?')[0]+page.attrs['href']))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('video')
        if container:
            # pretty(container)
            self.set_video_get_from_yt_dlp()
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'buttons-row'})

        # pretty(container)
        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/models/' in str(x))):
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

            for item in _iter(container.find_all('a', href=lambda x:'/tags/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url),style=dict(color='gray'))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        return self.title

if __name__ == "__main__":
    pass
