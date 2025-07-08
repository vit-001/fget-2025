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
        t = 'https://ok.xxx/get_file/13/63f3086f87736950ad29dff83e47755f/308000/308856/308856_720p.mp4/'
        referrer=URL('https://www.ebony8.com/videos/216847/horror-anal-team-fuck-with-ebony-hotty-marie-luv-marie-ebony/?utm_source=donnie')
        self.add_video('DEFAULT', URL(t, redirect=False, referer=referrer))

if __name__ == "__main__":
    pass