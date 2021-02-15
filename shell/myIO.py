from os import read, write

def readLines():
    args = read(0,1000)
    if not args:
        return ''
    args = args.decode().split()
    if not args: return ''
    for a in args:
        a = a.strip()
        a = a.strip('$_')
    while '\n' in args:
        args.remove('\n')
    for i in args:
        if i == '\n': args.remove('\n')
    return args
    
