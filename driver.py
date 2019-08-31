import os
from signal import (signal,
                    SIGWINCH)
from sys import (exit, stdout)

ROY_G_BIV_TO_ANSI_MAP = {

}

ANSI_CODES = {
    'prefix': '\x1b',
    'reset': '\x1b[0m',
    **ROY_G_BIV_TO_ANSI_MAP
}

def resize_handler(signum, frame):
    print(shell_dims())

def cprint(string):
    #print(colored_string('asdf'))

def shell_dims():
    '''
    Get the dimensions of terminal.

    returns: (height, width)
    '''
    # thanks @brokkr
    # https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python
    return os.popen('stty size', 'r').read().split()

def colored_string(string, foreground='30', background='47'):
    # thanks @jonaszk
    # https://medium.com/@jonaszk/craft-a-progress-bar-in-python-ece63136958
    return (ANSI_CODES['prefix']+
            f'[1;{foreground};{background}m'+
            string.strip()+
            ANSI_CODES['reset'])

def instructions():
    return 'Press A to add to list, R to remove, C to check or uncheck, U to update, and Q to quit'

def index(idx, checklist):
    '''
    Take a string as input. Raises exceptions if the string doesn't represent
    a valid index.

    returns: int
    '''
    try:
        idx = int(idx)
    except:
        raise ValueError('Oh no! That\'s not an integer.')
    else:
        if idx in range(len(checklist)):
            return idx
        raise IndexError(
                f'That index isn\'t valid for your checklist, '
                f'which has a length of {len(checklist)}'
            )

def sanitize(input):
    input = input.strip()
    if len(input) == 1 and ord(input) in range(ord('A'), ord('z')+1):
        return input.upper()
    raise ValueError(f'That\'s not a valid key. \
                     Here\'s what you can enter: \n{instructions()}')

def strikethrough(i, checklist):
    '''
    Remove strikethrough if item at index i is marked complete, otherwise adds
    strikethrough.

    returns: str, the affected string at index i
    '''
    STRIKETHROUGH = '\u0336'
    if checklist[i]['is_complete']:
        return ''.join(checklist[i]['content'].split(STRIKETHROUGH))
    return STRIKETHROUGH.join(checklist[i]['content'])+STRIKETHROUGH

def add(checklist):
    latent_item = input('Add to list: ')
    if len(latent_item):
        checklist.append({
            'content': latent_item,
            'is_complete': False,
        })
    else:
        raise ValueError('That\'s not a valid input.')

def remove(checklist):
    try:
        idx = index(input('Index of item to remove: '), checklist)
    except (ValueError, IndexError) as e:
        raise e
    else:
        del checklist[idx]

def update(checklist):
    try:
        idx = index(input('Index of item to update: '), checklist)
    except (ValueError, IndexError) as e:
        raise e
    else:
        val = input('Value you\'d like to update this item to: ')
        checklist[idx]['content'] = val

        # Temporarily xor is_complete to handle strikethrough for clean text
        # that needs strikethrough
        checklist[idx]['is_complete'] ^= 1
        checklist[idx]['content'] = strikethrough(idx, checklist)
        checklist[idx]['is_complete'] ^= 1 # Reverse xor


def check_switch(checklist):
    try:
        idx = index(input('Index of item to check or uncheck: '), checklist)
    except (ValueError, IndexError) as e:
        raise e
    else:
        checklist[idx]['content'] = strikethrough(idx, checklist)
        checklist[idx]['is_complete'] ^= 1

def pretty_format(checklist):
    for i, elm in enumerate(checklist):
        CHECKMARK = '\u2714' if elm["is_complete"] else ''
        yield f'{CHECKMARK:1} {str(i):10} {elm["content"]}\n'

def clear_terminal():
    # thanks @poke
    # https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header(checklist):
    cprint(instructions()+
          '\n'+
          (''.join(list(pretty_format(checklist)))))

def main():

    # Add window resize listener
    # thanks @Atlantic777
    # https://docs.python.org/3/library/signal.html
    signal(SIGWINCH, resize_handler)

    clear_terminal()
    cprint(instructions())
    key_function_map = {
        'A': add,
        'R': remove,
        'U': update,
        'C': check_switch,
        'Q': lambda x: exit(),
    }
    checklist = list()
    while True:
        key = sanitize(input())
        try:
            key_function_map[key](checklist)
        except Exception as e:
            clear_terminal()
            display_header(checklist)
            cprint(e)
        else:
            clear_terminal()
            display_header(checklist)

if __name__ == '__main__':
    main()
