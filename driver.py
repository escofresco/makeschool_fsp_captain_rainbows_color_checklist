from sys import exit

def instructions():
    return 'Press A to add to list, R to remove, U to update, and Q to quit'

def index(idx, checklist):
    '''
    Takes a string as input. Raises exceptions if the string doesn't represent
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
                f'That index isn\'t valid for your checklist, \
                which has a length of {len(checklist)}'
            )

def sanitize(input):
    if len(input) == 1 and ord(input) in range(ord('A'), ord('z')+1):
        return input.upper()
    raise ValueError(f'That\'s not a valid key. \
                     Here\'s what you can enter: \n{instructions()}')

def strikethrough(i, checklist):
    '''
    Removes strikethrough if item at index i is marked complete, otherwise adds
    strikethrough.

    returns: str, the affected string at index i
    '''
    STRIKETHROUGH = '\u0336'
    if checklist[i]['is_complete']:
        return ''.join(checklist[i]['content'].split(STRIKETHROUGH))
    return STRIKETHROUGH.join(checklist[i]['content'])

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

def check_switch(checklist):
    try:
        idx = index(input('Index of item to check or uncheck: '), checklist)
    except (ValueError, IndexError) as e:
        raise e
    else:
        checklist[idx]['content'] = strikethrough(idx, checklist)
        checklist[idx]['is_complete'] ^= 1

def pretty_format(checklist):
    CHECKMARK = '\u2714'
    for i, elm in enumerate(checklist):
        yield f'{CHECKMARK if elm['is_complete'] else '':1} \
                {str(i):10} {elm['content']}\n'

def main():
    print(instructions())
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
        except ValueError as e:
            print(e)
        else:
            print(''.join(list(pretty_format(checklist))))

if __name__ == '__main__':
    main()
