#! /usr/bin/env python

"""
Author: John Stupak (jstupak@fnal.gov)
Date: 4-9-15
Usage: python xRayUpload.py <input root file>
"""

##############################################################
outputDir='/Users/jstupak/tmp'
##############################################################

from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom
SE=SubElement

import ROOT
#ROOT.gErrorIgnoreLevel = ROOT.kWarning
from ROOT import *
gStyle.SetOptStat(0)
gROOT.SetBatch(1)

from glob import glob
import os
import subprocess
import sys
import zipfile

DEBUG=False

if len(sys.argv)<2:
    inputFile='/Users/jstupak/tmp/P-A-3-42.root'
else:
    inputFile=sys.argv[1]

################################################################
################################################################
################################################################

def prettify(elem):
    roughString = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(roughString)
    return reparsed.toprettyxml(indent="  ")

#---------------------------------------------------------------

def attachName(parent):
    name=SE(parent,'NAME')
    name.text=moduleName

################################################################

def analyze(inputFile, outputDir):
    rocs=SE(top, 'ROCS')
    attachName(rocs)

    c=TCanvas()
    slope=inputFile.GetKey('Ele/Vcal').ReadObj()
    offset=inputFile.Get('Offset')
    badBumps=inputFile.Get('BadBumps')

    slopes=[]; offsets=[]; bb=[]
    for i in range(16):
        roc=SE(rocs, 'ROC')
        position=SE(roc, 'POSITION')
        position.text=str(i)
        xray_offset=SE(roc, 'XRAY_OFFSET')
        xray_offset.text=str(round(offset.GetBinContent(i+1),2))
        offsets.append(round(offset.GetBinContent(i+1),2))
        xray_slope=SE(roc, 'XRAY_SLOPE')
        xray_slope.text=str(round(slope.GetBinContent(i+1),2))
        slopes.append(round(slope.GetBinContent(i+1),2))
        BADBUMPS_XRAY=SE(roc, 'BADBUMPS_XRAY')
        BADBUMPS_XRAY.text=str(int(badBumps.GetBinContent(i+1)))
        bb.append(int(badBumps.GetBinContent(i+1)))

    pic=SE(top, 'PIC')
    attachName(pic)
    file=SE(pic, 'FILE')
    file.text='slope.png'
    slope.Draw()
    c.SaveAs(outputDir+'/'+file.text)
    txt=SE(pic, 'TXT')
    txt.text='slope.txt'
    comment=open(outputDir+'/'+txt.text,'w')
    comment.write('\nslopes='+str(slopes))
    part=SE(pic,'PART')
    part.text='sidet_p'

    pic=SE(top, 'PIC')
    attachName(pic)
    file=SE(pic, 'FILE')
    file.text='offset.png'
    offset.Draw()
    c.SaveAs(outputDir+'/'+file.text)
    txt=SE(pic, 'TXT')
    txt.text='offset.txt'
    comment=open(outputDir+'/'+txt.text,'w')
    comment.write('\noffsets='+str(offsets))
    part=SE(pic,'PART')
    part.text='sidet_p'

    mean=inputFile.Get('Means')
  
    pic=SE(top, 'PIC')
    attachName(pic)
    file=SE(pic, 'FILE')
    file.text='mean.png'
    mean.Draw('COLZ')
    c.SaveAs(outputDir+'/'+file.text)
    txt=SE(pic, 'TXT')
    txt.text='mean.txt'
    part=SE(pic,'PART')
    part.text='sidet_p'

    comment=open(outputDir+'/'+txt.text,'w')
    comment.write('\n')
    for yBin in range(mean.GetNbinsY()):
        s=mean.GetYaxis().GetBinLabel(yBin+1)
        l=[]
        for xBin in range(16):
            l.append(round(mean.GetBinContent(xBin+1,yBin+1),2))
        comment.write(s+'='+str(l)+'\n')

    pic=SE(top, 'PIC')
    attachName(pic)
    file=SE(pic, 'FILE')
    file.text='BadBumps.png'
    c.SetLogy(True)
    badBumps.Draw()
    c.SaveAs(outputDir+'/'+file.text)
    c.SetLogy(False)
    txt=SE(pic, 'TXT')
    txt.text='BadBumps.txt'
    comment=open(outputDir+'/'+txt.text,'w')
    comment.write('\nnBadBumpsXRay='+str(bb))
    part=SE(pic,'PART')
    part.text='sidet_p'

    inefficiency=inputFile.Get('Ineffiency')  #mis-spelled to match example input
    pic=SE(top, 'PIC')
    attachName(pic)
    file=SE(pic, 'FILE')
    file.text='Inefficiency.png'
    inefficiency.Draw('COLZ')
    c.SaveAs(outputDir+'/'+file.text)
    txt=SE(pic, 'TXT')
    txt.text='Inefficiency.txt'
    comment=open(outputDir+'/'+txt.text,'w')
    comment.write('\n')
    
    inefficiencies=[]; fluxes=[]
    for xBin in range(inefficiency.GetNbinsX()):
        for yBin in range(inefficiency.GetNbinsY()):
            if inefficiency.GetBinContent(xBin,yBin)>0:
                inefficiencies.append(round(inefficiency.GetYaxis().GetBinCenter(yBin),3))
                fluxes.append(round(inefficiency.GetBinContent(xBin,yBin),2))
                continue
    comment.write('inefficiency='+str(inefficiencies)+'\n')
    comment.write('flux='+str(fluxes))
    part=SE(pic,'PART')
    part.text='sidet_p'


################################################################

def makeXML(inputFile):
    
    global moduleName
    moduleName=os.path.basename(inputFile).split('.')[0]
    inputFile=TFile(inputFile)

    global outputDir
    outputDir+='/'+moduleName
    if os.path.exists(outputDir):
        print 'WARNING: outputDir exists'
        #exit()
    else:
        print outputDir
        os.makedirs(outputDir)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    global top
    top=Element('ROOT')
    top.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')

    analyze(inputFile, outputDir)
        
    output=open(outputDir+'/master.xml','w')
    output.write(prettify(top))
    output.close()

    #print
    #print prettify(top)
    #print

    os.chdir(outputDir)
    zip=zipfile.ZipFile('../'+moduleName+'.zip', mode='w')
    for file in glob('*'):
        zip.write(file)
    zip.close()

################################################################
################################################################
################################################################

if __name__=='__main__':
    xml=makeXML(inputFile)
