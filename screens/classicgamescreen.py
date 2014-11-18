__author__ = 'Cheaterman'

from functools import partial
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from entities import Block, TetrisArea, TetrisGrid, Piece, PreviewPiece, PieceSpawner
from widgets import BMLabel



class ClassicGameScreen(Screen):
    gamearea = ObjectProperty(None)
    block = ObjectProperty(None)
    spawn = ObjectProperty(None)

    counter = ListProperty((0, 0, 0, 0))

    score = NumericProperty(0)
    level = NumericProperty(0)

    def on_enter(self, *args):
        self.spawn.new_piece()

    def on_leave(self, *args):
        for child in self.gamearea.children[:]:
            if not isinstance(child, TetrisGrid)\
               and not isinstance(child, PreviewPiece):
                self.gamearea.remove_widget(child)

        Clock.unschedule(self.restart)

    def restart(self, *args):
        self.on_leave()
        self.on_enter()

    def game_lost(self):
        Clock.schedule_once(self.restart, 10)