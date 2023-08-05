'''This is the standard way to
   include a multiple-line comment in
   your code.
'''
def printitem(items, level):

    if isinstance(items, list):
        for item in items:
            printitem(item, level + 1)
    else:
        for tab in range(level):
            print('\t', end='')
        print(items)
        
