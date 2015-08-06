#! /usr/bin/env python

from sys import argv
import os
import subprocess
import socket
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
testString['Pretest']='Pretest@T'
testString['Fulltest']='Fulltest@T'
IVString = ""
for i in range(len(moduleNames)):
    if moduleNames[i] is not '0':
        IVString += 'IV_'+str(i)+'@T,'
IVString.rstrip(',')
testString['IV']=IVString
testString['FPIXTest']='FPIXTest@T,'+testString['IV']

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

replacements.append(['OPERATOR',shifter])
for i in range(4):
    if moduleNames[i] is not '0':
        replacements.append(['USEM'+str(i),'True'])
        replacements.append(['MODULE'+str(i),moduleNames[i]])
    else:
        replacements.append(['USEM'+str(i),'False'])

station=os.environ['HOME'].split('/')[1]
replacements.append(['TESTCENTER',station])

replacements.append(['TESTCENTER',socket.gethostname()])

ini=Tini.replace('.default','')
conf=Tconf.replace('.default','')

subprocess.call(['cp',Tini,ini])
subprocess.call(['cp',Tconf,conf])

for replacement in replacements:
    print replacement
    subprocess.call(['sed','s/'+replacement[0]+'/'+replacement[1]+'/','--in-place',ini])
    subprocess.call(['sed','s/'+replacement[0]+'/'+replacement[1]+'/','--in-place',conf])
