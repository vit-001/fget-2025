# -*- coding: utf-8 -*-
__author__ = 'Vit'
import re
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, collect_string_to_array, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class SeverepornSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('severeporn.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):

        view.add_start_button(picture_filename='model/site/resource/severeporn.svg',
                              # menu_items=menu_items,
                              url=URL("https://severeporn.com/latest-updates/"))

    def get_shrink_name(self):
        return 'SP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'class':'list-videos'})

        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class': 'item'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)

                    img = thumbnail.find('img')
                    thumb_url = URL(img.attrs.get('data-original',img.attrs.get('data-webp')), base_url=url)
                    label = img.attrs.get('alt')

                    # title_tag = thumbnail.find('span', {'class': 'title'})
                    # label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('div', {'class': 'duration'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('span', {'class': 'is-hd'})
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
        return soup.find('div',{'class':'pagination'})

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            # pretty(container)
            for page in _iter(container.find_all('a', {'href': True})):
                if page.string and str(page.string).strip().isdigit():
                    self.add_page(str(page.string).strip(), URL(url.get().rstrip('/1234567890')+'/'+page.attrs['data-parameters'].split('from:')[1]+'/'))
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'player'})
        if video:
            # pretty(video)
            script=video.find('script',text=lambda x: 'video_url:' in str(x))
            # psp(str(script).replace("\t", ""))
            var = quotes(str(script).replace("\t", ""),'var','};').split('{')[1]
            # psp(var)

            # Регулярное выражение ищет шаблон НАЗВАНИЕ_КЛЮЧА: 'ЗНАЧЕНИЕ' или просто ЗНАЧЕНИЕ
            pattern = r"(\w+):\s*(?:'([^']*)'|([^,]+))"
            matches = re.findall(pattern, var)

            # Собираем в словарь (очищая от лишних пробелов по краям)
            data = {}
            for match in matches:
                key = match[0]
                # Берем значение либо из группы в кавычках, либо без кавычек
                value = match[1] if match[1] else match[2].strip()
                data[key] = value
                # print(key,value)

            # psp(data)

            if 'video_url' in data:
                self.add_video(data.get('video_url_text','SD'), URL(data.get('video_url'), base_url=url))

            if 'video_alt_url' in data:
                self.add_video(data.get('video_alt_url_text','HD'), URL(data.get('video_alt_url'), base_url=url))
                self.set_default_video(1)

            if 'video_alt_url2' in data:
                self.add_video(data.get('video_alt_url2_text','2K'), URL(data.get('video_alt_url2'), base_url=url))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'tags-video'})

        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/models/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = collect_string_to_array(item)[0]
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/studios/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='blue'))

            for item in _iter(container.find_all('a', href=lambda x:'/categories/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))

            for item in _iter(container.find_all('a', href=lambda x:'/tags/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url),style=dict(color='gray'))


    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass
