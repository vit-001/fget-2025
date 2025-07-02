# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class VtraheSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('vtrahe.page/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/Vtrahe.png',
                              # menu_items=menu_items,
                              url=URL("https://sex.vtrahe.page/", test_string='порно'))

    def get_shrink_name(self):
        return 'VT'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'contentbl'})
        # pretty(contents)
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('div', {'id': 'preview'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)
                    # style=xref.attrs.get('style')
                    # psp(style)
                    img = thumbnail.find('img')
                    img_url = thumbnail.img.attrs.get('data-webp', thumbnail.img.attrs.get('src', ''))
                    # img_url = quotes(str(style),"('","')")
                    # psp(img_url)
                    thumb_url = URL(img_url, base_url=url)
                    label = img.attrs.get('title')

                    duration = thumbnail.find('div', {'class': 'dlit'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('div', {'class': 'quality'})
                    hd = '' if hd_tag is None else collect_string(hd_tag)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                    # ])
                except AttributeError as e:
                    pass


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'navigation'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'id': 'player'})
        if video:
            # pretty(video)
            # print(video.attrs)
            # for item in video.attrs:
            #     print(item, video.attrs.get(item))
            data_id=video.attrs.get('data-id')
            data_f=video.attrs.get('data-f')
            data_q=video.attrs.get('data-q')
            data_q_split=data_q.strip().split(';')
            data_t=video.attrs.get('data-t')
            data_n=video.attrs.get('data-n')

            # print(data_q_split)

            # формат адреса: 'https://v2.cdnde.com/x2/upload_6f59938eceaf7a4ed8f06874a9dd1e69/37968/JOPORN_NET_37968_480p.mp4?time=1730615705'
            video_addr='https://v{0}.cdnde.com/x{0}/upload{1}/{2}/JOPORN_NET_{2}_{3}.mp4?time={4}'.format(data_n,data_q_split[1],data_id,data_q_split[0],data_q_split[4])
            # print(video_addr)

            self.add_video('default', URL(video_addr))

            for source in _iter(video.find_all('source')):
                # psp(source)
                if 'http' in source.attrs.get('src',''):
                    self.add_video(source.attrs.get('type','default'), URL(source.attrs['src']))
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'id':'ivideoinfo'})
        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/pornstar/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:not ('/pornstar/' in str(x) or '/tag/' in str(x)))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='green'))


            for item in _iter(container.find_all('a', href=lambda x:'/tag/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))



        container=soup.find('div', {'class':'tags-container'})
        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/performerb/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/topic/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass
