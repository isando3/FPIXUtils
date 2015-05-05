#! /usr/bin/env python

from sys import argv
import os
import subprocess

test=argv[1]
modules=argv[2:]

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Tini=os.getenv('HOME')+'/elComandante/config/elComandante.ini.default'
Tconf=os.getenv('HOME')+'/elComandante/config/elComandante.conf.default'

testString={}
testString['pretest']='Pretest'
testString['fulltest']='Fulltest'
testString['iv']='.'.join(['IV_'+str(x) for x in range(len(modules))])

############################################################
############################################################
############################################################

if test not in testString.keys():
    raise Exception('Not a valid test')

if len(modules)==0 or len(modules)>4:
    raise Exception('Too few or too many modules specified')

replacements=[['TESTS',testString[test].lower()]]
for i in range(len(modules)):
    replacements.append(['USEM'+str(i),'True'])
    replacements.append(['MODULE'+str(i),modules[i]])
for i in range(len(modules),4):
    replacements.append(['USEM'+str(i),'False'])

ini=Tini.replace('.default','')
conf=Tconf.replace('.default','')

subprocess.call(['cp',Tini,ini])
subprocess.call(['cp',Tconf,conf])

for replacement in replacements:
    print replacement
    subprocess.call(['sed','s/'+replacement[0]+'/'+replacement[1]+'/','--in-place',ini])
    subprocess.call(['sed','s/'+replacement[0]+'/'+replacement[1]+'/','--in-place',conf])
