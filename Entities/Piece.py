__author__ = 'Cheaterman'

from Layouts.SparseGridLayout import SparseGridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, InstructionGroup
from kivy.properties import ListProperty
from Entities.Block import Block
from Interfaces.TetrisAware import TetrisAware
from math import ceil, floor


class Piece(SparseGridLayout, TetrisAware):
    map = ListProperty([])

    def __init__(self, **kwargs):
        self.color = (1, 1, 1, 1)
        if 'color' in kwargs:
            self.color = kwargs['color']

        self.vertical = False

        super(SparseGridLayout, self).__init__(**kwargs)

        self.bind(map=self.on_map)

        self.keyboard = Window.request_keyboard(self.keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self.on_keypress)
        Clock.schedule_interval(self.update, .5)

    def on_map(self, instance, value):
        current_child = 0
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == 'x':
                    if len(self.children) < sum(line.count('x') for line in self.map):
                        self.add_widget(Block(coords=(x, y), color=self.color))
                    else:
                        self.children[current_child].coords = (x, y)
                        current_child += 1
        self.do_layout()

    def update(self, *args):
        if not self.parent:
            Clock.unschedule(self.update)
            return

        if self.tetris_coords[1] == 0 or self.collide_piece('down'):
            self.do_layout()
            self.remove_children()
            self.parent.check_line()
            self.parent.parent.spawn.new_piece()
            if self.parent:
                self.parent.remove_widget(self)
            self.keyboard_closed()
        else:
            self.tetris_coords[1] = self.tetris_coords[1] - 1

    def remove_children(self):
        for child in self.children[:]:
            child.pos_hint = {}
            self.remove_widget(child)
            self.parent.add_widget(child)

    def collide_piece(self, direction='down', map=[], coords=[]):
        if self.parent:
            for child in self.parent.children:
                if hasattr(child, 'tetris_coords') and child != self:
                    if direction == 'cw' or direction == 'ccw':
                        for y in range(len(map)):
                            for x in range(len(map[y])):
                                if map[y][x] == 'x':
                                    if coords[0] + x == child.tetris_coords[0]\
                                       and coords[1] + y == child.tetris_coords[1]:
                                            return True
                    else:
                        for own_child in self.children:
                            if direction == 'down':
                                if own_child.tetris_coords[1] - 1 == child.tetris_coords[1]\
                                   and own_child.tetris_coords[0] == child.tetris_coords[0]:
                                    return True
                            if direction == 'left':
                                if own_child.tetris_coords[0] - 1 == child.tetris_coords[0]\
                                   and own_child.tetris_coords[1] == child.tetris_coords[1]:
                                    return True
                            if direction == 'right':
                                if own_child.tetris_coords[0] + 1 == child.tetris_coords[0]\
                                   and own_child.tetris_coords[1] == child.tetris_coords[1]:
                                    return True
                            if direction == 'current':
                                if own_child.tetris_coords[0] == child.tetris_coords[0]\
                                   and own_child.tetris_coords[1] == child.tetris_coords[1]:
                                    return True

        return False

    def on_tetris_coords(self, *args):
        if hasattr(self, 'map') and self.parent:
            if self.tetris_coords[0] < 0:
                self.tetris_coords[0] = 0
            if self.tetris_coords[0] + len(self.map[0]) > self.parent.cols:
                self.tetris_coords[0] = self.parent.cols - len(self.map[0])
            if self.tetris_coords[1] < 0:
                self.tetris_coords[1] = 0
            if self.tetris_coords[1] + len(self.map) > self.parent.rows:
                self.tetris_coords[1] = self.parent.rows - len(self.map)

        if hasattr(self.parent, 'coord_to_pos'):
            self.pos = self.parent.coord_to_pos(*self.tetris_coords)

        for child in self.children:
            child.tetris_coords = [self.tetris_coords[0] + child.col, self.tetris_coords[1] + child.row]

    def do_layout(self, *args):
        super(Piece, self).do_layout(*args)

        if hasattr(self, 'outline'):
            self.canvas.before.remove(self.outline)

        self.outline = InstructionGroup()
        for child in self.children:
            self.outline.add(Color(.5, .8, 1, .8))
            self.outline.add(Rectangle(
                    size=(child.width + 4, child.height + 4),
                    pos=(child.x - 2, child.y - 2)
            ))

        if self.canvas.before:
            self.canvas.before.add(self.outline)

            if len(self.children) == 0:
                if hasattr(self, 'outline'):
                    self.canvas.before.remove(self.outline)

    def rotate(self, **kwargs):
        direction = 'ccw'
        if 'direction' in kwargs:
            direction = kwargs['direction']

        new_map = self.rotate_map(direction)
        new_coords = self.rotate_coords(new_map)

        if self.collide_piece(direction, new_map, new_coords):
            return

        self.vertical = not self.vertical

        self.map = new_map

        self.tetris_coords = new_coords

    def rotate_map(self, direction):
        new_map = zip(*self.map[::-1])
        if direction == 'cw':
            for i in range(2):
                new_map = zip(*new_map[::-1])

        return new_map

    def rotate_coords(self, new_map):
        map_diff = [
            len(self.map[0]) - len(new_map[0]),
            len(self.map) - len(new_map)
        ]

        for i in range(len(map_diff)):
            if self.vertical:
                map_diff[i] = floor(map_diff[i] / 2.)
            else:
                map_diff[i] = ceil(map_diff[i] / 2.)

        return self.tetris_coords[0] + map_diff[0], self.tetris_coords[1] + map_diff[1]

    def on_keypress(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'q':
            self.rotate(direction='ccw')
        elif keycode[1] == 'e':
            self.rotate(direction='cw')
        elif keycode[1] == 'a':
            if not self.collide_piece('left'):
                self.tetris_coords[0] -= 1
        elif keycode[1] == 'd':
            if not self.collide_piece('right'):
                self.tetris_coords[0] += 1
        elif keycode[1] == 's':
            if not self.collide_piece('down'):
                self.tetris_coords[1] -= 1
            self.update()
        else:
            return True

        return False

    def keyboard_closed(self):
        if self.keyboard:
            self.keyboard.unbind(on_key_down=self.on_keypress)
            self.keyboard = None

class ErrorPiece(Piece):
    def __init__(self, **kwargs):
        super(ErrorPiece, self).__init__(**kwargs)

        self.highlight = False

    def on_keypress(self, keyboard, keycode, text, modifiers):
        return True

    def do_layout(self, *args):
        super(ErrorPiece, self).do_layout(*args)
        self.update()

    def update(self, *args):
        if hasattr(self, 'outline'):
            self.canvas.before.remove(self.outline)

        self.outline = InstructionGroup()
        if self.highlight:
            for child in self.children[:]:
                self.outline.add(Color(1, .2, .2, .8))
                self.outline.add(Rectangle(
                        size=(child.width + 4, child.height + 4),
                        pos=(child.x - 2, child.y - 2)
                ))

            if self.canvas.before:
                self.canvas.before.add(self.outline)

            self.highlight = False
        else:
            self.canvas.before.remove(self.outline)

            self.highlight = True