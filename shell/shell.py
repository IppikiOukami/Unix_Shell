import os, sys, re, myIO

# Needs to determine functionality for symbols within commands
def runShell():
    while True:                                                     #keep active prompt
        pid = os.getpid()
    
        os.environ['PS1'] = '$ '                                    #change PS1 to '$ '
        os.write(1,(os.environ['PS1']).encode())                       

        usIN = myIO.readLines().split()
        if usIN == '': os.write(2, 'No command given\n'.encode())
        elif 'cd' in usIN:
            if len(usIN) == 2:
                try: os.chdir(usIN[1])
                except: os.write(2, 'Invalid directory\n'.encode())
            elif len(usIN) == 1: os.chdir(os.environ['HOME'])
            else: os.write(2, 'Invalid command\n'.encode())
            
        elif 'exit' in usIN: sys.exit(0)                            #exit on Command
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
            os.open(args[args.index('>')+1], os.O_WRONLY | os.O_CREAT);
            os.set_inheritable(1, True)                             #Accesibility
            args = args[:args.index('>')]
            myExe(args)
            
        if '<' in args:# dest < source
            os.close(0)
            os.open(args[args.index('<')+1], os.O_RDONLY);          #Input file
            os.set_inheritable(0, True)
            args = args[:args.index('<')]
            myExe(args)
            
        if '|' in args:
            p1 = args[:args.index('|')]
            p2 = args[args.index('|')+1:]
            pIn,pOut = os.pipe()
            for f in (pIn,pOut): os.set_inheritable(f,True)

            rc = os.fork()
            if rc < 0:
                os.write(2, ("Fork Failed, returning {}\n".format(rc)).encode())
                sys.exit(1)
            elif rc == 0:
                os.close(pIn)
                os.dup(pOut)
                os.set_inheritable(1, True)
                for fd in (pIn, pOut): os.close(fd)
                myExe(p1)
            else:
                os.close(pOut)
                os.dup(pIn)
                os.set_inheritable(0, True)
                for fd in (pIn,pOut): os.close(fd)
                myExe(p2)
        else:
            myExe(args)
    else:                                                           #Parent process
        if not '&' in args:
            cPID = os.wait()
            os.write(1, ('Parent: Child {} terminated with exit code {}\n'.format(cPID[0],cPID[1])).encode())


runShell()
