class Display(object):
    def __init__(self, height, width):
        self.lines = [[' ' for _ in range(width)] for _ in range(height)]
