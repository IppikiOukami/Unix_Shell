import os, sys, re

def runShell():
    os.environ['PS1'] = '$'                                                  #change PS1 to $
    print(os.environ['PS1'],end='')                                          #display to console
    usIn = readLine()                                                        #capture input
    args = usIn.split(" ")                                                   #split input on ' '
    if usIn == 'exit': sys.exit(0)                                           #exit on command
    rc = os.fork()                                                           #attempt fork()
    if rc < 0:                                                               #Failed fork
        os.write(2, ('Fork failed, returning {}\n'.format(rc)).encode())
        sys.exit(1)
    elif rc == 0:
        for dir in re.split(':',os.envrion['PATH']):
            program = '{}/{}'.format(dir,args[0])
            try: os.execve(program,args,os.environ)
            except FileNotFoundError: pass
        os.write(2, ('Child: Could not exec {}\n'.format(args[0]).encode()))
        sys.exit(1)
    else:                                                                    #Parent Process
        cPID = os.wait()
        os.write(1, ('Parent: Child {} terminated with exit code {}\n'
                     .format(cPID[0],cPID[1]).encode()))
        runShell()

raw = None
buf = ''

def readLine():
    global buf

    while True:
        line = getChar()
        if char == '': return ''
        if char == '\n':
            outLine, buf = buf, ''
            return outLine
        else: buf += char

def getChar():
    global raw, buf

    if not raw or not len(buf):
        raw = read(0,100)
        buf = raw.decode()
    if len(buf):
        outChar, buf = buf[0], buf[1:]
        return outChar
    else: return ''
                 
runShell()
