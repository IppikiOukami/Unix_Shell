from os import read, write
limit, index = 0,0

def readLines():
    global limit, index

    line = ""
    char = getChar()
    while char and char != "EOF": line, char = line + char, getChar()
    index, limit = 0,0
    return line

def getChar():
    global limit, index

    if index == limit:
        index = 0
        limit = read(0,1000)
        if limit == 0: return "EOF"
    if index < len(limit) - 1:
        char = chr(limit[index])
        index +=1
        return char
    else: return "EOF"
    
