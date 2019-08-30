
def instructions():
    return 'Press A to add to list, R to remove, U to update, and Q to quit'

def index(idx, checklist):
    '''
    Takes a string as input. Raises exceptions if that string doesn't represent
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
                f'That index isn\'t valid for your checklist, \
                which has a length of {len(checklist)}'
            )

def sanitize(input):
    if len(input) == 1 and ord(input) in range(ord('A'), ord('z')+1):
        return input.upper()
    raise ValueError(f'That\'s not a valid key. \
                     Here\'s what you can enter: \n{instructions()}')

def add(checklist):
    latent_item = input('Add to list: ')
    if len(latent_item):
        checklist.append(latent_item)
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
        checklist[idx] = val

def pretty_format(checklist):
    for i, elm in enumerate(checklist):
        yield f'{str(i):10} {elm}\n'

def main():
    key_function_map = {
        'A': add,
        'R': remove,
        'U': update,
    }
    checklist = list()
    key = sanitize(input())
    while key != 'Q':
        try:
            key_function_map[key](checklist)
        except ValueError as e:
            print(e)
        else:
            print(''.join(list(pretty_format(checklist))))
        finally:
            key = sanitize(input())

if __name__ == '__main__':
    print(instructions())
    main()
