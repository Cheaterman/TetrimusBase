__author__ = 'Cheaterman'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color
from kivy.properties import NumericProperty
from collections import deque
import random
from Entities.Piece import Piece, ErrorPiece



class PieceSpawner(Widget):
    preview = NumericProperty(3)

    def __init__(self, **kwargs):
        super(PieceSpawner, self).__init__(**kwargs)
        self.pieces = [
            [
                ['x', 'x', 'x', 'x']
            ],
            [
                ['x', 'x', ' '],
                [' ', 'x', 'x']
            ],
            [
                [' ', 'x', 'x'],
                ['x', 'x', ' ']
            ],
            [
                ['x', ' ', ' '],
                ['x', 'x', 'x']
            ],
            [
                ['x', 'x', 'x'],
                ['x', ' ', ' ']
            ],
            [
                [' ', 'x', ' '],
                ['x', 'x', 'x']
            ],
            [
                ['x', 'x'],
                ['x', 'x']
            ],
        ]

        self.colors = []

        for i in range(0, 360, 30):
            self.colors.append(Color(i / 360., .5, 1, mode='hsv'))

        self.next_pieces = deque([])
        self.next_colors = deque([])

        self.bind(preview=self.on_preview)
        self.on_preview(self, self.preview)

    def on_preview(self, instance, value):
        while len(self.next_pieces) < self.preview:
            self.next_pieces.appendleft(random.randrange(len(self.pieces)))
            self.next_colors.appendleft(random.randrange(len(self.colors)))

    def new_piece(self):
        area = self.parent.gamearea
        current_piece = self.next_pieces.pop()
        current_color = self.next_colors.pop()
        self.on_preview(self, self.preview)

        map = self.pieces[current_piece]
        for i in range(random.randrange(4)):
            map = zip(*map[::-1])

        color = self.colors[current_color]
        tetris_coords = (area.cols / 2 - len(map[0]) / 2, area.rows - len(map))

        if not self.check_spawn(tetris_coords, map):
            piece = Piece()
        else:
            piece = ErrorPiece()

        piece.pos = area.coord_to_pos(*tetris_coords)
        piece.size_hint = (None, None)
        piece.color = (color.r, color.g, color.b, color.a)

        piece.height = len(map) * area.tile_size()[1]
        piece.width = len(map[0]) * area.tile_size()[0]

        piece.shape = (len(map[0]), len(map))
        piece.map = map

        area.add_widget(piece)
        piece.tetris_coords = tetris_coords

        if type(piece) == ErrorPiece:
            self.parent.game_lost()

    def check_spawn(self, tetris_coords, map):
        area = self.parent.gamearea
        piece = Piece()

        area.add_widget(piece)
        piece.map = map
        piece.tetris_coords = tetris_coords

        collides = piece.collide_piece('current')
        area.remove_widget(piece)

        return collides
