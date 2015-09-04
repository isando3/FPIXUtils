#! /usr/bin/env python

"""
Author: John Stupak (jstupak@fnal.gov)
Date: 4-9-15
Usage: python uploadTest.py <testName> <isCold> [input dir]
"""

from config import *
from lessWeb import *
from sys import argv
from shutil import move
import os

outputDir=os.environ['HOME']+'/ShareTestResults/elComandante'
#outputDir=os.environ['HOME']+'/john'

"""
if len(argv)>2:
    testName=argv[1]
    doCold=argv[2]
    inputDirs=None
    if len(argv)>3:
        inputDirs=argv[3:]
else:
    raise Exception("You must specify if test was performed cold")
"""

if len(argv)>1: inputDirs=argv[1:]
else: inputDirs=None

if inputDirs:
    for input in inputDirs:
        for i in glob(input):
            makeXML(i)
            move(i,outputDir+'/'+os.path.basename(i))
else:
    for module in moduleNames:
        if module=='0': continue
        print module
        input=sorted(glob('/home/fnalpix?/allTestResults/'+module+'_ElComandanteTest_*[0-9]'))[-1]
        makeXML(input)
        move(input,outputDir+'/'+os.path.basename(input))

    
