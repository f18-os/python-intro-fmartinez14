#! /usr/bin/env python3

import os, sys, time, re


pid = os.getpid()

while(1): #Execute until Control C or exit command.
    print("Welcome to shell, insert a command: ")
    instruction = input() #Obtain command to run.
    UserInput = instruction.split(" ")

    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif str(UserInput[0]) == "exit": #Exit command kills the shell.
        break;

    elif rc == 0:                   # child
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, UserInput[0])
            try:
                if '<' in UserInput:
                    getIndex = UserInput.index('<')
                    open(UserInput[getIndex+1],"w+") #Open file.
                    writeFile= os.open(UserInput[getIndex+1],os.O_WRONLY) #According to python documentation, this sets the write only flag.
                    os.dup2(writeFile,1) #Duplicate the file
                    UserInput= UserInput[:getIndex] #Overwrite the parameters with just what is required to execute.
                if '>' in UserInput:
                    getIndex = UserInput.index('>') #Look for the pipe, if the file is found, execute it.
                    newParams = open(UserInput[getIndex+1],"r").read().strip()
                    command = UserInput[0];
                    UserInput.clear() #Format new parameters to fit the syntax.
                    UserInput.append(command)
                    UserInput= UserInput+ newParams.split(' ')

                os.execve(program, UserInput, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly
            except ValueError: #Exception returned by the index if it does not contain > or <.
                pass

        os.write(2, ("Child:    Could not exec %s\n" % UserInput[0]).encode())
        sys.exit(0)                 # terminate with error

    else:                           # parent (forked ok)
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                     (pid, rc)).encode())
        UserInput = instruction.split(" ")
        childPidCode = os.wait() #Wait until child dies. 
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                     childPidCode).encode())
sys.exit(0) #Kill process if control c or exit.
