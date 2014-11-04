__author__ = 'Cheaterman'

from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from collections import deque
from interfaces import GridAware
from entities import TetrisGrid
from entities import Block



class TetrisArea(FloatLayout, GridAware):
    grid = ObjectProperty(None)
    preview1 = ObjectProperty(None)
    preview2 = ObjectProperty(None)
    preview3 = ObjectProperty(None)

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
        spawner = self.parent.spawn
        next = deque(spawner.next_pieces)
        pieces = [
            next.pop(),
            next.pop(),
            next.pop()
        ]
        previews = [
            self.preview1,
            self.preview2,
            self.preview3
        ]
        sizes = [
            1,
            .5,
            .25
        ]

        for i in range(len(previews)):
            current_map = spawner.pieces[pieces[i]]
            current_color = spawner.colors[pieces[i]]
            previews[i].color = (current_color.r, current_color.g, current_color.b, current_color.a)
            previews[i].shape = (len(current_map[0]), len(current_map))
            previews[i].size = (
                self.tile_size()[0] * len(current_map[0]) * sizes[i],
                self.tile_size()[1] * len(current_map) * sizes[i]
            )
            previews[i].map = current_map