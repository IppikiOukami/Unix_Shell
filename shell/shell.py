import os
import sys
from IOFunctions import readLine, writeLine

def main():
    while True:
        writeLine('$: ')
        inputLine = readLine()
        if inputLine == 'exit': break
        if len(inputLine) == 0 or inputLine[0] == ' ': continue

        args = inputLine.split(' ')
        rc = os.fork()

        if rc < 0: writeLine('Fork Failed')
        elif rc == 0:
            runCommand(args)
            sys.exit(0)
        else: os.wait()

def runCommand(args):
    dirs = os.environ['PATH']

    for dir in dirs.split(':'):
        program = "{}/{}".format(dir, args[0])
        try:
            os.execve(program, args, os.environ)
        except OSError:
            pass
    writeLine('Unrecognized Command\n')

if __name__ == '__main__':
    main()
