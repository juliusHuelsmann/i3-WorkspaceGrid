#!/usr/bin/python3

# This controller is somewhat outdated, lauching a python script each time an
# operation is to be performed introduces latency.
# 
# Therefore the interface controller.py offers the possibility to communicate
# via named pipes which reduces the overhead to \approx 0. 
# 
# This file can be used for testing a not-running version manually.

# USAGE:                                        Provide operation as parameter.




import sys
import os

currPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currPath)

from grid import GridInterface 


if len(sys.argv) > 1:
    k = GridInterface();

    for i in range(1, len(sys.argv)):
        try:
            command = "k." + sys.argv[i] + "()"
            i = exec(command)
            print("x command", i , command)
        except:
            print("Command " + sys.argv[i] + " not recognized.")
            help(k)

   
else:
    print("Please provide some of the functions below as arguments!")
    help(GridInterface)

