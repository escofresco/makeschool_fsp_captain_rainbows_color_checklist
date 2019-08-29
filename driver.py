

def special_print(checklist):
    pass

def display_instructions():
    print('Press A to add to list, R to remove, U to updated, and Q to quit')

def numerical_input_is_valid(idx, checklist):
    try:
        str(idx)
    except:
        return False
    finally:
        return True

def sanitize(input):
    if ord(input) in range(ord('A'), ord('z')):
        return input.upper()

def add(checklist):
    checklist.append(input('Add to list: '))

def remove(checklist):
    idx = input('Index of item to remove: ')
    if numerical_input_is_valid(idx, checklist):
        del checklist[idx]

def update():
    idx = input('Index of item to update: ')
    val = input('Value you\'d like to update this item to')
    if numerical_input_is_valid(idx, checklist):
        checklist[idx] = val

def main():
    key_function_map = {
        'A': add,
        'R': remove,
        'U': update,
    }
    checklist = list()
    while True:
        key = sanitize(input())
        if key == 'Q':
            break
        key_function_map[key](checklist)
        special_print(checklist)

# if __name__ == '__main__':
#     display_instructions()
#     main()
