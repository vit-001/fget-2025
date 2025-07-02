__author__ = 'Vit'
from bs4 import BeautifulSoup
import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class ThepornfullSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('thepornfull.net/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        # menu_items=dict(Pornstars=URL('http://toseeporn.com/Actor*'),
        #             Home=URL('http://toseeporn.com/*'),
        #             Search_Example=URL('http://toseeporn.com/Search=asian%20sex%20diary*')
        #             )

        view.add_start_button(picture_filename='model/site/resource/Thepornfull.png',
                              # menu_items=menu_items,
                              url=URL("https://thepornfull.net/"))

    def get_shrink_name(self):
        return 'HB'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        container = soup.find('section', {'class': 'Eroz-Thumbs'})
        if container:
            # pretty(container)
            for thumbnail in _iter(soup.find_all('article', {'class':'post'})):
                try:
                    # pretty(thumbnail)
                    xref=thumbnail.find('a', href=True)
                    img=thumbnail.find('img', src=True, alt=True)

                    href = URL(xref.attrs.get('href'), base_url=url)
                    thumb_url = URL(img.attrs.get('src'), base_url=url)

                    label = img.attrs.get('alt')

                    duration = thumbnail.find('span', {'class': 'duration'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_span = str(thumbnail.find('span', {'class': 'video-resolution'}))
                    hd = 'HD' if 'HD.png' in hd_span else ''

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                except AttributeError:
                    pass

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('nav',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video=soup.find('div', {'class':'Player'})
        if video:
            # pretty(video)
            frame = video.find('iframe', src=True)
            if frame:
                # pretty(frame)

                filedata=FLData(URL(frame.attrs.get('src')),'')
            #
                self._result_type = 'video'
                self.model.loader.start_load_file(filedata,self.continue_parse_video)

    def continue_parse_video(self, fldata:FLData):
        soup=BeautifulSoup(fldata.text, 'html.parser')
        # pretty(soup)
        script = soup.find('script', text=lambda x: 'jwplayer("jwplayer").setup' in str(x))
        if script:
            # psp(script)
            video_url = quotes(str(script).replace(' ', ''), 'file:"', '"')
            self.add_video('default', URL(video_url,base_url=fldata.url))
            self.generate_video_view()
        else:
            print('No video here')

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'MoreInfo post'})
        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/toro_pornstar/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:(not (('/tag/' in str(x)) or ('/toro_pornstar/' in str(x)))))):
                # pretty(item)
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url))

            for item in _iter(container.find_all('a', href=lambda x:'/tag/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url), style=dict(color='black'))



if __name__ == "__main__":
    pass
