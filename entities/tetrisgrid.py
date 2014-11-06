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

            Color(.5, .5, .5, .5)
            for x in range(self.parent.cols + 1):
                coords = self.parent.coord_to_pos(x, 0)
                Line(
                    points=[
                        coords[0], coords[1],
                        coords[0], coords[1] + self.parent.height
                    ],
                    width=.25
                )

            for y in range(self.parent.rows):
                coords = self.parent.coord_to_pos(0, y)
                Line(
                    points=[
                        coords[0], coords[1],
                        coords[0] + self.parent.width, coords[1]
                    ],
                    width=.25
                )