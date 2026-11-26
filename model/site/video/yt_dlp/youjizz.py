__author__ = 'Vit'
from bs4 import BeautifulSoup
import yt_dlp

from data_format.url import URL
from common.util import _iter, quotes, pretty, collect_string, psp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class YoujizzSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('youjizz.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict()

        view.add_start_button(picture_filename='model/site/resource/youjizz.png',
                              menu_items=menu_items,
                              url=URL("https://www.youjizz.com/newest-clips/1.html*"))

    def get_shrink_name(self):
        return 'XM'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        # print('parse_thumbs')
        for thumb_container in _iter(soup.find_all('div',{'id':'content'})):
            # pretty(thumb_container)
            for thumb in _iter(thumb_container.find_all('div',{'class':'video-thumb'})):
                try:
                    # pretty(thumb)

                    xref = thumb.find('a', {'class':'video','href':True})
                    href = URL(xref.attrs['href'], base_url=url)

                    img = thumb.find('img')
                    thumb_url = URL(img.attrs.get('data-original'), base_url=url)
                    # label = img.attrs.get('alt')

                    title_tag = thumb.find('div', {'class': 'video-title'})
                    label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumb.find('span', {'class': 'time'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumb.find('div', {'class': 'wrap second'})
                    hd = '' if hd_tag is None else collect_string(hd_tag)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                except AttributeError as e:
                    print('AttributeError', str(e))

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        menu=soup.find('div', {'id':'menuLeft'})
        if menu:
            hrefs=menu.find_all('a',{'href':lambda x: '/channels/' in x})
            for item in _iter(hrefs):
                label=''
                for s in item.stripped_strings:
                    label +=s
                href = item.attrs['href']
                self.add_tag(label.strip(), URL(href, base_url=url))

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        return super().parse_thumb_title(soup, url).partition('.')[0]

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('ul', {'class': 'pagination'})

    # def parse_video(self, soup: BeautifulSoup, url: URL):
    #     video = soup.find('script', {'id': 'initials-script'})
    #     if video:
    #         # pretty(video)
    #         script=str(video)
    #         if script:
    #             data = str(script).replace(' ', '').replace('\\/', '/')
    #             if '"sources":' in data:
    #                 # psp(data)
    #                 sources=quotes(data,'"sources":{','}').split('","')
    #                 # psp(sources)
    #                 for item in sources:
    #                     # psp(item)
    #                     part=item.partition('":"')
    #                     # psp(part)
    #                     file = part[2].strip('"')
    #                     label=part[0].strip('"')
    #                     self.add_video(label, URL(file, base_url=url))
    #                 self.set_default_video(-1)

    def parse_video(self, soup: BeautifulSoup, url: URL):
        script = soup.find('script', text=lambda x: 'dataEncodings' in str(x))
        if script:
            # pretty(script)
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
                    if 'hls' not in fmt['format_id']:
                        self.add_video(fmt['format_id'], URL(fmt['url'],redirect=self.redirect))

        except Exception as e:
            pass

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'tag-list'})

        # pretty(container)
        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/pornstars/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item).strip())
                # if '/cat/pornstar/' in href:
                #     continue
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/channels/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='blue'))

            for item in _iter(container.find_all('a', href=lambda x:'/tags/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))



if __name__ == "__main__":
    pass