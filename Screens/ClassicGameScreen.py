__author__ = 'Cheaterman'

from functools import partial
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from entities import Block
from entities import TetrisArea
from entities import TetrisGrid
from entities import Piece
from entities import PieceSpawner



class ClassicGameScreen(Screen):
    gamearea = ObjectProperty(None)
    block = ObjectProperty(None)
    spawn = ObjectProperty(None)

    def on_enter(self, *args):
        self.spawn.new_piece()

    def on_leave(self, *args):
        for child in self.gamearea.children[:]:
            if not isinstance(child, TetrisGrid):
                self.gamearea.remove_widget(child)

        Clock.unschedule(self.restart)

    def restart(self, *args):
        self.on_leave()
        self.on_enter()

    def game_lost(self):
        Clock.schedule_once(self.restart, 10)