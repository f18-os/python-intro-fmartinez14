#!/bin/env python

print("Starting process...")

import sys        # command line arguments
import re         # regular expression tools
import os         # checking if file exists
import subprocess # executing program
#Original code for these imports provided by Dr.Freudenthal.




from collections import OrderedDict
#Importing dictionary for counter.

#Only accept three parameters from the console
if len(sys.argv) is not 3:
    print("Syntax for word was incorrect, please use the following: wordCount.py *input text file* *output file*")
    exit()

inputFileName = sys.argv[1]
outputFileName = sys.argv[2]

#Obtained file names for input and output files.


print("Input: " + inputFileName + " output: " + outputFileName)
#Declare variables and print them out to the screen.


print("Done") #Print out done.
