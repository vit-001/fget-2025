__author__ = 'Vit'
from bs4 import BeautifulSoup
import yt_dlp

from data_format.url import URL
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.parser import BaseSiteParser

class TwoPornoSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('2porno.online/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict()
        view.add_start_button(picture_filename='model/site/resource/two_porno.png',
                              menu_items=menu_items,
                              url=URL("https://2porno.online/main/"))

    def get_shrink_name(self):
        return 'PP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):

        contents = soup.find('div', {'class':'thumbs__list'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class':'item'})):
                try:
                    # pretty(thumbnail)
                    # print(url)

                    xref = thumbnail.find('a', href=True)
                    if not '.html' in xref.attrs['href']: continue
                    href = URL(xref.attrs['href'], base_url=url)

                    img = thumbnail.find('img')
                    thumb_url = URL(img.attrs.get('data-src'), base_url=url)
                    label = img.attrs.get('alt')

                    # title_tag = thumbnail.find('a', {'class': 'video-item-title'})
                    # label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('div', {'class': 'box'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('div', {'class': 'box second'})
                    hd = '' if hd_tag is None else collect_string(hd_tag)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                except AttributeError as e:
                    print('AttributeError', str(e))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        pass

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        current_page = url.get().partition('/page/')[2].strip('/')
        if not current_page:
            current_page='1'
        # print('current',current_page)

        for page in range(int(current_page)-5, int(current_page)+5):
            if page <= 0: continue
            if page == int(current_page): continue
            # print(page)
            self.add_page(str(page), URL('/main/page/{0}/'.format(page), base_url=url))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('video',{'class':'video-js'})
        if container:
            # pretty(container)
            self.set_video_get_from_yt_dlp()

    def parse_video_with_yt_dlp(self, soup:BeautifulSoup, url:URL):
        print("Parcing with yt-dlp")
        ydl_opts = {'quiet': True,'no_warnings': True}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url.get(), download=False)

                if not info.get('formats'):
                    print("Нет доступных форматов или сайт заблокирован.")
                    return

                self.title=info['title']

                for fmt in info['formats']:
                    self.add_video('default', URL(fmt['url'], redirect=False, referer=url))

        except Exception as e:
            pass

if __name__ == "__main__":
    pass
