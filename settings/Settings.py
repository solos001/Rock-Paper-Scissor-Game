WHITE = (255, 255, 255)
WIDTH, HEIGHT = 900, 500
FPS = 60


class Settings:

    def __init__(self):
        self.screen_width, self.screen_height = WIDTH, HEIGHT
        self.bg_color = WHITE
        self.fps = FPS

    def set_resolution(self, width, height):
        self.screen_width = width
        self.screen_height = height

    def set_fps(self, fps):
        self.fps = fps
     