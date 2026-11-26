# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
# from common.util import _iter, quotes, pretty, psp, collect_string_to_array

import json

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class TestSite(BaseSiteParser):

    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('google.com')
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        view.add_start_button(picture_filename='model/site/resource/test.png',
                              url=URL("https://www.google.com"))

    def get_shrink_name(self):
        return 'TT'

    def parse_video(self, soup: BeautifulSoup, url: URL):
        t = 'https://fp.spac.me/htz-xfc10/htz-xcs12/v/021174201082243129109164247084091201131064170011000173018075/1791662400/18617504/x3/8d30eb069e36a0e6c5589939b42625b4/file.mp4'
        referrer=URL('')
        self.add_video('DEFAULT', URL(t, redirect=False, referer=referrer))

if __name__ == "__main__":
    pass