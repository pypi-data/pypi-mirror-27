'''This is the standard way to
   include a multiple-line comment in
   your code.
'''
'''
    将一个函数的必要参数变成可选的参数，需要为这个参数提供一个缺省值，如果没有提供参数值，就会使用这个缺省值，如果提供了参数值，则会使用这个值而不是缺省值，参数的缺省值使这个参数成为可选参数
'''
def printitem(items, level=0):
    
    if isinstance(items, list):
        for item in items:
            printitem(item, level+1)
    else:
        for tab in range(level):
            print('\t', end='')
        print(items)

def newprintitem(items, level=0):
    
    for item in items:
        if isinstance(item, list):
            printitem(item, level+1)
        else:
            for tab in range(level):
                print('\t', end='')
            print(item)
