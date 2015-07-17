#! /usr/bin/env python

"""
Author: John Stupak (jstupak@fnal.gov)
Date: 5-2-15
Usage: ./checkPretest.py <input dir>
"""

import ROOT
ROOT.gErrorIgnoreLevel = ROOT.kWarning
from ROOT import *
#gStyle.SetOptStat(0)
import math
from config import *
from fnmatch import fnmatch

################################################################
################################################################
################################################################

goodModules=[]

def click(moduleNo):

    global goodModules

    if gPad.GetEvent()==11:
        if moduleNo in goodModules:
            goodModules.remove(moduleNo)

            testPad.cd(moduleNo+1)
            gPad.SetFillColor(kRed)
            gPad.Modified()
            gPad.Update()
        else:
            goodModules+=[moduleNo]
            goodModules.sort()

            testPad.cd(moduleNo+1)
            gPad.SetFillColor(kGreen)
            gPad.Modified()
            gPad.Update()

    return None

################################################################
################################################################
################################################################

class Comparison:
    
    def __init__(self, hName, refName, referenceFile, outputDir, info='All plots should resemble the reference plot'):
        self.hName=hName
        self.refFile=TFile(referenceFile)
        self.outputDir=outputDir
        self.info=info

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def do(self, testFiles):
        print self.hName
        testFiles=[TFile(f) for f in testFiles]

        #moduleNames=['_'.join(f.GetName().split('/')[-3].split('_')[:-4]) for f in testFiles]
        nModules = len(goodModuleNames)
        
        global goodModules
        goodModules=[]
        
        c=TCanvas('c','',1000,850)

        refPad=TPad('refPad','Reference Plot',.666,0.25,1,0.75)
        refPad.Draw()
        refPad.cd()

        for k in self.refFile.GetListOfKeys():
            dir=k.ReadObj()
            if type(dir)!=type(TDirectoryFile()): continue
            for key in dir.GetListOfKeys():
                if fnmatch(key.GetName(),self.hName.split('/')[-1]):
                    ref=key.ReadObj().Clone('REF__'+self.hName.split('/')[-1])
                    break
        is2D=(type(ref)==type(TH2D()))
        ref.Draw('COLZ'*is2D)

        c.cd()
        testPad=TPad('testPad','',0,0,.666,1)
        testPad.Divide(int(math.ceil(nModules/2.)),2)
        testPad.Draw()

        print self.hName

        histograms=[]
        for i in range(nModules):
            testPad.cd(i+1)
            h=None

            for k in testFiles[i].GetListOfKeys():
                dir=k.ReadObj()
                if type(dir)!=type(TDirectoryFile()): continue
                for key in dir.GetListOfKeys():
                    if fnmatch(key.GetName(),self.hName.split('/')[-1]):
                        h=key.ReadObj().Clone('REF__'+self.hName.split('/')[-1])
                        break
            #h=testFiles[i].Get(self.hName).Clone(moduleNames[i]+'__'+self.hName.split('/')[-1])
            try:
                h.SetTitle(goodModuleNames[i]+': '+h.GetTitle())
                h.Draw('COLZ'*is2D)
                histograms.append(h)
                
                gPad.Modified()
                gPad.Update()
                gPad.SetFillColor(kRed)
                gPad.Modified()
                gPad.Update()

                gPad.AddExec('exec','TPython::Exec( "click('+str(i)+')" );')
            except: pass

        c.Modified()
        c.Update()

        while True:
            input=raw_input('\n'+self.info+'\n\n'+'Press enter to submit results\n'+'Enter "-1" to go back a test\n\n')
            if input=='-1': 
                refPad.Close()
                testPad.Close()
                c.Close()
                return -1

            if input=='':
                badModules=[x for x in range(nModules) if x not in goodModules]
                for i in badModules:
                    try: testPad.GetPad(i+1).SaveAs(self.outputDir+'/'+histograms[i].GetName()+'.pdf')
                    except: pass
                badModuleNames=[goodModuleNames[i] for i in badModules]

                refPad.Close()
                testPad.Close()
                c.Close()

                return badModuleNames
