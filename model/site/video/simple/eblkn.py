__author__ = 'Vit'
from bs4 import BeautifulSoup
import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class EblknSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('eblkn.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict()
            # dict(New=URL('https://pornwild.to/ru/latest-updates/'),
            #         TopRated=URL('https://pornwild.to/ru/top-rated/'),
            #         Popular=URL('https://pornwild.to/ru/most-popular/')
            #         )

        view.add_start_button(picture_filename='model/site/resource/ebalkin-logo.png',
                              menu_items=menu_items,
                              url=URL("https://cxb.eblkn.com/"))

    def get_shrink_name(self):
        return 'EB'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('section', {'class':'video-category'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class':'video-item'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)

                    img = thumbnail.find('video')
                    img_url = img.attrs.get('poster')
                    thumb_url = URL(img_url, base_url=url)

                    title_tag = thumbnail.find('a', {'class': 'video-item-title'})
                    label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('div', {'class': 'drn1'})
                    dur_time = '' if duration is None else str(duration.string)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           ])
                except AttributeError:
                    print('AttributeError')
                    pass

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        # pretty(soup.find('div',{'class':'pagination-holder'}))
        return soup.find('div',{'class':'pagenav'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('section',{'class':'video-single'})
        if container:
            # pretty(container)

            frame=container.find('iframe')
            if frame:
                # pretty(frame)

                file_url=URL(frame.attrs['src'])
                filedata=FLData(file_url,'')
                #
                self._result_type = 'video'
                self.model.loader.start_load_file(filedata,self.continue_parse_video)

    def continue_parse_video(self, fldata:FLData):
        soup=BeautifulSoup(fldata.text, 'html.parser')
        container=soup.find('video-js',{'id':'player'})
        if container:
            # pretty(container)
            for item in _iter(container.find_all('source')):
                # pretty(item)
                self.add_video(item.attrs['label'], URL(item.attrs['src']))

            self.set_default_video(-1)
            self.generate_video_view()

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'video-item-desc'})

        # pretty(container)
        if container:
            pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/tag/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))

            for item in _iter(container.find_all('a', href=lambda x:'/category/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))

if __name__ == "__main__":
    pass
