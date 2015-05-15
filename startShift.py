#! /usr/bin/env python

print '\n'
shifter=raw_input('Enter your name:\n')

moduleNames=[]
for i in range(4):
    print '\n'
    moduleName=raw_input('Enter module '+str(i)+' (starting from rear of coldbox) name:\n')
    if moduleName: moduleNames.append(moduleName)
    else: break

f=open('/home/fnalpix2/FPIXUtils/config.py','w')
f.write('shifter="'+shifter+'"\n\n')

f.write('moduleNames=[\n')
for i in range(0,len(moduleNames)):
    f.write('\t"'+moduleNames[i]+'",\n')
f.write(']')

f.close()
    
