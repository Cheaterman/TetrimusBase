__author__ = 'Cheaterman'

from kivy.uix.floatlayout import FloatLayout
from Entities.TetrisGrid import TetrisGrid
from Entities.Block import Block
from Interfaces.GridAware import GridAware
from kivy.properties import ObjectProperty



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

        self.checking_line = False

    def remove_line(self, line):
        for child in self.children[:]:
            if type(child) == Block:
                if child.tetris_coords[1] == line:
                    self.remove_widget(child)
                if child.tetris_coords[1] > line:
                    child.tetris_coords[1] -= 1
                    child.pos = self.coord_to_pos(*child.tetris_coords)