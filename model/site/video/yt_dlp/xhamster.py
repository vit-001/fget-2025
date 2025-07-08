__author__ = 'Vit'
from bs4 import BeautifulSoup
import yt_dlp

from data_format.url import URL
from common.util import _iter, quotes, pretty, collect_string, psp, collect_string_to_array

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class XhamsterSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('xhamster.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict()

        view.add_start_button(picture_filename='model/site/resource/xmaster.svg',
                              menu_items=menu_items,
                              url=URL("https://ru.xhamster.com/newest*"))

    def get_shrink_name(self):
        return 'XM'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        # print('parse_thumbs')
        for thumb_container in _iter(soup.find_all('div',{'class':'thumb-list'})):
            # pretty(thumb_container)
            for thumb in _iter(thumb_container.find_all('div',{'class':'video-thumb'})):
                try:
                    # pretty(thumb)
                    href = URL(thumb.a.attrs['href'], base_url=url)
                    description = thumb.a.img.attrs['alt']
                    thumb_url = URL(thumb.img.attrs['src'], base_url=url)

                    duration = thumb.find('div', {'data-role':'video-duration'})
                    dur_time = '' if duration is None else str(duration.string)

                    quality = thumb.find('div', {'class': "hSpriteHD"})
                    qual = '' if quality is None else 'HD'

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                    labels=[{'text': dur_time, 'align': 'top right'},
                                            {'text': description, 'align': 'bottom center'},
                                            {'text': qual, 'align': 'top left', 'bold': True}])
                except AttributeError as e:
                    print(e.__repr__())


    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        return super().parse_thumb_title(soup, url).partition('.')[0]

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'page-list-container'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div', {'class': 'player-container'})
        if container:
            # pretty(video)
            self.set_video_get_from_yt_dlp()
            self.set_default_video(-1)

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
                    if 'mp4' in fmt['format_id']:
                        self.add_video(fmt['format_id'], URL(fmt['url'],redirect=self.redirect))

        except Exception as e:
            pass

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container = soup.find('nav', {'id': 'video-tags-list-container'})

        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/pornstars/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')+'/newest'
                title = item.attrs.get('title', collect_string_to_array(item)[0])
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/channels/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string_to_array(item)[0])
                self.add_tag(title, URL(href, base_url=url), style=dict(color='blue'))

            for item in _iter(container.find_all('a', href=lambda x:'/categories/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='black'))

            for item in _iter(container.find_all('a', href=lambda x:'/tags/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='gray'))

if __name__ == "__main__":
    pass