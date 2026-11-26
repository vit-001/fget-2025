__author__ = 'Vit'
import time
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, pretty, collect_string, collect_string_to_array

from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.parser import BaseSiteParser

class PervertiumSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pervertium.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict()
        view.add_start_button(picture_filename='model/site/resource/pervertium.svg',
                              menu_items=menu_items,
                              url=URL("https://www.pervertium.com/last-updates/"))

    def get_shrink_name(self):
        return 'PV'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'list-videos'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class':'item'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)

                    img = thumbnail.find('img')
                    thumb_url = URL(img.attrs.get('data-original',img.attrs.get('data-webp')), base_url=url)
                    label = img.attrs.get('alt')

                    # title_tag = thumbnail.find('span', {'class': 'card-t'})
                    # label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('div', {'class': 'duration'})
                    dur_time = '' if duration is None else collect_string_to_array(duration)[-1]

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
        # pretty(soup.find('div',{'class':'pagination-holder'}))
        return soup.find('div',{'class':'pagination'})

    # def parse_pagination(self, soup: BeautifulSoup, url: URL):
    #     container = self.get_pagination_container(soup)
    #     if not container:
    #         return
    #
    #     # pretty(container)
    #
    #     for page in _iter(container.find_all('a')):
    #         page_text = collect_string(page).strip()
    #         if not page_text:
    #             continue
    #
    #         pretty(page)
    #
    #         href=page.attrs.get('href')
    #
    #         if href == '#videos':
    #
    #             data_block_id = page.attrs.get('data-block-id')
    #             raw_params = page.attrs.get('data-parameters')
    #
    #             if not data_block_id or not raw_params:
    #                 continue
    #
    #             data_parameters = raw_params.replace(':', '=').replace(';', '&')
    #             timestamp = int(time.time() * 1000)
    #
    #             query = f'?mode=async&function=get_block&block_id={data_block_id}&{data_parameters}&_={timestamp}'
    #             page_url = URL(query, base_url=url)
    #
    #             self.add_page(page_text, page_url)
    #         else:
    #             self.add_page(page_text, URL(href, base_url=url))


    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'player'})
        if container:
            # pretty(container)
            self.set_video_get_from_yt_dlp()
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):

        container = soup.find('div', {'class': 'headline-items'})

        # pretty(container)
        if container:
            pretty(container)
            models_href_set = set()
            for item in _iter(container.find_all('a', href=lambda x: '/models/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                if href in models_href_set:
                    continue
                models_href_set.add(href)
                title = collect_string_to_array(item)[0]
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

        container=soup.find('div', {'id': 'tab_video_info'})

        # pretty(container)
        if container:
            pretty(container)
            models_href_set=set()
            for item in _iter(container.find_all('a', href=lambda x:'/models/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                if href in models_href_set:
                    continue
                models_href_set.add(href)
                title = collect_string_to_array(item)[0]
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/members/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')+'videos/'
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
        return self.title

if __name__ == "__main__":
    pass
