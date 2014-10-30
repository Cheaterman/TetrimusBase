__author__ = 'Cheaterman'

from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from Interfaces.GridAware import GridAware
from Entities.TetrisGrid import TetrisGrid
from Entities.Block import Block



class TetrisArea(FloatLayout, GridAware):
    grid = ObjectProperty(None)

    def check_line(self):
        y = 0
        while y < self.rows:
            found_children = 0
            for x in range(self.cols):
                for child in self.children:
                    if type(child) == Block and child.tetris_coords == [x, y]:
                        found_children += 1
            if found_children == self.cols:
                self.add_explosion(y)
                self.remove_line(y)
            else:
                y += 1

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

    def add_explosion(self, line):
        for child in self.children:
            if type(child) == Widget:
                line += 1

        explosion = Widget()
        with explosion.canvas:
            Color(1, 1, .5, .8)
            Rectangle(
                pos=self.coord_to_pos(0, line),
                size=(
                    self.tile_size()[0] * self.cols,
                    self.tile_size()[1]
                )
            )

        self.add_widget(explosion)

        def remove(self, widget):
            widget.parent.remove_widget(widget)

        anim = Animation(
            opacity=0,
            duration=.125
        )
        anim.bind(on_complete=remove)
        anim.start(explosion)

    def preview_update(self):
        pass