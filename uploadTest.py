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

outputDir=os.environ['HOME']+'/ProductionTestResults'
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
    for inputDir in inputDirs:
        inputs=glob(inputDir)
        if not inputs:
            print 'ERROR: input directory',inputDir,'not found'
            exit()
        if len(inputs)>1:
            print 'ERROR: multiple input directories match string',inputDir
            exit()
        i=inputs[0]
        makeXML(i)
        move(i,outputDir+'/'+os.path.basename(i))
else:
    for module in moduleNames:
        if module=='0': continue
        print module
        input=sorted(glob('/home/fnalpix?/allTestResults/'+module+'_*[0-9]'))[-1]
        makeXML(input)
        move(input,outputDir+'/'+os.path.basename(input))

    
