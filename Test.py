__author__ = 'Cheaterman'

from functools import partial
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.animation import Animation



kv = """
<TestWidget>:
    block: block
    Button:
        text: 'Move the square around'
        on_release: root.move_block()

        center: root.center
        width: root.width / 3

    Widget:
        id: block

        size: (50, 50)
        center_x: root.width / 4
        center_y: root.height * 3 / 4

        canvas:
            Color:
                rgb: 0.5, 1, 0.5

            Rectangle:
                pos: self.pos
                size: self.size
"""

Builder.load_string(kv)

class TestWidget(Widget):
    block = ObjectProperty(None)

    def on_block(self, widget, block):
        def on_block_pos(self, block, pos):
            self.block_coords = [
                (self.width / 4, self.height / 2),
                (self.width / 2, self.height / 4),
                (self.width * 3 / 4, self.height / 2),
                (self.width / 3, self.height * 3 / 4)
            ]
        self.current_coord_idx = 0
        block.bind(pos=partial(on_block_pos, self))

    def move_block(self):
        Animation.cancel_all(self.block)
        Animation(pos=(self.block_coords[self.current_coord_idx])).start(self.block)
        self.current_coord_idx += 1
        if self.current_coord_idx == len(self.block_coords):
            self.current_coord_idx = 0

class TestApp(App):
    def build(self):
        return TestWidget()



if __name__ == '__main__':
    TestApp().run()