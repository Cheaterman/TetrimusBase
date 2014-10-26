__author__ = 'Cheaterman'

from kivy.uix.floatlayout import FloatLayout
from Entities.TetrisGrid import TetrisGrid
from kivy.properties import ObjectProperty
from Interfaces.GridAware import GridAware



class TetrisArea(FloatLayout, GridAware):
    grid = ObjectProperty(None)

    def on_children(self, *args):
        for y in range(self.rows):
            for x in range(self.cols):
                pass