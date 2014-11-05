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
            Color(.5, .5, .5, .25)

            tile_size = self.parent.tile_size()
            for x in range(self.parent.cols):
                for y in range(self.parent.rows):
                    coords = [
                        self.parent.coord_to_pos(x, y, (0,            0)),
                        self.parent.coord_to_pos(x, y, (tile_size[0], 0)),
                        self.parent.coord_to_pos(x, y, (tile_size[0], tile_size[1])),
                        self.parent.coord_to_pos(x, y, (0,            tile_size[1]))
                    ]

                    for coord in coords[:]:
                        coords.remove(coord)
                        coords.append(coord[0])
                        coords.append(coord[1])

                    Line(
                        points=coords,
                        width=.25,
                        close=True
                    )