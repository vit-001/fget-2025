# -*- coding: utf-8 -*-
__author__ = 'Vit'
import os

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import  QMediaPlayer, QAudioOutput #,QMediaContent
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QWidget, QMenu
from PyQt6.QtGui import QAction

import requests
import requests.exceptions

from common.util import get_menu_handler
from data_format.url import URL

from view_qt6.qt_ui.ui_video_player_widget import Ui_VideoPlayerWidget
from view_qt6.widgets.playlist import Playlist

class VideoWidget(QVideoWidget):
    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.setFullScreen(not self.isFullScreen())

class VideoPlayerWidget(QWidget):
    def __init__(self, QWidget_parent=None, Qt_WindowFlags_flags=0):
        QWidget.__init__(self, QWidget_parent)

        self.ui=Ui_VideoPlayerWidget()
        savecwd = os.getcwd()
        os.chdir('view_qt6/qt_ui')
        self.ui.setupUi(self)
        os.chdir(savecwd)

        # self.playlist= None

        self.duration=0

        self.default=-1
        self.url=''
        self.saved_position=None

        self.ui.buffer.setMaximum(100)

        self.media_player = QMediaPlayer()#None, QMediaPlayer.VideoSurface)
        self.audio_output= QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        self.media_player_widget = VideoWidget(self.ui.top_frame)
        self.ui.top_frame_layout.addWidget(self.media_player_widget)
        self.media_player.setVideoOutput(self.media_player_widget)
        self.media_player_widget.show()

        # self.media_player.bufferProgressChanged.connect(lambda x:self.ui.buffer.setValue(x))
        self.media_player.bufferProgressChanged.connect(self.buffer_progress_changed)
        self.media_player.positionChanged.connect(self.positionChanged)
        self.media_player.durationChanged.connect(self.durationChanged)
        self.media_player.mediaStatusChanged.connect(self.media_status_changed)
        self.media_player.errorOccurred.connect(self.handleError)

        # self.ui.buffer.hide()

        self.ui.bn_play.clicked.connect(self.media_player.play)
        self.ui.bn_pause.clicked.connect(self.media_player.pause)
        self.ui.bn_stop.clicked.connect(self.stop)
        self.ui.bn_mute.clicked.connect(self.audio_output.setMuted)
        self.ui.progress.sliderMoved.connect(self.media_player.setPosition)
        self.ui.volume.valueChanged.connect(self.volume_changed)

    def connect_to_playlist(self,playlist:Playlist):
        self.playlist=playlist

    def buffer_progress_changed(self,x:float):
        # print(x)
        self.ui.buffer.setValue(int(100*x))

    def volume_changed(self,x:int):
        # print(x)
        self.audio_output.setVolume(float(x)/100.0)

    # def _set_url_list(self, list_of_dict:list, default:int):
    #     self.urls=list_of_dict
    #     self.default=default
    #     self.set_url(self.urls[self.default]['url'])
    #
    #     # menu = QMenu(self)
    #     # for item in self.urls:
    #     #     menu_action = QAction(item['text'], self, triggered=get_menu_handler(self.re_open,item['url']))
    #     #     menu.addAction(menu_action)
    #     # self.ui.bn_quality.setMenu(menu)

    def re_open(self, res:int):
        print('Re-open',res)
        self.saved_position=self.media_player.position()
        print(self.saved_position)
        self.playlist.set_resolution(res,self.saved_position)
        # self.set_url(url)
        self.media_player.play()

    def set_url(self, url:str):
        print('Playing:', url)
        self.url=url
        self.media_player.setSource(QUrl(url))

    def init_quality_menu(self):
        self.menu = QMenu(self)
        self.ui.bn_quality.setMenu(self.menu)

    def add_quality_menu_item(self, item:str, no:int):
        # print('Adding quality menu item:', item)
        menu_action = QAction(item, self, triggered=get_menu_handler(self.re_open,no))
        self.menu.addAction(menu_action)

    def media_status_changed(self, media_status):
        if media_status == QMediaPlayer.MediaStatus.EndOfMedia:
            print(media_status)
            next=self.playlist.next_part()
            if next:
                self.media_player.setSource(QUrl(next))
                self.play()
        if media_status == QMediaPlayer.MediaStatus.BufferedMedia:
            if self.saved_position:
                self.media_player.setPosition(self.saved_position)
                self.saved_position = None

    def positionChanged(self, position):
        def time_format(ms):
            dur = ms // 1000
            hours=dur // 3600
            minutes =  dur // 60 - hours*60
            secundes = dur - minutes * 60- hours*3600
            if hours==0:
                return '%2d:%02d' % (minutes, secundes)
            else:
                return '%d:%02d:%02d' % (hours, minutes, secundes)
        self.ui.progress.setValue(position)
        self.ui.lb_time.setText(time_format(position) + ' / ' + time_format(self.duration))

    def durationChanged(self, duration):
        self.ui.progress.setRange(0, duration)
        self.duration = duration

    def little_forward(self, second:int):
        current_position=self.media_player.position()
        new_position=current_position + second*1000
        if new_position < self.duration:
            self.media_player.setPosition(new_position)

    def play(self):
        print('..play')
        self.media_player.play()

    def stop(self):
        print('..stop')
        self.media_player.stop()

    def pause(self):
        print('..pause')
        self.media_player.pause()

    def set_volume(self, volume:int):
        print('..set volume')
        self.ui.volume.setValue(volume)
        self.volume_changed(volume)

    def get_volume(self)->int:
        return self.ui.volume.value()

    def mute(self, on:bool):
        print('..mute')
        self.audio_output.setMuted(on)
        self.ui.bn_mute.setChecked(on)

    def is_muted(self):
        return self.ui.bn_mute.isChecked()

    def set_error_handler(self, on_error=lambda error_text:None):
        print('..on error set', on_error)
        self.on_error=on_error

    def handleError(self):
        print(self.media_player.error(), self.media_player.errorString())
        print("Error in " + self.url + ': ' + self.media_player.errorString())
        # self.on_error("Error in " + self.url.link() + ': ' + self.media_player.errorString())
        # self.error_handler('Player error: ' + self.media_player.errorString())

    def destroy(self, bool_destroyWindow=True, bool_destroySubWindows=True):
        self.media_player.deleteLater()
        super().destroy(bool_destroyWindow, bool_destroySubWindows)


if __name__ == "__main__":
    pass