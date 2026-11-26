__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.parser import BaseSiteParser

class EmpflixSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('empflix.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict()
        view.add_start_button(picture_filename='model/site/resource/empflix.png',
                              menu_items=menu_items,
                              url=URL("https://www.empflix.com/new*"))

    def get_shrink_name(self):
        return 'MHP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'video-list'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('a', {'class':'thumb'})):
                try:
                    # pretty(thumbnail)

                    # xref = thumbnail.find('a', href=True)
                    href = URL(thumbnail.attrs['href'], base_url=url)

                    img = thumbnail.find('img')
                    thumb_url = URL(img.attrs.get('data-src',img.attrs.get('src')), base_url=url)
                    label = img.attrs.get('alt')

                    # title_tag = thumbnail.find('a', {'class': 'video-item-title'})
                    # label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('div', {'class': 'video-duration'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('div', {'class': 'max-quality'})
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

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('video')
        if container:
            # pretty(container)
            self.set_video_get_from_yt_dlp()
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'video-detail-badges'})

        # pretty(container)
        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=True)):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = collect_string(item)
                if '/profile/' in href:
                    label_color='red'
                else:
                    label_color='black'
                self.add_tag(title, URL(href, base_url=url), style=dict(color=label_color))



    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        return self.title

if __name__ == "__main__":
    pass
