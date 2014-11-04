__author__ = 'Cheaterman'

from kivy.core.window import Window
from kivy.clock import Clock



class KeyboardManager():
    def __init__(self):
        Window.bind(
            on_key_down=self.on_key_down,
            on_key_up=self.on_key_up,
        )
        self.callbacks = []
        self.pressed_keys = []

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if scancode and not scancode in self.pressed_keys:
            if len(self.pressed_keys) == 0:
                Clock.schedule_interval(self.on_key_repeat, .1)

            self.pressed_keys.append(scancode)
            self.process_callbacks(scancode=scancode)

    def on_key_up(self, window, codepoint, scancode):
        if scancode in self.pressed_keys:
            self.pressed_keys.remove(scancode)

            if len(self.pressed_keys) == 0:
                Clock.unschedule(self.on_key_repeat)

    def on_key_repeat(self, *args):
        for key in self.pressed_keys:
            self.process_callbacks(scancode=key)

    def process_callbacks(self, key=None, scancode=None, modifiers=[]):
        if scancode:
            for callback in self.callbacks:
                if not callback(self, key, scancode, modifiers):
                    return True

    def bind(self, callback):
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def unbind(self, callback):
        if callback in self.callbacks:
            self.callbacks.remove(callback)