__author__ = 'Cheaterman'

from kivy.uix.image import Image
from interfaces.tetrisaware import TetrisAware
from kivy.properties import ReferenceListProperty, NumericProperty



class Block(Image, TetrisAware):
    row = NumericProperty(0)
    col = NumericProperty(0)
    coords = ReferenceListProperty(col, row)