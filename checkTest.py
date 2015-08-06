#! /usr/bin/env python

"""
Author: John Stupak (jstupak@fnal.gov)
Date: 5-2-15
Usage: ./checkTest.py <test>
"""

from Comparison import *
from sys import argv
from config import *
from glob import glob
import os

#referenceFile=os.environ['HOME']+'/ShareTestResults/P-A-2-23_ElComandanteTest_2015-06-30_14h09m_1435691373/001_FPIXTest_p17/commander_FPIXTest.root'
#IVReferenceFile=os.environ['HOME']+'/ShareTestResults/P-A-2-23_ElComandanteTest_2015-06-30_14h09m_1435691373/000_IV_p17/ivCurve.log'
referenceFile=os.environ['HOME']+'/ShareTestResults/elComandante/P-A-2-23_ElComandanteTest_2015-07-13_15h33m_1436819615/000_FPIXTest_p17/commander_FPIXTest.root'
IVReferenceFile=os.environ['HOME']+'/ShareTestResults/elComandante/P-A-2-23_ElComandanteTest_2015-07-13_15h33m_1436819615/001_IV_p17/ivCurve.log'

outputDir=os.environ['HOME']+'/forExperts'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if len(argv)>1:
    testName=argv[1]
else:
    raise Exception("You must specify which test to check")

inputDirs=None
if len(argv)>2:
    inputDirs=argv[2:]

testFiles=[]; IVFiles=[]

if inputDirs:
    testFiles=[glob(d+'/*/commander_'+testName+'.root')[0] for d in inputDirs]
    if testName=='FPIXTest': IVFiles=[glob(d+'/*_IV_*/ivCurve.log')[0] for d in inputDirs]
else:
    for module in goodModuleNames:
        s=os.environ['HOME']+'/ShareTestResults/elComandante/'+module+'_ElComandanteTest_*/*_'+testName+'_*/commander_'+testName+'.root'
        try: testFiles.append(sorted(glob(s))[-1])
        except: 
            print 'Found no files matching:',s
            exit()

        if testName=='FPIXTest': 
            s=os.environ['HOME']+'/ShareTestResults/elComandante/'+module+'_ElComandanteTest_*/*_IV_*/ivCurve.log'
            try: IVFiles.append(sorted(glob(s))[-1])
            except:
                print 'Found no files matching:',s
                exit()

if testName=='Pretest':
    theComparisons=[Comparison('Pretest/programROC_V0',testFiles,'Pretest/programROC_V0',referenceFile,outputDir,'All y values should be greater than 0'),
                    Comparison('Pretest/Iana_V0',testFiles,'Pretest/Iana_V0',referenceFile,outputDir,'All y values should be approximately 24')]
    theComparisons+=[Comparison('Pretest/pretestVthrCompCalDel_c*r*_C'+str(i)+'_V0',testFiles,'Pretest/pretestVthrCompCalDel_c*_r*_C0_V0',referenceFile,outputDir) for i in range(16)]

if testName=='FPIXTest':
    theComparisons=[]
    theComparisons+=[Comparison('IV/IV',IVFiles,'IV/IV',IVReferenceFile,outputDir)]
    #theComparisons+=[Comparison('Trim/dist_thr_TrimThrFinal_vcal_C'+str(i)+'_V0',testFiles,'Trim/dist_thr_TrimThrFinal_vcal_C0_V0',referenceFile,outputDir,'Distribution should be sharply peaked around 35') for i in range(16)]
    theComparisons+=[Comparison('Scurves/dist_thr_scurveVcal_Vcal_C'+str(i)+'_V0',testFiles,'Scurves/dist_thr_scurveVcal_Vcal_C0_V0',referenceFile,outputDir,'Distribution should be sharply peaked around 35') for i in range(16)]
    theComparisons+=[Comparison('Scurves/dist_sig_scurveVcal_Vcal_C'+str(i)+'_V0',testFiles,'Scurves/dist_sig_scurveVcal_Vcal_C0_V0',referenceFile,outputDir,'Distribution should peak above 2') for i in range(16)]
    theComparisons+=[Comparison('PhOptimization/PH_c*_r*_C'+str(i)+'_V0',testFiles,'PhOptimization/PH_c*_r*_C0_V0',referenceFile,outputDir,'') for i in range(16)]
    theComparisons+=[Comparison('GainPedestal/gainPedestalNonLinearity_C'+str(i)+'_V0',testFiles,'GainPedestal/gainPedestalNonLinearity_C0_V0',referenceFile,outputDir,'Distribution should be sharply peaked just below 1') for i in range(16)]
    theComparisons+=[Comparison('PixelAlive/PixelAlive_C'+str(i)+'_V0',testFiles,'PixelAlive/PixelAlive_C0_V0',referenceFile,outputDir,'Plot should be almost entirely red') for i in range(16)]
    theComparisons+=[Comparison('BB3/dist_rescaledThr_C'+str(i)+'_V0',testFiles,'BB3/dist_rescaledThr_C0_V0',referenceFile,outputDir,'Less than ~5% of the entries should be at larger x values than the arrow') for i in range(16)]
    
################################################################
################################################################
################################################################

if __name__=='__main__':

    results=[]
    i=0
    badModules=[]
    while i<len(theComparisons):
        #gSystem.Sleep(100)
        result=theComparisons[i].do()
        
        #go back one test
        if result==-1: i=max(i-1,0)

        if type(result)==type([]):
            try: results[i]=result
            except: results.append(result)
            i+=1

    badModules=set([])
    for result in results:
        badModules=badModules|set(result)
    badModules=list(badModules)
    if len(badModules)>0:
        print 'Replace the following module(s) and repeat pre-test:'
        for m in badModules:
            print '    - '+str(m)
    else:
        print 'Rock on'
        
