#! /usr/bin/env python

from config import *
from lessWeb import *

if len(argv)>1:
    doCold=argv[1]
else:
    raise Exception("You must specify if test was performed cold")

for module in moduleNames:
    input=sorted(glob('/home/fnalpix?/ShareTestResults/'+module+'_ElComandanteTest_*/*_'+testName.capitalize()+'_*'))[-1]
    makeXML(input)
    
