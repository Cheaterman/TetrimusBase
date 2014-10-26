__author__ = 'Cheaterman'

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ReferenceListProperty
from Interfaces.GridAware import GridAware



class SparseGridLayout(FloatLayout, GridAware):
    def do_layout(self, *args):
        size_hint = (1. / self.cols, 1. / self.rows)

        for child in self.children:
            child.size_hint = (None, None)
            child.size = self.tile_size()

            if hasattr(child, 'coords'):
                child.col = child.coords[0]
                child.row = child.coords[1]
            if not hasattr(child, 'row'):
                child.row = 0
            if not hasattr(child, 'col'):
                child.col = 0

            child.pos_hint = {'x': size_hint[0] * child.col,
                              'y': size_hint[1] * child.row}
        super(SparseGridLayout, self).do_layout(*args)