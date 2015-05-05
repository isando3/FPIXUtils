#! /usr/bin/env python

"""
Author: John Stupak (jstupak@fnal.gov)
Date: 5-2-15
Usage: ./checkPretest.py <input dir>
"""

import ROOT
ROOT.gErrorIgnoreLevel = ROOT.kWarning
from ROOT import *
gStyle.SetOptStat(0)
import math

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
        testFiles=[TFile(f) for f in testFiles]

        moduleNames=['_'.join(f.GetName().split('/')[-3].split('_')[:-4]) for f in testFiles]
        nModules=len(moduleNames)
        
        global goodModules
        goodModules=[]
        
        c=TCanvas('c','',600,800)

        refPad=TPad('refPad','Reference Plot',.666,0.25,1,0.75)
        refPad.Draw()
        refPad.cd()

        ref=self.refFile.Get(self.hName).Clone('REF__'+self.hName.split('/')[-1])
        is2D=(type(ref)==type(TH2D()))
        ref.Draw('COLZ'*is2D)

        c.cd()
        testPad=TPad('testPad','',0,0,.666,1)
        testPad.Divide(int(math.ceil(nModules/2.)),2)
        testPad.Draw()

        histograms=[]
        for i in range(nModules):
            testPad.cd(i+1)

            h=testFiles[i].Get(self.hName).Clone(moduleNames[i]+'__'+self.hName.split('/')[-1])
            h.SetTitle(moduleNames[i])
            h.Draw('COLZ'*is2D)
            histograms.append(h)

            gPad.Modified()
            gPad.Update()
            gPad.SetFillColor(kRed)
            gPad.Modified()
            gPad.Update()

            gPad.AddExec('exec','TPython::Exec( "click('+str(i)+')" )')

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
                    testPad.GetPad(i+1).SaveAs(self.outputDir+'/'+histograms[i].GetName()+'.pdf')
                badModuleNames=[moduleNames[i] for i in badModules]

                refPad.Close()
                testPad.Close()
                c.Close()

                return badModuleNames
