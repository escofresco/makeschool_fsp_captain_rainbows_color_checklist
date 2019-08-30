
def display_instructions():
    print('Press A to add to list, R to remove, U to update, and Q to quit')

def numerical_input_is_valid(idx, checklist):
    try:
        int(idx)
    except:
        raise ValueError('')
    return int(idx) in range(len(checklist))

def sanitize(input):
    if ord(input) in range(ord('A'), ord('z')+1):
        return input.upper()

def add(checklist):
    latent_item = input('Add to list: ')
    if len(latent_item):
        checklist.append(latent_item)
    else:
        raise ValueError('That\'s not a valid input.')

def remove(checklist):
    idx = input('Index of item to remove: ')
    if numerical_input_is_valid(idx, checklist):
        del checklist[int(idx)]
    else:
        raise ValueError('That\'s not a valid input.')

def update(checklist):
    idx = input('Index of item to update: ')
    if numerical_input_is_valid(idx, checklist):
        val = input('Value you\'d like to update this item to')
        checklist[idx] = val
    else:
        raise ValueError('That\'s not a valid input.')

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
    key = ''
    while key != 'Q':
        key = sanitize(input())
        try:
            key_function_map[key](checklist)
        except ValueError as e:
            print(e)
        else:
            print(''.join(list(pretty_format(checklist))))
        finally:
            pass

if __name__ == '__main__':
    display_instructions()
    main()
