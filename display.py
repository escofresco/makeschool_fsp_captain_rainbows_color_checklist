from copy import deepcopy
import os
from typing import List

class Display(object):

    STRIKETHROUGH = '\u0336'

    def __init__(self, string=''):
        self.ROY_G_BIV_TO_ANSI_MAP = {
            # ISO 6429 compliant

        }
        self.ANSI_CODES = {
            'prefix': '\x1b',
            'reset': '\x1b[0m',
            **self.ROY_G_BIV_TO_ANSI_MAP
        }
        self.height, self.width = self.shell_dims()
        self.clear()
        self.add_string(string)

    @staticmethod
    def reshape_matrix(matrix: List[list],
                       target_width: int,
                       target_height: int) -> List[list]:
        '''
        Resize a matrix to fit given dimensions.

        6x2 -> 3x3
        [[' ', 'H', 'e', 'l', 'l', 'o'],            [[' ', 'H', 'e'],
         [' ', 'W', 'o', 'r', 'l', 'd']]    -->      ['l', 'l', 'o'],
                                                     [' ', 'W', 'o']]
        '''
        target_matrix = Display.empty_matrix(target_width, target_height)
        cur_target_row = 0
        for init_row in range(len(matrix)):
            cur_target_col = 0
            for init_col in range(len(matrix[init_row])):
                if cur_target_col >= target_width:
                    # Emulate a carriage return
                    cur_target_row += 1
                    cur_target_col = 0
                if cur_target_row >= target_height:
                    # Truncate: there's no more room to transfer information
                    return target_matrix
                (target_matrix
                 [cur_target_row]
                 [cur_target_col]) = matrix[init_row][init_col]
                cur_target_col += 1
            cur_target_row += 1
        return target_matrix

    @staticmethod
    def empty_matrix(width: int, height: int) -> List[list]:
        return [[' ' for _ in range(width)]
                for _ in range(height)]

    def initialize_lines(self):
        self.lines = Display.empty_matrix(self.width, self.height)
        self.next_available_line = 0

    def add_string(self, string: str) -> None:
        self.next_available_line += 1
        col = 0
        for i,char in enumerate(string):
            if (col+1) % self.width == 0 or char == '\n':
                self.next_available_line += 1
                col = 0
            elif char == Display.STRIKETHROUGH:
                if col != 0:
                    self.lines[self.next_available_line][col-1] += char
            else:
                self.lines[self.next_available_line][col] = char
                col += 1

    def render(self) -> None:
        for line in self.lines:
            print(self.colored_string(''.join(line)))

    def resize(self, width: int, height: int) -> None:
        self.lines = Display.reshape_matrix(self.lines, width, height)
        self.render()

    def clear(self) -> None:
        # thanks @poke
        # https://stackoverflow.com/questions/2084508/clear-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')

        self.initialize_lines()
        self.render()

    def print(self, string: str) -> None:
        self.add_string(string)
        self.render()

    def colored_string(self,
                       string: str,
                       foreground='30',
                       background='47') -> str:
        # thanks @jonaszk
        # https://medium.com/@jonaszk/craft-a-progress-bar-in-python-ece63136958
        return (self.ANSI_CODES['prefix']+
                f'[1;{foreground};{background}m'+
                string+
                self.ANSI_CODES['reset'])

    def shell_dims(self) -> map:
        '''
        Get the dimensions of terminal.

        returns: (height, width)
        '''
        # partial thanks @brokkr
        # https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python
        return map(int, os.popen('stty size', 'r').read().split())

    def resize_handler(self, signum, frame) -> None:
        self.resize(*list(self.shell_dims())[::-1])
