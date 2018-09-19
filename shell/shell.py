#! /usr/bin/env python3

import os, sys, time, re , subprocess, fileinput
UserInput=[]
remainingPipes=-1
pr,pw = os.pipe()
for f in (pr, pw):
    os.set_inheritable(f, True)

SystemOut= os.dup(1)
SystemIn=os.dup(0)

pid = os.getpid()
instruction = ""
while(1): #Execute until Control C or exit command.
    try:
        pathToUse= os.environ['PATH']

        try:
            PS1 = os.environ['PS1']
        except: #Check for PS1 Existing
            PS1= os.getcwd() + "$ "



        if len(UserInput) ==0:
            instruction = ""
            instruction = input(PS1) #Obtain command to run.
            instruction = instruction.strip()
            UserInput = instruction.split(" ")



        if "cd" in UserInput: #Change directory
            getIndex = UserInput.index('cd')
            os.chdir(UserInput[getIndex + 1])


        # print("------------------------------------------------------------------------")
        # print(str(UserInput))
        # print(str(len(UserInput)))
        # print("------------------------------------------------------------------------")
        # print(len(instruction))

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
                    # os.dup2(SystemIn,0)
                    # os.dup2(SystemOut,1)
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

                        if UserInput[-1]=='|':
                            instruction=""
                            print("deleting")
                            del UserInput[-1]

                        if instruction:
                            tmp= open("shll.tmp","w+") #Open file.
                            writeFile= os.open("shll.tmp",os.O_RDWR) #According to python documentation, this sets the write only flag.
                            os.dup2(writeFile,1) #Duplicate the file

                        # if not instruction:
                        #     print("dont worry you fuck")
                        #
                            # tmp= open("shll.tmp","r") #Open file.
                            # readFile= os.open("shll.tmp",os.O_RDONLY) #According to python documentation, this sets the write only flag.
                            # os.dup2(readFile,0) #Duplicate the file
                            #
                            # os.close(1)
                            # os.close(pw)
                            # os.close(pr)
                            # for line in fileinput.input(): #Debug : Read from stdin.
                            #     print("From child: <%s>" % line)


                        getIndex = UserInput.index('|')
                        if UserInput.count('|') >= 1:
                            UserInput= UserInput[:getIndex]



                        # if len(instruction) > 0:
                        #     # os.dup2(pw,sys.stdout.fileno())

                        # os.close(sys.stdout.fileno())

                        # tempDup= os.dup(pw)
                            # os.close(1)
                            # os.dup2(pw,1)
                            # for fd in (pr, pw):
                            #     os.close(fd)

                            # os.close(0)
                            # os.dup2(pr,0)
                            # for fd in (pw, pr):
                            #     os.close(fd)


                        # else:
                        #     open("leTemp.tmp","w+") #Open file.
                        #     writeFile= os.open("leTemp.tmp",os.O_WRONLY) #According to python documentation, this sets the write only flag.
                        #     os.dup2("leTemp.tmp",1) #Duplicate the file




                        # extraPipeCommand = subprocess.Popen(extraParams,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
                        # stdinPipe = extraPipeCommand.communicate()[0]
                        # writeOut = open("shell.tmp","w+")
                        # writeOut.write(stdinPipe.decode())
                        # writeOut.close()
                        # open("shell.tmp","r")
                        # readFile= os.open("shell.tmp",os.O_RDONLY)
                        # os.dup2(readFile,0)

                    if '&' in UserInput:
                        getIndex= UserInput.index('&')
                        del UserInput[getIndex]



                        # open(os.devnull,"w+") #Open file.
                        # writeFile= os.open(os.devnull,os.O_WRONLY) #According to python documentation, this sets the write only flag. We write to a null file so the output isnt shown.
                        # readFile= os.open(os.devnull,os.O_RDONLY)
                        # os.dup2(readFile,0)
                        # os.dup2(writeFile,1) #Duplicate the file

                    if len(UserInput) < 1 or UserInput[0] == "" or UserInput[0] == "cd":
                        os._exit(0) #Kill the kid without exec if its an implemented feature.

                    os.execve(program, UserInput, os.environ) # try to exec program
                except FileNotFoundError:             # ...expected
                    pass                              # ...fail quietly
                except ValueError: #Exception returned by the index if it does not contain > or <.
                    sys.exit(0)
                    pass

            print("Could not find this command:" + str(UserInput[0]))
            os._exit(0)

        else:
            if '|' in UserInput:
                childPidCode = os.wait() #Wait until child dies.
                code, error = childPidCode

                if UserInput[-1]=='|':
                    del UserInput[-1]
                try:
                    getIndex = UserInput.index('|')
                    if UserInput.count('|') >= 1:
                        UserInput= UserInput[getIndex+1:]
                        UserInput.append('<')
                        UserInput.append("shll.tmp")
                    else:
                        del UserInput[getIndex]

                except:
                    pass

                instruction = ""


            elif '&' in UserInput: #Do not wait if the # is present.
                getIndex= UserInput.index('&')
                del UserInput[getIndex]
                pass

            else:
                childPidCode = os.wait() #Wait until child dies.
                code, error = childPidCode
                UserInput=[]
                instruction = ""
                if os.path.exists("shll.tmp"):
                  os.remove("shll.tmp")
                if error != 0: #If it was not sucessful, report it.
                    print("Process terminated with this exit code:  " + str(error))


    except EOFError: #If eof is passed to program, termiante.
        sys.exit(0)
sys.exit(0) #Kill process if control c or exit.
