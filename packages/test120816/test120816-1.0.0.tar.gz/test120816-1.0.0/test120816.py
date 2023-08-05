'''This is the standard way to
   include a multiple-line comment in
   your code.
'''
def printitem(items):

    if isinstance(items, list):
        for item in items:
            printitem(item)
    else:
        print(items)

        
