__author__ = 'Cheaterman'

from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty
from kivy.animation import Animation



class BackgroundMusicAware(Screen):
    music_filename = StringProperty('')

    def __init__(self, **kwargs):
        super(BackgroundMusicAware, self).__init__(**kwargs)

        self.music = None

    def on_music_filename(self, *args):
        self.music = SoundLoader.load(self.music_filename)

        if self.music:
            self.music.loop = True
            self.music.volume = 0
            self.music.play()

    def on_pre_enter(self, *args):
        if self.music:
            anim = Animation(volume=1, d=.4)
            anim.start(self.music)

    def on_pre_leave(self, *args):
        if self.music:
            anim = Animation(volume=0, d=.4)
            anim.start(self.music)