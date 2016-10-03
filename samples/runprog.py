###############################################
# This file illustrates how to run another
# program from python code. As an example,
# Here we are using program openssl which we
# assumes resides in the same directory as
# this file.  Please feel free to use this code
# in your extorter worm.
###############################################

# Import the necessary files
from subprocess import call

# The following is an example which makes
# program openssl executable once you download
# it from the web. The code that follows is 
# equivalent to running chmod a+x openssl
# from the shell command line. 
# The format is <command name>, <ARG1>, <ARG2>,
# ..., <ARGN> where each ARGi is an argument. 
call(["chmod", "a+x", "./openssl"])

# The code below is equivalent to running line:
# openssl aes-256-cbc -a -salt -in secrets.txt -out secrets.txt.enc
# from the shell prompt. 
# You do not need to understand the details of how
# this program works. Basically, "runprog.py" is the
# input file to the program which we would like to
# encrypt, "runprog.py.enc" is the output file 
# containing encrypted contents of file 
# "runprog.py.enc" and "pass" is the password.
call(["./openssl", "aes-256-cbc", "-a", "-salt", "-in", "runprog.py", "-out", "runprog.py.enc", "-k", "pass"])


