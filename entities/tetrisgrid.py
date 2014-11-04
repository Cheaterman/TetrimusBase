__author__ = 'Cheaterman'

from kivy.uix.widget import Widget
from kivy.graphics import Color, Line



class TetrisGrid(Widget):
    def __init__(self, **kwargs):
        super(TetrisGrid, self).__init__(**kwargs)
        self.bind(size=self.redraw)

    def redraw(self, *args):
        with self.canvas:
            Color(1, .5, 0)
            Line(
                points=[
                    self.x - 1, self.top + 1,
                    self.x - 1, self.y - 1,
                    self.right + 1, self.y - 1,
                    self.right + 1, self.top + 1
                ],
                width=1.5
            )