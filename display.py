class Display(object):
    def __init__(self, height, width, string=''):
        self.lines = [[' ' for _ in range(width)] for _ in range(height)]
        self.current_available_line = 0
        if len(string):
            self.print_string(string)

    def print_string(self, string):
        
