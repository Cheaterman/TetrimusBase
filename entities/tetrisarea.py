__author__ = 'Cheaterman'

from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup
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

    def __init__(self, **kwargs):
        super(TetrisArea, self).__init__(**kwargs)

        self.currently_exploding = 0

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

        if self.currently_exploding:
            self.parent.counter[self.currently_exploding - 1] += 1
            score_increase = self.currently_exploding ** 2 * 100
            self.parent.score += score_increase * (self.parent.level if self.parent.level > 0 else 1)

            self.parent.level_progress += score_increase

        if self.parent.level_progress >= 1000:
            self.parent.level += 1
            self.parent.level_progress = 0

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
        line += self.currently_exploding
        self.currently_exploding += 1

        explosion = InstructionGroup()
        color = Color(1, 1, .5, .8)

        explosion.add(color)

        explosion.add(Rectangle(
            pos=self.coord_to_pos(0, line),
            size=(
                self.tile_size()[0] * self.cols,
                self.tile_size()[1]
            )
        ))

        self.canvas.add(explosion)

        def remove(self):
            self.canvas.remove(explosion)
            self.currently_exploding -= 1

        anim = Animation(
            a=0,
            duration=.125
        )
        anim.bind(on_complete=lambda *args: remove(self))
        anim.start(color)

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