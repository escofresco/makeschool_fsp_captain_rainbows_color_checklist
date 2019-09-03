from display import Display
from getpass import getpass
from signal import (signal,
                    SIGWINCH)
from sys import (exit, stdout)


def cprint(string, display):
    display.print(str(string).strip())

def instructions():
    return 'Press A to add to list, R to remove, C to check/uncheck, U to update, and Q to quit'

def index(idx, checklist) -> int:
    '''
    Take a string as input. Raise exceptions if the string doesn't represent
    a valid index.
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

def sanitize(input) -> str:
    input = input.strip()
    if len(input) == 1 and ord(input) in range(ord('A'), ord('z')+1):
        return input.upper()
    raise ValueError(f'That\'s not a valid key.'
                     f'Here\'s what you can enter: \n{instructions()}')

def strikethrough(i, checklist) -> str:
    '''
    Remove strikethrough if item at index i is marked complete, otherwise add
    strikethrough.
    '''
    STRIKETHROUGH = '\u0336'
    if checklist[i]['is_complete']:
        return ''.join(checklist[i]['content'].split(STRIKETHROUGH))
    return STRIKETHROUGH.join(checklist[i]['content'])+STRIKETHROUGH

def create(checklist) -> None:
    latent_item = input('Add to list: ')
    if len(latent_item):
        checklist.append({
            'content': latent_item.strip(),
            'is_complete': False,
        })
    else:
        raise ValueError('That\'s not a valid input.')

def destroy(checklist) -> None:
    try:
        idx = index(input('Index of item to remove: '), checklist)
    except (ValueError, IndexError) as e:
        raise e
    else:
        del checklist[idx]

def update(checklist) -> None:
    try:
        idx = index(input('Index of item to update: '), checklist)
    except (ValueError, IndexError) as e:
        raise e
    else:
        val = input('Value you\'d like to update this item to: ')
        checklist[idx]['content'] = val

        # Temporarily xor is_complete to handle strikethrough for clean text
        checklist[idx]['is_complete'] ^= 1
        checklist[idx]['content'] = strikethrough(idx, checklist)
        checklist[idx]['is_complete'] ^= 1 # Reverse xor


def check_switch(checklist):
    '''
    Apply justified checkmark and strikethrough content if is_complete flag
    is False, otherwise remove checkmark and strikethrough
    '''
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

def display_header(checklist, display):
    cprint(instructions()+
          '\n'+
          (''.join(list(pretty_format(checklist)))),
          display)

def main():
    display = Display()

    # Add window resize listener
    # thanks @Atlantic777
    # https://docs.python.org/3/library/signal.html
    signal(SIGWINCH, display.resize_handler)

    display.clear()
    cprint(instructions(), display)
    key_function_map = {
        'A': create,
        'R': destroy,
        'U': update,
        'C': check_switch,
        'Q': lambda x: exit(),
    }
    checklist = list()
    while True:
        key = sanitize(input())
        # key = getpass(prompt="")
        try:
            key_function_map[key](checklist)
        except Exception as e:
            display.clear()
            display_header(checklist, display)
            cprint(e, display)
        else:
            display.clear()
            display_header(checklist, display)

if __name__ == '__main__':
    main()
