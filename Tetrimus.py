__author__ = 'Cheaterman'

from kivy.config import Config

Config.set('kivy', 'exit_on_escape', False)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 800)
Config.set('graphics', 'height', 600)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.app import App
from kivy.core.window import Window
from Screens.TetrimusScreenManager import TetrimusScreenManager



class TetrimusApp(App):
    def build(self):
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self.on_keypress)
        return TetrimusScreenManager()

    def keyboard_closed(self):
        if self.keyboard:
            self.keyboard.unbind(on_key_down=self.on_keypress)
            self.keyboard = None

    def on_keypress(self, keyboard, keycode, text, modifiers):
        return True



if __name__ == '__main__':
    TetrimusApp().run()