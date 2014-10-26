__author__ = 'Cheaterman'

from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget



class GridAware(Widget):
    rows = NumericProperty(1)
    cols = NumericProperty(1)
    shape = ReferenceListProperty(cols, rows)

    def tile_size(self, offset=(0, 0)):
        return self.width / self.cols + offset[0], self.height / self.rows + offset[1]

    def coord_to_pos(self, x, y, offset=(0, 0)):
        return self.x + offset[0] + self.width / self.cols * x, self.y + offset[1] + self.height / self.rows * y