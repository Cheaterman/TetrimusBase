__author__ = 'Cheaterman'

from kivy.uix.widget import Widget
from kivy.core.image import Texture
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.properties import NumericProperty



class LevelProgressBar(Widget):
    progress = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(LevelProgressBar, self).__init__(*args, **kwargs)

        texture = Texture.create(size=(1, 16))

        size = 1 * 16 * 3

        buf = [
            int(Color(
                .66 - (float(data) / size) * .66,
                .75,
                .75,
                mode='hsv'
            ).rgb[data % 3] * 255) for data in range(size)
        ]

        buf = b''.join(map(chr, buf))

        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

        self.progress_bar = Rectangle(texture=texture)
        self.progress_mask = Rectangle()

        group = InstructionGroup()
        group.add(Color(0, 0, 0))
        group.add(self.progress_mask)

        self.canvas.add(Color(1, 1, 1))
        self.canvas.add(self.progress_bar)
        self.canvas.add(group)

        self.bind(pos=self.redraw, size=self.redraw)

    def on_progress(self, *args):
        self.progress_mask.pos  = (self.x, self.y + self.height * self.progress)
        self.progress_mask.size = (self.width, self.height * (1 - self.progress))

    def redraw(self, *args):
        self.progress_bar.size = self.size
        self.progress_mask.size = self.size

        self.progress_bar.pos = self.pos
        self.progress_mask.pos = self.pos

        self.on_progress()