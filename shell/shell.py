import os, sys, re

def runShell():
    while True:                                                     #keep active prompt
        pid = os.getpid()
        if 'PS1' in os.environ: os.write(1, (os.eviron['PS1']).encode())
        else:
            os.write(1,('$ ').encode())                             #use PS1 if present
            
        usIN = input()                                              #get input
        usIN = usIN.split(' ')                                      #delimit input by spacing

        if 'cd' in usIN:                                            #change dir command
            try: os.chdir(usIN[1])
            except FileNotFoundError: pass
            continue
        if 'exit' in usIN: sys.exit(0)                              #exit on command

        if not usIN: pass                                           #try getting input again
        else: runCommand(usIN,pid)                                  #inspect input
                    
def myExe(args):                                                    #attempt to exec
    for dir in re.split(':', os.environ["PATH"]):
        program = '{}/{}'.format(dir,args[0])
        try: os.execve(program, args, os.environ)
        except FileNotFoundError: pass                              #quiet fail
    os.write(2,('{}: command not found'.format(args[0])).encode())  #notify user
    sys.exit(1)

def runCommand(args,pid=None):                                      #find command
    rc = os.fork()                                                  #attempt fork
    if rc < 0:                                                      #Failed fork
        os.write(2, ('Fork Failed, returning {}\n'.format(rc)).encode())
        sys.exit(1)
    elif rc == 0:                                                   #Child process
        myExe(args)
    else:                                                           #Parent process
        if not '&' in args:
            cPID = os.wait()
            os.write(1, ('Parent: Child {} terminated with exit code {}\n'.format(cPID[0],cPID[1])).encode())


runShell()
