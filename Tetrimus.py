__author__ = 'Cheaterman'

from kivy.config import Config

Config.set('kivy', 'exit_on_escape', False)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 800)
Config.set('graphics', 'height', 600)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.app import App
from kivy.core.window import Window
from screens import TetrimusScreenManager
from entities import KeyboardManager



class TetrimusApp(App):
    def build(self):
        self.keyboard = KeyboardManager()

        return TetrimusScreenManager()

if __name__ == '__main__':
    TetrimusApp().run()