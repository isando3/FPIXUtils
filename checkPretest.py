#! /usr/bin/env python

"""
Author: John Stupak (jstupak@fnal.gov)
Date: 5-2-15
Usage: ./checkPretest.py <input root file 1> ... <input root file N>
"""

from Comparison import *

from sys import argv

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if len(argv)>1:
    testFiles=argv[1:]
else:
    testFiles=['/Users/jstupak/CMS/pixel/ShareTestResults/M_LL_922_ElComandanteTest_2015-04-28_10h33m_1430235234/001_Pretest_p17/commander_Pretest.root',
               '/Users/jstupak/CMS/pixel/ShareTestResults/M_TT_915_ElComandanteTest_2015-04-28_10h33m_1430235234/001_Pretest_p17/commander_Pretest.root',
               '/Users/jstupak/CMS/pixel/ShareTestResults/P-A-03-42_ElComandanteTest_2015-04-28_10h33m_1430235234/001_Pretest_p17/commander_Pretest.root',
               '/Users/jstupak/CMS/pixel/ShareTestResults/M_FR_902_ElComandanteTest_2015-04-16_15h24m_1429215874/001_Pretest_p17/commander_Pretest.root'
               ]

referenceFile='/Users/jstupak/CMS/pixel/ShareTestResults/M_FR_902_ElComandanteTest_2015-04-16_15h24m_1429215874/001_Pretest_p17/commander_Pretest.root'

outputDir='tmp'

theComparisons=[Comparison('Pretest/programROC_V0','Pretest/programROC_V0',referenceFile,outputDir,'All y values should be greater than 0'),
                Comparison('Pretest/Iana_V0','Pretest/Iana_V0',referenceFile,outputDir,'All y values should be approximately 24')]
theComparisons+=[Comparison('Pretest/pretestVthrCompCalDel_c12_r22_C'+str(i)+'_V0','Pretest/pretestVthrCompCalDel_c12_r22_C0_V0',referenceFile,outputDir) for i in range(16)]

################################################################
################################################################
################################################################

if __name__=='__main__':

    results=[]
    i=0
    badModules=[]
    while i<len(theComparisons):
        result=theComparisons[i].do(testFiles)
        
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
        
