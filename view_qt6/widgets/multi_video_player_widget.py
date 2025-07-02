# -*- coding: utf-8 -*-
__author__ = 'Vit'
import os
import sys

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import  QMediaPlayer, QAudioOutput #,QMediaContent
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QWidget, QMenu, QFrame
from PyQt6.QtGui import QAction

import requests
import requests.exceptions

import vlc


from common.util import get_menu_handler, time_format
from data_format.url import URL
from common.setting import Setting

from view_qt6.qt_ui.ui_video_player_widget import Ui_VideoPlayerWidget
from view_qt6.widgets.playlist import Playlist

# class VideoWidget(QVideoWidget):
#     def mouseDoubleClickEvent(self, *args, **kwargs):
#         self.setFullScreen(not self.isFullScreen())

class BaseVideoWidget():
    def __init__(self):
        pass

    def set_on_position_changed_handler(self, handler:lambda pos, pos_str:None):
        self.on_position_changed = handler

    def set_on_duration_changed_handler(self, handler:lambda dur:None):
        self.on_duration_changed = handler

    def set_on_buffered_changed_handler(self, handler:lambda buf:None):
        self.on_buffered_changed = handler

class QtVideoWidget(QVideoWidget, BaseVideoWidget):
    def __init__(self, QWidget_parent=None):
        super().__init__(QWidget_parent)

        self.duration=0
        self.saved_position = None

        self.media_player = QMediaPlayer()
        self.audio_output= QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        self.media_player.setVideoOutput(self)

        self.media_player.durationChanged.connect(self.durationChanged)
        self.media_player.positionChanged.connect(self.positionChanged)
        self.media_player.errorOccurred.connect(self.handleError)
        self.media_player.bufferProgressChanged.connect(self.buffer_progress_changed)
        self.media_player.mediaStatusChanged.connect(self.media_status_changed)

    def setSource(self, url:str):
        # print('Playing:', url)
        self.url=url
        self.media_player.setSource(QUrl(url))

    def re_open(self, url:str):
        # print('Re-open',url)
        self.saved_position=self.media_player.position()
        # print(self.saved_position)
        # self.playlist.set_resolution(res,self.saved_position)
        self.setSource(url)
        self.media_player.play()

    def play(self):
        # print('QtVideoWidget..play')
        self.media_player.play()

    def stop(self):
        # print('QtVideoWidget..stop')
        self.media_player.stop()

    def pause(self):
        # print('QtVideoWidget..pause')
        self.media_player.pause()

    def setVolume(self,x:int):
        # print('QtVideoWidget..volume_changed',x)
        self.audio_output.setVolume(float(x)/100.0)

    def little_forward(self, second:int):
        # print('QtVideoWidget..little_forward',second)
        current_position=self.media_player.position()
        new_position=current_position + second*1000
        if new_position < self.duration:
            self.media_player.setPosition(new_position)
            # self.saved_position = new_position

    def set_position(self, position:int):
        # print('QtVideoWidget..set_position',position)
        # self.media_player.setPosition(position)
        self.saved_position=position

    def durationChanged(self, duration):
        self.on_duration_changed(duration)
        # self.ui.progress.setRange(0, duration)
        self.duration = duration

    def positionChanged(self, position):
        self.on_position_changed(position,time_format(position) + ' / ' + time_format(self.duration))
        # self.ui.progress.setValue(position)
        # self.ui.lb_time.setText(time_format(position) + ' / ' + time_format(self.duration))

    def mute(self, on:bool):
        # print('..mute')
        self.audio_output.setMuted(on)
        # self.ui.bn_mute.setChecked(on)

    def buffer_progress_changed(self,x:float):
        self.on_buffered_changed(int(100*x))

    def media_status_changed(self, media_status):
        if media_status == QMediaPlayer.MediaStatus.BufferedMedia:
            if self.saved_position:
                self.media_player.setPosition(self.saved_position)
                self.saved_position = None

    def handleError(self):
        print(self.media_player.error(), self.media_player.errorString())
        print("Error in " + self.url + ': ' + self.media_player.errorString())

    def mouseDoubleClickEvent(self, *args, **kwargs):

        self.setFullScreen(not self.isFullScreen())

class VlcVideoWidget(QFrame, BaseVideoWidget):
    __vlc_instance=None
    def __init__(self, QWidget_parent=None):
        super().__init__(QWidget_parent)

        # print('VlcVideoWidget..init start')
        self.duration=0
        self.saved_position = None
        self.busy=True

        # Создаем экземпляр VLC с параметрами логирования
        if VlcVideoWidget.__vlc_instance is None:
            VlcVideoWidget.__vlc_instance = vlc.Instance("--file-logging --logfile=vlc_log.txt --logmode=text --verbose=1")
        # self.instance = vlc.Instance()

        # Create an empty vlc media player
        self.media_player = VlcVideoWidget.__vlc_instance.media_player_new()
        self.media_player.audio_set_volume(10)
        self.media_player.video_set_mouse_input(False)

        self.media = None

        self.event=self.media_player.event_manager()
        self.event.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.positionChanged)
        self.event.event_attach(vlc.EventType.MediaPlayerPlaying, self.play_event)
        self.event.event_attach(vlc.EventType.MediaPlayerBuffering, self.buffering_event)
        self.event.event_attach(vlc.EventType.MediaStateChanged, self.handleError)

        # print('VlcVideoWidget..init done')

    def setSource(self, url:str):
        # print('VlcVideoWidget..setSource', url)
        self.url=url

        if self.media:
            self.media.release()
        else:
            self.media_player.set_hwnd(int(self.winId()))

        self.media = VlcVideoWidget.__vlc_instance.media_new(url)
        self.media_player.set_media(self.media)
        self.media.parse()

    def re_open(self, url:str):
        # print('VlcVideoWidget..Re-open',url)
        self.saved_position=self.media_player.get_position()
        self.setSource(url)
        self.media_player.play()
        self.media_player.set_position(self.saved_position)

    def play(self):
        # print('VlcVideoWidget..play')
        self.media_player.play()
        self.media_player.video_set_mouse_input(False)

    def stop(self):
        # print('VlcVideoWidget..stop')
        self.media_player.stop()

    def pause(self):
        # print('VlcVideoWidget..pause')
        self.media_player.set_pause(True)

    def setVolume(self,x:int):
        # print('VlcVideoWidget..volume_changed',x)
        self.media_player.audio_set_volume(x)

    def little_forward(self, second:int):
        # print('VlcVideoWidget..little_forward',second)
        current_position=self.media_player.get_position()
        new_position=current_position*self.duration + second*1000.0
        if new_position < self.duration:
            self.media_player.set_position(new_position/self.duration)

    def set_position(self, position:int):
        # print('VlcVideoWidget..set_position',position)
        # print(self.media_player.is_playing())
        # if self.busy:
        #     return
        # print('              ..set_position', position, position/self.duration, -self.media_player.get_position()+position/self.duration)

        # self.media_player.set_pause(True)
        self.media_player.set_position(position/self.duration)
        # self.media_player.play()
        # self.media_player.set_position(0.5)

    def play_event(self,e):
        # print('VlcVideoWidget..play_event', e)
        self.duration=self.media.get_duration()
        self.on_duration_changed(self.duration)

    def buffering_event(self,e):
        # print('VlcVideoWidget..buffering_event')
        self.busy= e.u.new_cache <90.0
        # print(e.u.new_cache, self.busy)
        self.on_buffered_changed(int(e.u.new_cache))

    def positionChanged(self, position):
        # print('VlcVideoWidget..positionChanged', position.u.new_position)
        pos=int(position.u.new_position*self.duration)
        self.on_position_changed(pos,time_format(pos) + ' / ' + time_format(int(self.duration)))

    def mute(self, on:bool):
        # print('VlcVideoWidget..mute', on)
        self.media_player.audio_set_mute(on)

    def handleError(self,e):
        # print(f"Произошла ошибка: {e.u.media_error}")
        # print(self.media_player.error(), self.media_player.errorString())
        print(e)
        print("Error in " + self.url + ': ' + e.u.media_error)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        print('mouseDoubleClickEvent')
        self.media_player.toggle_fullscreen()


class VideoPlayerWidget(QWidget):
    def __init__(self, QWidget_parent=None, Qt_WindowFlags_flags=0):
        QWidget.__init__(self, QWidget_parent)

        self.ui=Ui_VideoPlayerWidget()
        savecwd = os.getcwd()
        os.chdir('view_qt6/qt_ui')
        self.ui.setupUi(self)
        os.chdir(savecwd)

        self.ui.buffer.setMaximum(100)

        if Setting.use_vlc:
            self.player = VlcVideoWidget(self.ui.top_frame)
        else:
            self.player = QtVideoWidget(self.ui.top_frame)

        self.ui.top_frame_layout.addWidget(self.player)
        self.player.show()

        self.player.set_on_position_changed_handler(self.positionChanged)
        self.player.set_on_duration_changed_handler(self.durationChanged)
        self.player.set_on_buffered_changed_handler(self.buffer_progress_changed)

        self.ui.bn_play.clicked.connect(self.player.play)
        self.ui.bn_pause.clicked.connect(self.player.pause)
        self.ui.bn_stop.clicked.connect(self.stop)
        self.ui.bn_mute.clicked.connect(self.mute)
        # self.ui.progress.sliderMoved.connect(self.player.set_position)
        self.ui.progress.sliderMoved.connect(self.slider_moved)
        self.ui.progress.sliderReleased.connect(self.slider_released)

        self.ui.volume.valueChanged.connect(self.volume_changed)

    def slider_moved(self, e):
        # print('move..',e)
        # self.slider_value = e
        self.player.pause()

    def slider_released(self):
        # print('release at', self.ui.progress.value())
        self.player.set_position(self.ui.progress.value())
        self.player.play()

    def connect_to_playlist(self,playlist:Playlist):
        self.playlist=playlist

    def buffer_progress_changed(self,percent:int):
        self.ui.buffer.setValue(percent)

    def volume_changed(self,new_volume:int):
        # print('VideoPlayerWidget..volume_changed',new_volume)
        self.player.setVolume(new_volume)

    def re_open(self, res:int):
        self.player.re_open(self.playlist.get_stream(res))

    def set_url(self, url:str):
        # print('Playing:', url)
        self.url=url
        self.player.setSource(url)

    def init_quality_menu(self):
        self.menu = QMenu(self)
        self.ui.bn_quality.setMenu(self.menu)

    def add_quality_menu_item(self, item:str, no:int):
        # print('VideoPlayerWidget..Adding quality menu item:', item)
        menu_action = QAction(item, self, triggered=get_menu_handler(self.re_open,no))
        self.menu.addAction(menu_action)

    def media_status_changed(self, media_status):
        # if media_status == QMediaPlayer.MediaStatus.EndOfMedia:
        #     print(media_status)
        #     next=self.playlist.next_part()
        #     if next:
        #         self.media_player.setSource(QUrl(next))
        #         self.play()
        if media_status == QMediaPlayer.MediaStatus.BufferedMedia:
            if self.saved_position:
                self.media_player.setPosition(self.saved_position)
                self.saved_position = None

    def positionChanged(self, position, pos_in_str):
        self.ui.progress.setValue(position)
        self.ui.lb_time.setText(pos_in_str)

    def durationChanged(self, duration):
        self.ui.progress.setRange(0, duration)

    def little_forward(self, second:int):
        self.player.little_forward(second)

    def play(self):
        # print('VideoPlayerWidget..play')
        self.player.play()

    def stop(self):
        # print('VideoPlayerWidget..stop')
        self.player.stop()

    def pause(self):
        # print('VideoPlayerWidget..pause')
        self.player.pause()

    def set_volume(self, volume:int):
        # print('VideoPlayerWidget..set volume' ,volume)
        self.ui.volume.setValue(volume)
        self.volume_changed(volume)

    def get_volume(self)->int:
        return self.ui.volume.value()

    def mute(self, on:bool):
        # print('VideoPlayerWidget..mute')
        self.player.mute(on)
        self.ui.bn_mute.setChecked(on)

    def is_muted(self):
        return self.ui.bn_mute.isChecked()

    def destroy(self, bool_destroyWindow=True, bool_destroySubWindows=True):
        # self.media_player.deleteLater()
        super().destroy(bool_destroyWindow, bool_destroySubWindows)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        print('mouseDoubleClickEvent')
        # self.media_player.toggle_fullscreen()

if __name__ == "__main__":
    pass