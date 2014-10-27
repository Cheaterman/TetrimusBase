__author__ = 'Cheaterman'

from kivy.uix.widget import Widget
from kivy.properties import ListProperty



class TetrisAware():
    tetris_coords = ListProperty([0, 0])

    def __init__(self, **kwargs):
        if 'tetris_coords' in kwargs:
            self.tetris_coords = list(kwargs['tetris_coords'])
        super(TetrisAware, self).__init__(**kwargs)