from bs4 import BeautifulSoup
from data_format.url import URL
from common.util import pretty, _iter

class LinksFileParcer:
    def __init__(self):
        pass

    def parce(self, bs:BeautifulSoup)->list[URL]:
        return []

class PornDudeParcer(LinksFileParcer):
    def __init__(self, filename:str):
        super().__init__()
        self.filename = filename

    def parce(self, soup:BeautifulSoup)->list[URL]:
        print('Parcing ' + self.filename)
        sites=[]
        # pretty(soup)
        contents=soup.find('div', {'id':'related-sites'})
        # pretty(contents)
        if contents:
            # pretty(contents)
            for link in _iter(contents.find_all('a', {'data-site-link': True})):

                # pretty(link)
                sites.append(URL(link['data-site-link']))

                # xref=thumbnail.find('a',href=True)
                # img=thumbnail.find('img',src=True,alt=True)
                # href = URL(xref.attrs['href'], base_url=url)
                # img_url=img.attrs.get('src','')
                # thumb_url = URL(img_url, base_url=url)
                #
                # # title_tag = thumbnail.find('div', {'class': 'th-title'})
                # # title = thumbnail.find('strong', {'class': 'title'})
                # label=img.get('alt','')
                #
                # duration = thumbnail.find('div', {'class': 'ct-video-thumb-duration'})
                # dur_time = '' if duration is None else collect_string(duration)
                #
                # hd_tag = thumbnail.find('div', {'class': 'ct-video-thumb-hd-icon'})
                # hd = '' if hd_tag is None else 'HD'
                #
                # self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                #                labels=[{'text':dur_time, 'align':'top right'},
                #                        # {'text': count, 'align': 'top right'},
                #                        {'text':label, 'align':'bottom center'},
                #                        {'text': hd, 'align': 'top left'}
                #                ])

        print('Collected ' + str(len(sites)) + ' sites')

        return sites


