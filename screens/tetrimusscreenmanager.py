__author__ = 'Cheaterman'

from kivy.lang import Builder
from screens import MenuScreen, ClassicGameScreen
from kivy.uix.screenmanager import ScreenManager
from widgets import OSButton



class TetrimusScreenManager(ScreenManager):
    def __init__(self):
        super(TetrimusScreenManager, self).__init__()

        self.add_widget(Builder.load_file('resources/views/menu.kv'))
        self.add_widget(Builder.load_file('resources/views/classicgame.kv'))