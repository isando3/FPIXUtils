from ROOT import *

def makeIVPlot(log):

  values=[]
    for line in input:
        if line[0]=='#': continue
        values.append([abs(float(line.split()[0])),float(line.split()[1])])
  
  nBins=len(values)
  xMin=values[0][0]
  xMax=values[-1][0]
  binWidth=float(xMax-xMin)/(nBins-1)
  xMin-=binWidth/2
  xMax+=binWidth/2

  h=TH1F('IV',';-U [V];-I [#muA]',nBins,xMin,xMax)
  for i in range(len(values)): h.SetBinContent(i+1, -1*values[i][1])
  h.SetMaximum(5*h.GetMaximum())

  return h
