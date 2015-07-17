#! /usr/bin/env python

"""
Author: John Stupak (jstupak@fnal.gov)
Date: 4-9-15
Usage: python uploadTest.py <testName> <isCold> [input dir]
"""

from config import *
from lessWeb import *
from sys import argv

if len(argv)>2:
    testName=argv[1]
    doCold=argv[2]
    inputDirs=None
    if len(argv)>3:
        inputDirs=argv[3:]
else:
    raise Exception("You must specify if test was performed cold")

if inputDirs:
    for input in inputDirs:
        for i in glob(input):
            makeXML(i)
else:
    for module in moduleNames:
        input=sorted(glob('/home/fnalpix?/ShareTestResults/elComandante/'+module+'_ElComandanteTest_*[0-9]'))[-1]
        makeXML(input)
    
