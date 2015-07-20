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
    #else: print gPad.GetEvent()

    return None

def makeIV(input):
    """
    #
    #--------LOG from Tue 30 Jun 2015 at 14h:26m:49s ---------
    #
    #voltage(V)current(A)timestamp
    -0.030-1.6675e-081435692186
    -5.028-5.0295e-081435692191
    -10.026-7.5020e-081435692196
    -15.023-9.8705e-081435692201
    """

    values=[]
    for line in open(input):
        if line[0]=='#': continue
        values.append([abs(float(line.split()[0])),float(line.split()[1])])
    
    nBins=len(values)
    xMin=0
    xMax=nBins*round(values[1][0]-xMin,0)
    binWidth=float(xMax-xMin)/(nBins-1)
    xMin-=binWidth/2
    xMax+=binWidth/2
    
    h=TH1F('IV',';-U [V];-I [#muA]',nBins,xMin,xMax)
    for i in range(len(values)): h.SetBinContent(i+1, -1*values[i][1])
    h.SetMaximum(5*h.GetMaximum())
    
    return h

################################################################
################################################################
################################################################

class Comparison:
    
    def __init__(self, hName, testFiles, refName, referenceFile, outputDir, info='All plots should resemble the reference plot'):
        self.hName=hName
        self.testFiles=testFiles
        self.refFile=referenceFile
        self.outputDir=outputDir
        self.info=info

        self.goodModuleNames=[f.split('_ElComandanteTest')[0].split('/')[-1] for f in self.testFiles]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def do(self):
        print self.hName

        if self.hName=='IV/IV':
            #make temporary root file and put IV plot in it
            testFiles=[]
            for f in self.testFiles:
                file=TFile(f.replace('log','root'),'RECREATE')
                file.cd()
                file.mkdir('IV')
                file.cd('IV')
                h=makeIV(f)
                file.Write()
                testFiles.append(file)
        else:
            testFiles=[TFile(f) for f in self.testFiles]

        print testFiles
        nModules = len(self.testFiles)
        
        global goodModules
        goodModules=[]
        
        c=TCanvas('c','',1000,850)

        refPad=TPad('refPad','Reference Plot',.666,0.25,1,0.75)
        refPad.Draw()
        refPad.cd()

        if self.hName=='IV/IV':
            #make temporary root file and put IV plot in it
            file=TFile(self.refFile.replace('log','root'),'RECREATE')
            file.cd()
            file.mkdir('IV')
            file.cd('IV')
            h=makeIV(self.refFile)
            file.Write()
            self.refTFile=file
            
            refPad.SetLogy()
        else:
            self.refTFile=TFile(self.refFile)

        for k in self.refTFile.GetListOfKeys():
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

            if self.hName=='IV/IV': gPad.SetLogy()

            h=None

            print i
            for k in testFiles[i].GetListOfKeys():
                dir=k.ReadObj()
                if type(dir)!=type(TDirectoryFile()): continue
                for key in dir.GetListOfKeys():
                    if fnmatch(key.GetName(),self.hName.split('/')[-1]):
                        h=key.ReadObj().Clone(self.hName.split('/')[-1])
                        break

            try:
                h.SetTitle(self.goodModuleNames[i]+': '+h.GetTitle())
                h.Draw('COLZ'*is2D)
                histograms.append(h)

                if self.hName=='IV/IV':
                    I100=h.GetBinContent(h.FindBin(100))
                    I150=h.GetBinContent(h.FindBin(150))

                    l=TLatex()
                    l.DrawLatex(10,1E-5,"I(150V)="+str(round(I150*1E6,1))+"#muA")
                    l2=TLatex()
                    l2.DrawLatex(10,3E-6,"I(150V)/I(100V)="+str(round(I150/I100,2)))

                gPad.Modified()
                gPad.Update()
                gPad.SetFillColor(kRed)
                gPad.Modified()
                gPad.Update()

                gPad.AddExec('exec','TPython::Exec( "click('+str(i)+')" );')
            except: 
                print 'Missing plot for module',self.goodModuleNames[i]
                

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
                badModuleNames=[self.goodModuleNames[i] for i in badModules]

                refPad.Close()
                testPad.Close()
                c.Close()

                return badModuleNames
