__author__ = 'Vit'
from bs4 import BeautifulSoup

import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser

class YPData(FLData):
    def __init__(self, url: URL, part: str):
        super().__init__(url, '')
        self.part=part

class YourpornSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('youporn.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Latest=URL('https://yourporn.sexy/blog/all/0.html?sm=latest*'),
                    Views=URL('https://yourporn.sexy/blog/all/0.html?sm=views*'),
                    Rating=URL('https://yourporn.sexy/blog/all/0.html?sm=rating*'),
                    Orgazmic=URL('https://yourporn.sexy/blog/all/0.html?sm=orgasmic*'),
                    )

        view.add_start_button(picture_filename='model/site/resource/youporn.png',
                              menu_items=menu_items,
                              url=URL("https://www.youporn.com/browse/time/"))

    def get_shrink_name(self):
        return 'YP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        main=soup.find('div',{'class':'container'})

        # for contents in _iter(soup.find_all('div', {'class':{'video_listing','searchResults'}})):
        # pretty(contents)
        for thumbnail in _iter(main.find_all('article', {'class': 'video-box'})):
            try:


                # pretty(thumbnail)
                xref=thumbnail.find('a',href=True)
                # xref = thumbnail
                # img=thumbnail.find('img',href=True)
                href = URL(xref.attrs['href'], base_url=url)
                img_url=thumbnail.img.attrs.get('data-src',thumbnail.img.attrs.get('data-poster',''))

                if '.mov/' in img_url or '.mp4/' in img_url:
                    # pretty(thumbnail)
                    # psp(img_url)
                    img_url ='https://ea.ypncdn.com/702f9f161d75867cd0a7b8670d84dcbf7f2081f4/youporn/cdn_assets/images/shared/logo.png'
                thumb_url = URL(img_url, base_url=url)

                # title_tag = thumbnail.find('div', {'class': 'th-title'})
                label = thumbnail.img.attrs.get('alt')

                duration = thumbnail.find('div', {'class': 'video-duration'})
                dur_time = '' if duration is None else collect_string(duration)
                # psp(dur_time)

                hd_tag = thumbnail.find('span', {'class': 'hd'})
                hd = '' if hd_tag is None else collect_string(hd_tag)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])
            except AttributeError as e:
                print(e)
                pass

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'id': 'pages'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div', {'id': 'watch-container'})
        # video_container = soup.find('div', {'itemprop': 'video'})

        if container:
            # pretty(container)
            self.set_video_get_from_yt_dlp(id_filter=lambda x:'hls-' in x)
            self.set_default_video(-1, override=True)

    def continue_parse_video(self, fldata: FLData):
        data = json.loads(fldata.text)
        # psp(data)
        for item in data:
            # psp(item)
            self.add_video(item['quality'], URL(item['videoUrl'], referer=self.base_url))
        self.generate_video_view()

    def parse_video_title(self, soup:BeautifulSoup, url:URL)->str:
        return collect_string(soup.find('title'))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):

        container = soup.find('div', {'class': 'tm_categoriesWrapper'})
        if container:
            # pretty(container)
            for href in _iter(container.find_all('a', href=lambda x: '/pornstar/' in str(x))):
                self.add_tag(collect_string(href), URL(href.attrs['href'],base_url=url), style={'color':'red'})

            for href in _iter(container.find_all('a', href=lambda x: '/category/' in str(x))):
                self.add_tag(collect_string(href), URL(href.attrs['href'],base_url=url), style={'color':'green'})

            for href in _iter(container.find_all('a', href=lambda x: '/porntags/' in str(x))):
                self.add_tag(collect_string(href), URL(href.attrs['href'],base_url=url), style={'color':'black'})

if __name__ == "__main__":
    pass
