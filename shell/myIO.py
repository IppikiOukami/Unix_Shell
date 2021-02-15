from os import read, write

def readLines():
    args = read(0,1000)
    if not args:
        return ''
    args = args.decode().split()
    return args
    
