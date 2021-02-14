from os import read, write

rawLines = None
buffLines = ''

def readLines():
    global buffLines

    while True:
        char = getChar()
        if char == '': return ''
        if char == '\n':
            tempBuff,buffLines = buffLines,''
            return tempBuff
        else: buffLines += char
        
def getChar():
    global rawLines
    global buffLines

    if not rawLines or not len(buffLines):
        rawLines = read(0, 100)
        buffLines = rawLines.decode()

    if len(buffLines):
        tempChar, buffLines = buffLines[0], buffLines[1:]
        return tempChar
    else: return ''

def writeLine(line):
    write(1, line.encode())
