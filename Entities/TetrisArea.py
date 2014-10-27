
__author__ = 'Cheaterman'

from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.properties import ObjectProperty
from Interfaces.GridAware import GridAware
from Entities.TetrisGrid import TetrisGrid
from Entities.Block import Block



class TetrisArea(FloatLayout, GridAware):
    grid = ObjectProperty(None)

    def check_line(self):
        for y in range(self.rows):
            found_children = 0
            for x in range(self.cols):
                for child in self.children:
                    if type(child) == Block and child.tetris_coords == [x, y]:
                        found_children += 1
            if found_children == self.cols:
                self.remove_line(y)
                self.check_line()
                return

    def remove_line(self, line):
        for child in self.children[:]:
            if type(child) == Block:
                if child.tetris_coords[1] == line:
                    self.remove_widget(child)
                if child.tetris_coords[1] > line:
                    child.tetris_coords[1] -= 1
                    Animation.cancel_all(child, 'pos')
                    Animation(
                        pos=self.coord_to_pos(*child.tetris_coords),
                        duration=.25,
                        t='in_expo'
                    ).start(child)