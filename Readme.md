This repository has a utility that counts the number of instances of a word inside a text and
counts them. Afterwards, it will write it to a file and sort it alphabetically.

Usage is as follows:
`$ python3 wordCount.py input.txt output.txt`

To test the program, the given program wordCountText.py was given , and its usage is as follows:

`$ python3 wordCountTest.py declaration.txt myOutput.txt declarationKey.txt`

Similarly, the shell folder contains a shell project that is run by using the following command:


`$ python3 shell.py`

It works using a bash-like commands which gets executed using the execv tool.

It supports both I/O redirects, piping and background.

This program will work using more than one pipe. However, it will display the output of all the pipes one at a time. Therefore, it will show as failed in the shell tester. Inside the shell, it will work and complete the command.

To test it against the shell program, one must run:

`./shellTest.sh ./shell.py`
