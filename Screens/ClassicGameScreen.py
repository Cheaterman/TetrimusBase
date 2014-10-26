__author__ = 'Cheaterman'

from functools import partial
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.properties import ObjectProperty
from Entities.Block import Block
from Entities.TetrisArea import TetrisArea
from Entities.TetrisGrid import TetrisGrid
from Entities.Piece import Piece
from Entities.PieceSpawner import PieceSpawner



class ClassicGameScreen(Screen):
    gamearea = ObjectProperty(None)
    block = ObjectProperty(None)
    spawn = ObjectProperty(None)

    def on_leave(self, *args):
        for child in self.gamearea.children[:]:
            if not isinstance(child, TetrisGrid):
                self.gamearea.remove_widget(child)