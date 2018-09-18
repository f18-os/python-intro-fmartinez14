#! /usr/bin/env python3

import os, sys, time, re , subprocess


pid = os.getpid()
while(1): #Execute until Control C or exit command.
    try:
        if os.path.exists("shell.tmp"):
          os.remove("shell.tmp")
        pathToUse= os.environ['PATH']
        try:
            PS1 = os.environ['PS1']
        except: #Check for PS1 Existing
            PS1= os.getcwd() + "$ "

        instruction = ""
        instruction = input(PS1) #Obtain command to run.
        instruction = instruction.strip()
        UserInput = instruction.split(" ")


        if "cd" in UserInput: #Change directory
            getIndex = UserInput.index('cd')
            os.chdir(UserInput[getIndex + 1])

        rc = os.fork()


        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)

        elif str(UserInput[0]) == "exit": #Exit command kills the shell.
            break;

        elif rc == 0:                   # child
            if len(UserInput) > 0 and UserInput[0] != "" and UserInput[0][0] == '/': #Checks for a direct path, if not , resort to $PATH
                tempVar = UserInput[0].split("/")
                commandToUse= tempVar[-1]
                UserInput[0] = commandToUse
                tempVar= tempVar[:-1]
                pathToUse = "/".join(tempVar)
            for dir in re.split(":", pathToUse): # try each directory in the path
                program = "%s/%s" % (dir, UserInput[0])
                try:
                    if '>' in UserInput:
                        getIndex = UserInput.index('>')
                        open(UserInput[getIndex+1],"w+") #Open file.
                        writeFile= os.open(UserInput[getIndex+1],os.O_WRONLY) #According to python documentation, this sets the write only flag.
                        os.dup2(writeFile,1) #Duplicate the file
                        UserInput= UserInput[:getIndex] #Overwrite the parameters with just what is required to execute.
                    if '<' in UserInput:
                        getIndex = UserInput.index('<') #Look for the pipe, if the file is found, execute it.
                        UserInput.remove('<')
                        open(UserInput[getIndex],"r")
                        readFile= os.open(UserInput[getIndex],os.O_RDONLY)
                        os.dup2(readFile,0)

                    if '|' in UserInput: #Gets a pipe to execute commands and use them as process.
                        getIndex = UserInput.index('|')
                        extraParams = UserInput[:getIndex]
                        UserInput = UserInput[getIndex+1:]
                        extraPipeCommand = subprocess.Popen(extraParams,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
                        stdinPipe = extraPipeCommand.communicate()[0]
                        writeOut = open("shell.tmp","w+")
                        writeOut.write(stdinPipe.decode())
                        writeOut.close()
                        open("shell.tmp","r")
                        readFile= os.open("shell.tmp",os.O_RDONLY)
                        os.dup2(readFile,0)

                    if '&' in UserInput:
                        getIndex= UserInput.index('&')
                        del UserInput[getIndex]
                        open(os.devnull,"w+") #Open file.
                        writeFile= os.open(os.devnull,os.O_WRONLY) #According to python documentation, this sets the write only flag. We write to a null file so the output isnt shown.
                        readFile= os.open(os.devnull,os.O_RDONLY)
                        os.dup2(readFile,0)
                        os.dup2(writeFile,1) #Duplicate the file

                    if len(UserInput) < 1 or UserInput[0] == "" or UserInput[0] == "cd":
                        os._exit(0) #Kill the kid without exec if its an implemented feature.

                    os.execve(program, UserInput, os.environ) # try to exec program
                except FileNotFoundError:             # ...expected
                    pass                              # ...fail quietly
                except ValueError: #Exception returned by the index if it does not contain > or <.
                    pass

            print("Could not find this command:" + str(UserInput[0]))
            os._exit(0)

        else:
            if '&' in UserInput: #Do not wait if the # is present.
                getIndex= UserInput.index('&')
                del UserInput[getIndex]
                pass
            else:
                childPidCode = os.wait() #Wait until child dies.
                code, error = childPidCode
                if error != 0: #If it was not sucessful, report it.
                    print("Process terminated with this exit code:  " + str(error))

    except EOFError: #If eof is passed to program, termiante.
        sys.exit(0)
sys.exit(0) #Kill process if control c or exit.
