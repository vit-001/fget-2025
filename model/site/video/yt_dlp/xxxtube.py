__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.parser import BaseSiteParser

class XxxTubeSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('x-x-x.tube/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict()
        view.add_start_button(picture_filename='model/site/resource/xxxtube.svg',
                              menu_items=menu_items,
                              url=URL("https://x-x-x.tube/videos/"))

    def get_shrink_name(self):
        return 'SK'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'thumb-holder'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class':'item'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)

                    img = thumbnail.find('img')
                    thumb_url = URL(img.attrs.get('data-original'), base_url=url)
                    label = img.attrs.get('alt')

                    # title_tag = thumbnail.find('a', {'class': 'video-item-title'})
                    # label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('div', {'class': 'duration'})
                    dur_time = '' if duration is None else str(duration.string)

                    hd_tag = thumbnail.find('div', {'class': 'wrap second'})
                    hd = '' if hd_tag is None else collect_string(hd_tag)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                except AttributeError:
                    print('AttributeError')
                    pass

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        # pretty(soup.find('div',{'class':'pagination-holder'}))
        return soup.find('ul',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'player'})
        if container:
            # pretty(container)
            self.set_video_get_from_yt_dlp()
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container1 = soup.find('div', {'class': 'video-wrapper'})

        # pretty(container)
        if container1:
            pretty(container1)
            for item in _iter(container1.find_all('a', class_='btn', href=lambda x: '/models/' in str(x))):
                pretty(item)
                href = item.attrs.get('href', '') + 'videos/?by=post_date'
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

        container=soup.find('div', {'class': 'video-info'})

        # pretty(container)
        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', class_='row-item', href=lambda x:'/models/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/studios/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='blue'))

            for item in _iter(container.find_all('a', href=lambda x:'/categories/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '') + 'videos/?by=post_date'
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))

            for item in _iter(container.find_all('a', href=lambda x:'/tags/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')+ 'videos/?by=post_date'
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        return self.title.partition('- ')[-1][:50]

if __name__ == "__main__":
    pass
