import os, sys, re

def runShell():
    os.environ['PS1'] = '$'
    print(os.environ['PS1'],end='')
    usIn = input()
    args = usIn.split(' ')
    if usIn == 'exit': sys.exit(1)
    rc = os.fork()
    if rc < 0:
        os.write(2, ('Fork failed, returning {}\n'.format(rc)).encode())
        sys.exit(1)
    elif rc == 0:
        for dir in re.split(':',os.environ['PATH']):
            program = '{}/{}'.format(dir,args[0])
            try: os.execve(program,args,os.environ)
            except FileNotFoundError: pass
        os.write(2, ('Child: Could not exec {}\n'.format(args[0]).encode()))
        sys.exit(1)
    else:
        cPID = os.wait()
        os.write(1, ('Parent: Child {} terminated with exit code {}\n'.format(cPID[0],cPID[1]).encode()))
        runShell()
                 
runShell()
