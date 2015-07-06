#! /usr/bin/env python

from sys import argv
import os
import subprocess
from config import *

affirmativeResponses= ['true', 'True', '1', 't', 'T', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh', 'most def']

try:
    test=argv[1]
    doCold=argv[2] in affirmativeResponses
except:
    test=raw_input('\nEnter test name (Pretest, Fulltest, IV, or FPIXTest)\n')
    doCold=raw_input('\nPerform test at -20C? (y/n)\n').strip() in affirmativeResponses
    print '\n'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Tini=os.getenv('HOME')+'/elComandante/config/elComandante.ini.default'
Tconf=os.getenv('HOME')+'/elComandante/config/elComandante.conf.default'

testString={}
testString['Pretest']='powercycle,Pretest@T'
testString['Fulltest']='powercycle,Fulltest@T'
testString['IV']=','.join(['IV_'+str(x)+'@T' for x in range(len(moduleNames))])
testString['FPIXTest']='powercycle,FPIXTest@T,'+testString['IV']

############################################################
############################################################
############################################################

if test not in testString.keys():
    raise Exception('Not a valid test')

if len(moduleNames)==0 or len(moduleNames)>4:
    raise Exception('Too few or too many modules specified')

if doCold: temp='-20'
else:      temp='17'

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
