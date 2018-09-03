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

WordCounter = {}
with open(inputFileName, 'r') as inputFile: #Add to the dictionary the words found in the file.
    for line in inputFile:
        line= line.strip() 
        wordLine = re.split("[- \t  : . ; , ' \n --]", line) #Splitting depending on all of the regexe's given here.
        for currentWord in wordLine:
            if len(currentWord) != 0:
                currentWord= currentWord.lower() #making all words lower case to prevent disturbing the count.
                if currentWord not in WordCounter:
                    WordCounter[currentWord]=1 #Start the element if not in dictionary.
                else:
                    WordCounter[currentWord] += 1 #Add to element otherwise.

sortedWordCounts= OrderedDict(sorted(WordCounter.items(), key=lambda x: x[0]))
dictionaryWriter = open(outputFileName, 'w') #Sorting dictionary
for value,key in sortedWordCounts.items():
    dictionaryWriter.write(value + " " + str(key) + '\n')
#Writing to file
print("Done") #Print out done.
