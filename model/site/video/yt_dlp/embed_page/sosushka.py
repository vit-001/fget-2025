__author__ = 'Vit'
from bs4 import BeautifulSoup
import yt_dlp
from data_format.url import URL
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.parser import BaseSiteParser

class SosushkaSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('sosushka.vip/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict()
        view.add_start_button(picture_filename='model/site/resource/sosushka.png',
                              menu_items=menu_items,
                              url=URL("https://go.sosushka.vip/new/"))

    def get_shrink_name(self):
        return 'SS'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'thumbs-wrap'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class':'thumb'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)

                    img = thumbnail.find('img')
                    thumb_url = URL(img.attrs.get('data-src', img.attrs.get('src','')), base_url=url)
                    label = img.attrs.get('alt')

                    # title_tag = thumbnail.find('a', {'class': 'video-item-title'})
                    # label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('span', {'class': 'right'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('span', {'class': 'top-right'})
                    hd = '' if hd_tag is None else collect_string(hd_tag).strip()

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
        return soup.find('div',{'class':'pages'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'player'})
        if container:
            # pretty(container)
            frame=container.find('iframe',src=True)
            if frame:
                # pretty(frame)
                self.url=URL(frame.attrs['src'], base_url=url)
                self.set_video_get_from_yt_dlp()
                # self.set_default_video(-1)

    def parse_video_with_yt_dlp(self, soup:BeautifulSoup, url:URL):
        super().parse_video_with_yt_dlp(soup, self.url)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'full-links'})
        if container:
            pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/model/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item).strip())
                # if '/cat/pornstar/' in href:
                #     continue
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/studio/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='blue'))

            def is_cathegory(href:str) ->bool:
                if '/tags/' in href:
                    return False
                if '/studio/' in href:
                    return False
                if '/model/' in href:
                    return False
                return True

            for item in _iter(container.find_all('a', href=lambda x:is_cathegory(str(x)))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))

            for item in _iter(container.find_all('a', href=lambda x:'/tags/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='gray'))


    # def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
    #     return self.title.partition('- ')[-1][:50]

if __name__ == "__main__":
    pass
