__author__ = 'Cheaterman'

from kivy.uix.button import Button



class OSButton(Button):
    def on_touch_up(self, touch):
        if(self.collide_point(*touch.pos)):
            super(OSButton, self).on_touch_up(touch)
        else:
            self.state = 'normal'