import os, sys, re
import myIO

# Needs to determine functionality for symbols within commands
def runShell():
    while True:                                                     #keep active prompt
        pid = os.getpid()
        if 'PS1' in os.environ: os.write(1, (os.eviron['PS1']).encode())
        else:
            os.write(1,('$ ').encode())                             #use PS1 if present
            
        usIN = myIO.readLines()                                     #delimit input by spacing
        if 'cd' in usIN:                                            #change dir command
            try: os.chdir(usIN[1])
            except FileNotFoundError: pass
            continue
        if 'exit' in usIN: sys.exit(0)                              #exit on Command
        if not usIN: pass
        else:
            runCommand(usIN,pid)                                    #attempt command
                    
def myExe(args):                                                    #attempt to exec
    for dir in re.split(':', os.environ["PATH"]):
        program = '{}/{}'.format(dir,args[0])
        try: os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass
    os.write(2,('{}: command not found'.format(args[0])).encode())  #notify user
    sys.exit(1)

def runCommand(args,pid=None):                                      #find command
    rc = os.fork()                                                  #attempt fork
    if rc < 0:                                                      #Failed fork
        os.write(2, ('Fork Failed, returning {}\n'.format(rc)).encode())
        sys.exit(1)
    elif rc == 0:                                                   #Child process
        if '>' in args:
            os.close(1)
            os.open(args[-1], os.O_CREAT | os.O_WRONLY);
            os.set_inheritable(1, True)
            argg = args[:args.index('>')]
            myExe(argg)
        if '<' in args:
            os.close(0)
            os.open(args[-1], os.O_RDONLY);
            os.set_inheritable(0, True)
            argg = args[:args.index('<')]
            myExe(argg)
        if '|' in args:
            p1 = args[:args.index('|')]
            p2 = args[args.index('|')+1:]
            pr,pw = os.pipe()
            for f in (pr,pw): os.set_inheritable(f,True)

            pf = os.fork()
            if pf < 0:
                os.write(2, ("Fork Failed, returning {}\n".format(pf)).encode())
                sys.exit(1)
            elif pf == 0:
                os.close(1)
                os.dup(pw)
                os.set_inheritable(1, True)
                for fd in (pw, pr): os.close(fd)
                myExe(p1)
            else:
                os.close(0)
                os.dup(pr)
                os.set_inheritable(0, True)
                for fd in (pw,pr): os.close(fd)
                myExe(p2)
        else:
            myExe(args)
    else:                                                           #Parent process
        if not '&' in args:
            cPID = os.wait()
            os.write(1, ('Parent: Child {} terminated with exit code {}\n'.format(cPID[0],cPID[1])).encode())


runShell()
