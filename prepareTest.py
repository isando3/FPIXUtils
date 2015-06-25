#! /usr/bin/env python

from sys import argv
import os
import subprocess
from config import *

test=argv[1]
doCold=argv[2]

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Tini=os.getenv('HOME')+'/elComandante/config/elComandante.ini.default'
Tconf=os.getenv('HOME')+'/elComandante/config/elComandante.conf.default'

testString={}
testString['Pretest']='powercycle,Pretest@T'
testString['Fulltest']='powercycle,Fulltest@T'
testString['IV']='powercycle,'+','.join(['IV_'+str(x)+'@T' for x in range(len(moduleNames))])
testString['FPIXTest']=testString['IV']+',FPIXTest@T'

############################################################
############################################################
############################################################

if test not in testString.keys():
    raise Exception('Not a valid test')

if len(moduleNames)==0 or len(moduleNames)>4:
    raise Exception('Too few or too many modules specified')

print doCold
if doCold=='True':    temp='-20'
elif doCold=='False':  temp='17'
else: raise Exception('Invalid doCold option')

replacements=[['TESTS',testString[test].replace('@T','@'+temp)]]
for i in range(len(moduleNames)):
    replacements.append(['USEM'+str(i),'True'])
    replacements.append(['MODULE'+str(i),moduleNames[i]])
for i in range(len(moduleNames),4):
    replacements.append(['USEM'+str(i),'False'])

ini=Tini.replace('.default','')
conf=Tconf.replace('.default','')

subprocess.call(['cp',Tini,ini])
subprocess.call(['cp',Tconf,conf])

for replacement in replacements:
    print replacement
    subprocess.call(['sed','s/'+replacement[0]+'/'+replacement[1]+'/','--in-place',ini])
    subprocess.call(['sed','s/'+replacement[0]+'/'+replacement[1]+'/','--in-place',conf])
