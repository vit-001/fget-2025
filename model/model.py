# -*- coding: utf-8 -*-
__author__ = 'Vit'

from bs4 import BeautifulSoup

from common.setting import Setting

from data_format.url import URL

from interface.loader_interface import LoaderInterface
from interface.model_interface import ModelFromControllerInterface, ModelFromSiteInterface
from interface.site_interface import SiteInterface
from interface.view_manager_interface import ViewManagerFromModelInterface

from model.favorites.favorites import Favorites

from model.history_model.hystory import HistoryModel

from model.loader.multiprocess_loader import MultiprocessLoader

from model.site.other.space import Space

from model.site.picture.tgp_sites.babesandbitches import BabesandbitchesSite
from model.site.picture.tgp_sites.bravoerotica import BravoeroticaSite
from model.site.picture.tgp_sites.teenport import TeenportSite
from model.site.picture.tgp_sites.tomorrowporn import TomorrowpornSite
from model.site.picture.tgp_sites.vibraporn import VibrapornSite

from model.site.video.plus_file.pornvibe import PornvibeSite
from model.site.video.plus_file.redtube import RedtubeSite
from model.site.video.plus_file.thepornfull import ThepornfullSite
from model.site.video.plus_file.mobifcuk import MobifcukSite
from model.site.video.plus_file.yourporn import YourpornSite

from model.site.video.simple.eblkn import EblknSite
# from model.site.video.plus_file.hitbdsm import HitbdsmSite

from model.site.video.script._nonwork.motherless import MotherlessSite
from model.site.video.script._nonwork.porntrex import PorntrexSite
from model.site.video.script.jizzbunker import JizzbunkerSite
from model.site.video.script.katestube import KatestubeSite
from model.site.video.script.pervclips import PervclipsSite
from model.site.video.script.pornicom import PornicomSite
from model.site.video.script.pornwatchers import PornwatchersSite
from model.site.video.script.pornwhite import PornwhiteSite
from model.site.video.script.shockingmovies import ShockingmoviesSite
from model.site.video.script.shooshtime import ShooshtimeSite
from model.site.video.script.sleazyneasy import SleazyneasySite
from model.site.video.script.vikiporn import VikipornSite
from model.site.video.script.xnxx import XnxxSite
from model.site.video.script.xvideo import XvideoSite
from model.site.video.script.xhand import XhandSite
from model.site.video.script.tryboobs import TryboobsSite
from model.site.video.script.tubous import TubousSite
from model.site.video.script.xtits import XtitsSite
# from model.site.video.script.porngem import PorngemSite
# from model.site.video.script.tubebunny import TubebunnySite
# from model.site.video.script.pornbimbo import PornbimboSite
from model.site.video.script.inxxx import InxxxSite
from model.site.video.script.prostoporno import ProstopornoSite
from model.site.video.script.pornobomba import PornobombaSite
from model.site.video.script.pornvideobb import PornvideobbSite
from model.site.video.script.analdin import AnaldinSite
from model.site.video.script.zatube import ZatubeSite
from model.site.video.script.pornhub import PornhubSite
from model.site.video.script.pornk import PornkSite
from model.site.video.script.brbz import BrbzSite

from model.site.video.simple.bravotube import BravotubeSite
from model.site.video.simple.freeuseporn import FreeusepornSite
from model.site.video.simple.gigporno import GigpornoSite
from model.site.video.simple.homeporno import HomepornoSite
from model.site.video.simple.pornoakt import PornoaktSite
from model.site.video.simple.pornxxxvideos import PornxxxvideosSite
from model.site.video.simple.rapelust import RapelustSite
from model.site.video.simple.ruleporn import RulepornSite
from model.site.video.simple.sextube_nl import SextubeNlSite
from model.site.video.simple.sickjunk import SickjunkSite
from model.site.video.simple.spreee import SpreeeSite
from model.site.video.simple.test import TestSite
from model.site.video.simple.iporntoo import IporntooSite
from model.site.video.simple.bdsmone import BdsmoneSite
from model.site.video.simple.crocotube import CrocotubeSite
from model.site.video.simple.fapguru import FapguruSite
from model.site.video.simple.freeporn import FreepornSite
from model.site.video.simple.hdporn import HdpornSite
from model.site.video.simple.pornpapa import PornpapaSite
from model.site.video.simple.sex3 import Sex3Site
from model.site.video.simple.sextubefun import SextubefunSite
from model.site.video.simple.stileproject import StileprojectSite
from model.site.video.simple.spicyflix import SpicyflixSite
from model.site.video.simple.xcum import XcumSite
from model.site.video.simple.trendyporn import TrendyPornSite
from model.site.video.simple.bingato import BingatoSite
from model.site.video.simple.ogporn import OgpornSite
from model.site.video.simple.vtrahe import VtraheSite
from model.site.video.simple.motherless import MotherlessSite
from model.site.video.simple.crazyshit import CrazyshitSite
from model.site.video.simple.bdsmstreak import BdsmstreakSite
from model.site.video.simple.strip2 import Strip2Site
from model.site.video.simple.cumlouder import CumlouderSite
from model.site.video.simple.incestflix import IncestflixSite
from model.site.video.simple.ajax_pagination.uppornx import UppornxSite
from model.site.video.simple.erothots import ErothotsSite
from model.site.video.simple.porus import PorusSite
from model.site.video.simple.spankbang import SpankbangSite
from model.site.video.simple.darknessporn import DarknesspornSite
from model.site.video.simple.fetishshrine import FetishshrineSite
from model.site.video.simple.rahaporn import RahapornSite
from model.site.video.simple.rahatupu import RahatupuSite
from model.site.video.simple.anysex import AnysexSite
from model.site.video.simple.ajax_pagination.pornone import PornoneSite

from model.site.video.tricky.mzansiporn import MzansipornSite

from model.site.video.yt_dlp.sosalkino import SosalkinoSite
from model.site.video.yt_dlp.ajax_pagination.huyamba import HuyambaSite
from model.site.video.yt_dlp.eporner import EpornerSite
from model.site.video.yt_dlp.xgroovy import XgroovySite
from model.site.video.yt_dlp.xhamster import XhamsterSite
from model.site.video.yt_dlp.ajax_pagination.xxxperevod import XxxperevodSite
from model.site.video.yt_dlp.ajax_pagination.pornopotok import PornopotokSite
from model.site.video.yt_dlp.embed_page.sosushka import SosushkaSite
from model.site.video.yt_dlp.xozilla import XozillaSite
from model.site.video.yt_dlp.ajax_pagination.porndr import PorndrSite
from model.site.video.yt_dlp.sunporno import SunpornoSite
from model.site.video.yt_dlp.ajax_pagination.two_porno import TwoPornoSite
from model.site.video.yt_dlp.ajax_pagination.tytporno import TytpornoSite
from model.site.video.yt_dlp.youjizz import YoujizzSite
from model.site.video.yt_dlp.kojka import KojkaSite
from model.site.video.yt_dlp.ajax_pagination.fapnow import FapnowSite
from model.site.video.yt_dlp.ajax_pagination.porngem import PorngemSite
from model.site.video.yt_dlp.ajax_pagination.ebony8 import Ebony8Site
from model.site.video.yt_dlp.whoreshub import WhoreshubSite

class Model(ModelFromControllerInterface, ModelFromSiteInterface):

    def __init__(self, view_manager:ViewManagerFromModelInterface):
        self._view_manager=view_manager
        self._loader=MultiprocessLoader()
        self._site_models=[
                            TestSite,
                            
                            Space('Classic:'),SosushkaSite,XhamsterSite,WhoreshubSite,PornoneSite,PornhubSite, XxxperevodSite,PornicomSite,PornxxxvideosSite,PorusSite,AnysexSite,YoujizzSite,AnaldinSite,SosalkinoSite, HuyambaSite,EpornerSite,XozillaSite,XgroovySite,SunpornoSite,
                            YourpornSite,PornopotokSite,FetishshrineSite, PorndrSite,BrbzSite,Ebony8Site,RahapornSite,RahatupuSite,MzansipornSite,KojkaSite,FapnowSite,PorngemSite,
                            GigpornoSite,EblknSite,VtraheSite,ProstopornoSite,MobifcukSite,TrendyPornSite,RedtubeSite,BingatoSite,XhandSite,UppornxSite,Strip2Site,PornobombaSite,
                            DarknesspornSite,PervclipsSite,SpankbangSite,TwoPornoSite,TytpornoSite,
                            InxxxSite,OgpornSite,XcumSite,VikipornSite,PornwhiteSite,RulepornSite,
                            SextubeNlSite,TubousSite,FreepornSite,PornpapaSite,ErothotsSite,PornkSite,


                            IncestflixSite,MotherlessSite,ShockingmoviesSite, BdsmstreakSite, CrazyshitSite, ZatubeSite,CumlouderSite,PornoaktSite,PornvideobbSite,XtitsSite,
                            BravotubeSite,CrocotubeSite, SleazyneasySite,ShooshtimeSite,XvideoSite,

                            Space('Blocked:'),
                            PorntrexSite,
                            SpreeeSite,

                            # XozillaSite,

                            # PornxpSite,

                            # PornmzSite,XhamsterSite,
                            Sex3Site,
                            SextubefunSite,
                            #TubebunnySite,
                            KatestubeSite,HdpornSite,
                            # TprnSite,
                            #PornbimboSite,
                           IporntooSite,

                            # ItsSite,DlouhaSite,
                            # FrprnSite,PorngemSite,PornwildSite,

                            # CrockotubeSite,YespornpleasexxxSite,
                            SickjunkSite,
                            # XdpornerSite,
                            PornvibeSite,XnxxSite,

                            JizzbunkerSite,
                            HomepornoSite,#PetardashdSite,


                            ThepornfullSite,


                            Space('Static:'),
                            TryboobsSite,SpicyflixSite,StileprojectSite, FapguruSite,PornwatchersSite,



                            # Space('Amateur:'),


                            Space('Deviant:'),
                            #HitbdsmSite, BoundhubSite,
                            BdsmoneSite,RapelustSite,FreeusepornSite,

                           # Space('Short:'),

                            Space('Photo:'),
                            BravoeroticaSite,TomorrowpornSite,TeenportSite,VibrapornSite,
                            BabesandbitchesSite,

                            Space('Non working:'),
                            # DarknesspornSite,RealGfSite,
                            # RusvideosSite, HdEasypornSite,PohubSite,PornozotSite,PornoaktSite,
                            #  PlusoneSite,
                            # CollectionofbestpornSite,
                            # PorngoSite,
                            # HotscopeSite,
                            # HeavyRSite,PornslandSite,V24videoSite,YourpornSite,TnaflixSite,SexixSite,
                            # PornhdSite,ThumbzillaSite,SpankwireSite,
                            # PornComSite,PornoxoSite,YoungPornVideosSite,
                            # DeviantclipSite,ExtremetubeSite,PervertslutSite,MotherlessSite,PornfunSite,PornbozzSite,
                            # Tube8Site,BeemtubeSite,PornoneSite,Porn0sexSite,
                            # Space('Blocked'),
                            # PorntrexSite,
                            # FapmeifyoucanSite,

                           ]

        self._thumb_history=HistoryModel('thumb', self._view_manager.on_thumb_history_changed)
        self._full_history=HistoryModel('full', self._view_manager.on_full_history_changed)
        self._favorites=Favorites(Setting.global_data_path+'favorites.json')

        n=0
        for site in self._site_models:
           n+=site.number_of_accepted_dimains()
        print('No of sites:',n)

        if Setting.parce_links_file:
            if Setting.parcer_for_links_file:
                parser=Setting.parcer_for_links_file
                # print('parce',parser.filename)
                new_urls=[]
                with open(parser.filename,'r', encoding="utf-8") as f:
                    bs=BeautifulSoup(f,'html.parser')
                    urls=parser.parce(bs)

                    for url in urls:
                        if not self.can_accept_url(url):
                            new_urls.append(url)
                            print(url)

                with open(parser.filename.rpartition('.')[0]+'.out' , 'w') as f1:
                    for url in new_urls:
                        f1.write(url.get()+'\n')

    def create_sites(self):
        for site_class in self._site_models:
            site_class.create_start_button(self.view_manager)


    def goto_url(self, url: URL, **options):
        site=self.can_accept_url(url)
        if site:
            site(self).goto_url(url, **options)
        else:
            print('Rejected', url)

    def add_to_favorites(self, url: URL, label:str=None):
        if label:
            self._favorites.add(label,url)
        else:
            site_class=self.can_accept_url(url)
            if site_class:
                label=site_class.get_thumb_label(url)
                self._favorites.add(label, url)

    def remove_favorite(self, url):
        print('Removing',url)
        self._favorites.remove(url)
        self._view_manager.refresh_thumb_view()

    def get_favorite_items(self, site: SiteInterface) -> list:
        return self._favorites.get_favorite_items(site)

    def can_accept_url(self, url: URL):
        for site_class in self._site_models:
            if site_class.can_accept_url(url):
                return site_class
        return None

    def on_cycle_handler(self):
        self._loader.on_update()
        self._view_manager.on_cycle_handler()

    def on_exit(self):
        self._loader.on_exit()
        self._favorites.on_exit()

    @property
    def view_manager(self) -> ViewManagerFromModelInterface:
        return self._view_manager

    @property
    def loader(self) -> LoaderInterface:
        return self._loader

    @property
    def full_history(self) -> HistoryModel:
        return self._full_history

    @property
    def thumb_history(self) -> HistoryModel:
        return self._thumb_history


if __name__ == "__main__":
    pass