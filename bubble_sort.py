from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock
import random

class Renderer(Window):
    def __init__(self):
        super().__init__(800, 600, "Bubble Sort Visualization")
        self.batch = Batch()
        self.x = list(range(1, 50))  # Unique heights for each bar
        random.shuffle(self.x)  # Shuffle the heights
        self.bars = []
        spacing = 15  # Adjust the spacing between bars

        for e, i in enumerate(self.x):
            self.bars.append(Rectangle(50 + e * spacing, 30, 10, i * 4, color=(255, 255, 255), batch=self.batch))  # White initially

        self.sorted = False
        self.i = 0
        self.j = 0

    def on_update(self, deltatime):
        if not self.sorted:
            if self.j < len(self.x) - self.i - 1:
                if self.x[self.j] > self.x[self.j + 1]:
                    self.x[self.j], self.x[self.j + 1] = self.x[self.j + 1], self.x[self.j]
                    self.update_bars()
                self.j += 1
            else:
                self.j = 0
                self.i += 1

            if self.i == len(self.x) - 1:
                self.sorted = True

    def update_bars(self):
        self.bars = []
        spacing = 15  # Adjust the spacing between bars
        for e, i in enumerate(self.x):
            # Set color based on sorting status
            if e >= len(self.x) - self.i - 1:
                color = (0, 255, 0)  # Green for sorted bars
            elif e >= len(self.x) - self.j - 1:
                color = (255, 255, 0)  # Yellow for currently sorting bars
            else:
                color = (255, 255, 255)  # White for unsorted bars
            self.bars.append(Rectangle(50 + e * spacing, 30, 10, i * 4, color=color, batch=self.batch))

    def on_draw(self):
        self.clear()
        self.batch.draw()

renderer = Renderer()
clock.schedule_interval(renderer.on_update, 0.2 / 1000.0)  
run()
