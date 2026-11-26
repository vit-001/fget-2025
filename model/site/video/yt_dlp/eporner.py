__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.parser import BaseSiteParser

class EpornerSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('eporner.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict()
        view.add_start_button(picture_filename='model/site/resource/eporner.png',
                              menu_items=menu_items,
                              url=URL("https://www.eporner.com/cat/all/"))

    def get_shrink_name(self):
        return 'SK'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        # pretty(soup)
        contents = soup.find('div', {'id':'content'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class':'mb'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)

                    img = thumbnail.find('img')
                    thumb_url = URL(img.attrs.get('data-src', img.attrs.get('src','')), base_url=url)
                    label = img.attrs.get('alt')

                    # title_tag = thumbnail.find('a', {'class': 'video-item-title'})
                    # label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('span', {'class': 'mbtim'})
                    dur_time = '' if duration is None else str(duration.string)

                    hd_tag = thumbnail.find('div', {'class': 'mvhdico'})
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
        return soup.find('div',{'class':'numlist2'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'id':'movieplayer-box'})
        if container:
            # pretty(container)
            self.set_video_get_from_yt_dlp()
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'video-info-tags'})

        # pretty(container)
        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/pornstar/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')+'recent/'
                title = item.attrs.get('title', collect_string(item).strip())
                if '/cat/pornstar/' in href:
                    continue
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/profile/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')+'uploaded-videos/'
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='blue'))

            for item in _iter(container.find_all('a', href=lambda x:'/cat/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))


    # def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
    #     return self.title.partition('- ')[-1][:50]

if __name__ == "__main__":
    pass
