__author__ = 'Cheaterman'

from kivy.lang import Builder
from Screens import MenuScreen, ClassicGameScreen
from kivy.uix.screenmanager import ScreenManager
from Widgets.Button import OSButton



class TetrimusScreenManager(ScreenManager):
    def __init__(self):
        super(TetrimusScreenManager, self).__init__()
        self.add_widget(Builder.load_file('resources/views/Menu.kv'))
        self.add_widget(Builder.load_file('resources/views/ClassicGame.kv'))