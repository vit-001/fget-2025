__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.parser import BaseSiteParser

class HuyambaSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('huyamba.mobi/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict()
        view.add_start_button(picture_filename='model/site/resource/huyamba.svg',
                              menu_items=menu_items,
                              url=URL("https://retro.huyamba.mobi/videos/"))

    def get_shrink_name(self):
        return 'HM'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'main-flex'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class':'item'})):
                try:
                    # pretty(thumbnail)

                    xref = thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)

                    img = thumbnail.find('img')
                    thumb_url = URL(img.attrs.get('data-original'), base_url=url)
                    label = img.attrs.get('alt')

                    # title_tag = thumbnail.find('a', {'class': 'video-item-title'})
                    # label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('div', {'class': 'box'})
                    dur_time = '' if duration is None else collect_string(duration.string).strip()

                    hd_tag = thumbnail.find('div', {'class': 'box second'})
                    hd = '' if hd_tag is None else collect_string(hd_tag).strip()

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
        return soup.find('div',{'class':'pagination-list'})


    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            req_base=url.get().split('?mode=')[0]
            print(req_base)
            for page in _iter(container.find_all('a', {'href': True})):
                if page.string and str(page.string).strip().isdigit():
                    if page.attrs.get('data-action') == 'ajax':
                        data_block_id = page.attrs.get('data-block-id')
                        data_parameters = page.attrs.get('data-parameters').replace(':','=').replace(';','&')

                        req_addr = req_base + '?mode=async&function=get_block&block_id={0}&{1}'.format(
                            data_block_id, data_parameters)
                        self.add_page(str(page.string).strip(), URL(req_addr))
                    else:
                        self.add_page(str(page.string).strip(), URL(page.attrs['href'], base_url=url))
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'player'})
        if container:
            # pretty(container)
            self.set_video_get_from_yt_dlp()
            self.set_default_video(-1)
            self.redirect=True

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'player-tools'})

        # pretty(container)
        if container:
            pretty(container)
            for item in _iter(container.find_all('a', class_='author', href=lambda x:'/models/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')+'videos/'
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/categories/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')+'videos/'
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url))

            for item in _iter(container.find_all('a', href=lambda x:'/tags/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')+'videos/'
                title = item.attrs.get('title', collect_string(item))
                self.add_tag(title, URL(href, base_url=url), style=dict(color='gray'))


    # def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
    #     return self.title.partition('- ')[-1][:50]

if __name__ == "__main__":
    pass
