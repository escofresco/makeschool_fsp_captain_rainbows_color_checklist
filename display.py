class Display(object):
    def __init__(self, height, width, string=''):
        self.ROY_G_BIV_TO_ANSI_MAP = {

        }
        self.ANSI_CODES = {
            'prefix': '\x1b',
            'reset': '\x1b[0m',
            **self.ROY_G_BIV_TO_ANSI_MAP
        }
        self.height = height
        self.width = width
        self.lines = self.initial_lines()
        self.next_available_line = 0
        if len(string):
            self.add_string(string)

    def initial_lines(self):
        return [[' ' for _ in range(width)] for _ in range(height)]

    def add_string(self, string):
        string = string.strip()
        for i,char in enumerate(string):
            col = i % self.width
            if (i+1) % self.width == 0 or char == '\n':
                self.next_available_line += 1
            else:
                self.lines[self.next_available_line][col] = char

    def render(self):
        for line in self.lines:
            print(colored_string(''.join(line)))

    def colored_string(string, foreground='30', background='47'):
        # thanks @jonaszk
        # https://medium.com/@jonaszk/craft-a-progress-bar-in-python-ece63136958
        return (self.ANSI_CODES['prefix']+
                f'[1;{foreground};{background}m'+
                string+
                self.ANSI_CODES['reset'])