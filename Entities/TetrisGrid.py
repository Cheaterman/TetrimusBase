__author__ = 'Cheaterman'

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle



class TetrisGrid(Widget):
    def __init__(self, **kwargs):
        super(TetrisGrid, self).__init__(**kwargs)
        self.bind(size=self.redraw)

    def redraw(self, *args):
        with self.canvas:
            Color(1, .5, 0)
            Rectangle(size=self.size, pos=self.pos)
            Color(0, 0, 0)
            Rectangle(size=(self.width - 2, self.height - 2), pos=(self.x + 1, self.y + 1))