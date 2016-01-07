#!/usr/local/bin/python
from ROOT import *
import subprocess
import os
import sys

XrayInDir = sys.argv[1]

def placeHRFiles():
  for f in os.listdir(XrayInDir + '/000_FPIXTest_p17'):
    if 'hr' in f and 'root' in f and 'NoCal' not in f:
      hrdig = list(f)[2] + list(f)[3]
      hrVal = int(hrdig)/5 + 1
      hrDir = '/%03d'%hrVal + '*'
      subprocess.call('cp '+ XrayInDir + '/000_FPIXTest_p17/' + f + ' ' + topDir + '/' + hrDir, shell = True)

def writeIniFile():
  inTmpFile = open('elComandante.ini.tmp')
  outTmpFile = open('elComandante.ini', 'w')
  for line in inTmpFile:
    if 'insertTestsHere' in line:
      line = 'Test = HRData@60MHz/cm2,HRData@130MHz/cm2>{HREfficiency@30MHz/cm2,HREfficiency@60MHz/cm2,HREfficiency@100MHz/cm2,HREfficiency@130MHz/cm2,HREfficiency@170MHz/cm2}' + '\n'
    outTmpFile.write(line)
  inTmpFile.close()
  outTmpFile.close()
  subprocess.call('mv elComandante.ini ' + topDir + '/configfiles', shell = True)


module = XrayInDir.split('_')[0]
date = XrayInDir.split('_')[2]
time = XrayInDir.split('_')[3]
number = XrayInDir.split('_')[4]

topDir = module + '_XrayQualification_' + date + '_' + time + '_' + number
print 'Creating directory: ' + topDir
print 'tarring directory...'

mainDirList = ['HRData_60','HRData_130','HREfficiency_30', 'HREfficiency_60', 'HREfficiency_100', 'HREfficiency_130', 'HREfficiency_170']

configParamFilePath = XrayInDir + '/000_FPIXTest_p17/configParameters.dat'
testParamFilePath = XrayInDir + '/000_FPIXTest_p17/testParameters.dat'
defaultMaskFilePath = XrayInDir + '/000_FPIXTest_p17/defaultMaskFile.dat'

subprocess.call('mkdir ' + topDir, shell = True)
for i in range (0, len(mainDirList)):
  subprocess.call('mkdir ' + topDir + '/%03d'%i + '_' + mainDirList[i], shell = True)
  subprocess.call('cp ' + configParamFilePath + ' ' + topDir + '/%03d'%i + '_' + mainDirList[i], shell = True)
  subprocess.call('cp ' + testParamFilePath + ' ' + topDir + '/%03d'%i + '_' + mainDirList[i], shell = True)
  subprocess.call('cp ' + defaultMaskFilePath + ' ' + topDir + '/%03d'%i + '_' + mainDirList[i], shell = True)
subprocess.call('mkdir ' + topDir + '/configfiles', shell = True)
subprocess.call('mkdir ' + topDir + '/logfiles', shell = True)
subprocess.call('cp ' + XrayInDir + '/000_FPIXTest_p17/dc10*' + ' ' + topDir + '/000_HRData_60/', shell = True)
subprocess.call('cp ' + XrayInDir + '/000_FPIXTest_p17/dc20*' + ' ' + topDir + '/001_HRData_130/', shell = True)

placeHRFiles()
writeIniFile()

if '/' in topDir:
  topDir = topDir.replace("/", "")
subprocess.call('tar -zcvf ' + topDir + '.tar.gz ' + topDir, shell = True)