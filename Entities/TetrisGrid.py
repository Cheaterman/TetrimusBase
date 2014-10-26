__author__ = 'Cheaterman'

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle



class TetrisGrid(Widget):
    def __init__(self, **kwargs):
        super(TetrisGrid, self).__init__(**kwargs)
        self.bind(size=self.redraw)

    def redraw(self, *args):
        with self.canvas:
            for x in range(self.parent.cols):
                for y in range(self.parent.rows):
                    Color(1, .5, 0)
                    Rectangle(size=self.parent.tile_size(), pos=(self.parent.coord_to_pos(x, y)))
                    Color(0, 0, 0)
                    Rectangle(size=self.parent.tile_size((-2, -2)), pos=(self.parent.coord_to_pos(x, y, (1, 1))))