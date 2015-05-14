#! /usr/bin/env python

from config import *
from lessWeb import *
from sys import argv

if len(argv)>2:
    testName=argv[1]
    doCold=argv[2]
else:
    raise Exception("You must specify if test was performed cold")

for module in moduleNames:
    input=sorted(glob('/home/fnalpix?/ShareTestResults/'+module+'_ElComandanteTest_*'))[-1]
    makeXML(input)
    
