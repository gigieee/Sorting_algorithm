from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock
import random

class Renderer(Window):
    def __init__(self):
        super().__init__(800, 600, "Merge Sort Algorithm")
        self.batch = Batch()
        self.x = list(range(1, 50))  # Unique heights for each bar
        random.shuffle(self.x)  # Shuffle the heights
        self.bars = []

        # Initialize bars with white color
        for e, i in enumerate(self.x):
            self.bars.append(Rectangle(50 + e * 15, 30, 10, i * 4, color=(255, 255, 255), batch=self.batch))

        self.animation_frames = self.generate_frames(self.x.copy())
        self.current_frame = None

    def generate_frames(self, arr):
        frames = []
        self.merge_sort_frames(arr, 0, len(arr), frames)
        return frames

    def merge_sort_frames(self, arr, start, end, frames):
        if end - start > 1:
            mid = (start + end) // 2
            self.merge_sort_frames(arr, start, mid, frames)
            self.merge_sort_frames(arr, mid, end, frames)

            merged_array = self.merge(arr[start:mid], arr[mid:end])
            frames.append((start, end, merged_array.copy()))

            for i in range(len(merged_array)):
                arr[start + i] = merged_array[i]

    def merge(self, left, right):
        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])

        return merged

    def on_update(self, deltatime):
        if self.animation_frames:
            start, end, merged_array = self.animation_frames.pop(0)
            self.x[start:end] = merged_array
            self.current_frame = (start, end)
            self.update_bars()

    def update_bars(self):
        self.bars = []
        for e, i in enumerate(self.x):
            # Set color based on sorting status
            if self.current_frame:
                start, end = self.current_frame
                if start <= e < end:
                    color = (255, 255, 0)  # Yellow for sorting
                elif e < end:
                    color = (255, 255, 255)  # White for unsorted
                else:
                    color = (0, 255, 0)  # Green for sorted
            else:
                color = (255, 255, 255)  # White if not sorting
            self.bars.append(Rectangle(50 + e * 15, 30, 10, i * 4, color=color, batch=self.batch))

    def on_draw(self):
        self.clear()
        self.batch.draw()

renderer = Renderer()
clock.schedule_interval(renderer.on_update, 0.5)
run()
