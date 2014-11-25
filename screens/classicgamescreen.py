__author__ = 'Cheaterman'

from functools import partial
from interfaces import BackgroundMusicAware
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from entities import Block, TetrisArea, TetrisGrid, Piece, PreviewPiece, PieceSpawner
from widgets import BMLabel, LevelProgressBar



class ClassicGameScreen(BackgroundMusicAware):
    gamearea = ObjectProperty(None)
    block = ObjectProperty(None)
    spawn = ObjectProperty(None)

    counter = ListProperty((0, 0, 0, 0))

    score = NumericProperty(0)
    level = NumericProperty(0)

    level_progress = NumericProperty(0)

    def on_enter(self, *args):
        self.spawn.new_piece()
        Clock.schedule_interval(self.level_update, .1)

    def on_leave(self, *args):
        for child in self.gamearea.children[:]:
            if not isinstance(child, TetrisGrid)\
               and not isinstance(child, PreviewPiece)\
               and not isinstance(child, LevelProgressBar):
                self.gamearea.remove_widget(child)

        Clock.unschedule(self.restart)
        Clock.unschedule(self.level_update)

        self.counter = (0, 0, 0, 0)
        self.score = self.level = self.level_progress = 0

    def restart(self, *args):
        self.on_leave()
        self.on_enter()

    def game_lost(self):
        Clock.schedule_once(self.restart, 10)
        Clock.unschedule(self.level_update)

    def level_update(self, *args):
        self.level_progress += 1

        for bar in self.gamearea.progress:
            bar.progress = self.level_progress / 1000.