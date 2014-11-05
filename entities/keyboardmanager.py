__author__ = 'Cheaterman'

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.event import EventDispatcher



class KeyboardManager(EventDispatcher):
    def __init__(self):
        self.attach_keyboard()

        self.register_event_type('on_key_down')
        self.register_event_type('on_key_up')

        self.pressed_keys = []

        self.repeat_delay = .2
        self.repeat_speed = .1

        self.keypress_breaks_repeat = True

    def attach_keyboard(self):
        Window.bind(
            on_key_down=self.hardware_key_down,
            on_key_up=self.hardware_key_up,
        )

    def on_key_down(self):
        pass

    def on_key_up(self, scancode):
        pass

    def is_pressed(self, scancode):
        for pressed_key, pressed_scancode, pressed_modifiers in self.pressed_keys:
            if pressed_scancode == scancode:
                return True

    def hardware_key_down(self, window, key, scancode, codepoint, modifiers):
        if scancode and not self.is_pressed(scancode):
            if self.keypress_breaks_repeat:
                Clock.unschedule(self.on_key_repeat)
                Clock.schedule_once(self.start_key_repeat, self.repeat_delay)
            elif len(self.pressed_keys) == 0:
                Clock.schedule_once(self.start_key_repeat, self.repeat_delay)

            self.pressed_keys.append([key, scancode, modifiers])
            self.dispatch('on_key_down', key, scancode, modifiers)

    def hardware_key_up(self, window, codepoint, scancode):
        if self.is_pressed(scancode):
            for pressed_key, pressed_scancode, pressed_modifiers in self.pressed_keys:
                if pressed_scancode == scancode:
                    self.pressed_keys.remove([pressed_key, pressed_scancode, pressed_modifiers])
                    break

            self.dispatch('on_key_up', scancode)

            if len(self.pressed_keys) == 0:
                Clock.unschedule(self.start_key_repeat)
                Clock.unschedule(self.on_key_repeat)

    def start_key_repeat(self, *args):
        Clock.schedule_interval(self.on_key_repeat, self.repeat_speed)

    def on_key_repeat(self, *args):
        for key, scancode, modifiers in self.pressed_keys:
            self.dispatch('on_key_down', key, scancode, modifiers)