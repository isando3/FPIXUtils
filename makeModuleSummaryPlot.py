#!/usr/bin/env python
from ROOT import *
from array import array
import sys
from optparse import OptionParser

# options

# -v=0 - version of plot to get
# -t TEST which test to get results from
# -b bare plot (no axes or palette, canvas size = sensor size)
# -d directory within shareTestResults to look in
# -i=pxar.root input file
# --logz


### parse the command-line options

parser = OptionParser()
#parser = set_commandline_arguments(parser)

parser.add_option("-z", "--logz", action="store_true", dest="logZ", default=False,
                  help="sets the z axis to a log scale")
parser.add_option("-b", "--bare", action="store_true", dest="bareModule", default=False,
                  help="remove axes and palette - canvas will be size of sensor on wafer")
parser.add_option("-v", "--version", dest="plotVersion", default=0, 
                  help="specify which version of plots to get (default = 0)")
parser.add_option("-d", "--dir", dest="inputDir", 
                  help="input directory")
parser.add_option("-i", "--file", dest="inputFile", 
                  help="input file (default = pxar.root)")
parser.add_option("-c", "--config", dest="config", 
                  help="config file name")
parser.add_option("-t", "--test", dest="testType", 
                  help="type of plot to get (default = ?)")

(arguments, args) = parser.parse_args()

if arguments.config:
    sys.path.append(os.getcwd())
    exec("from " + re.sub (r".py$", r"", arguments.config) + " import *")



gROOT.SetBatch()
gStyle.SetOptStat(0)

# true dimensions of a sensor in 10^-4 m (active area + periphery)
SENSOR_WIDTH = 672
SENSOR_HEIGHT = 186
PERIPHERY = 12.



gStyle.SetCanvasDefH(SENSOR_HEIGHT)
gStyle.SetCanvasDefW(SENSOR_WIDTH)
gStyle.SetCanvasBorderMode(0)
gStyle.SetCanvasBorderSize(0)
gStyle.SetPadBorderMode(0)
gStyle.SetPadBorderSize(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetFrameBorderSize(0)
gStyle.SetPadColor(0)
gStyle.SetCanvasColor(0)
gStyle.SetCanvasDefX(0)
gStyle.SetCanvasDefY(0)
gStyle.SetPadTopMargin(PERIPHERY/SENSOR_HEIGHT)
gStyle.SetPadBottomMargin(PERIPHERY/SENSOR_HEIGHT)
gStyle.SetPadLeftMargin(PERIPHERY/SENSOR_WIDTH)
gStyle.SetPadRightMargin(PERIPHERY/SENSOR_WIDTH)
gStyle.SetHistTopMargin(0)
gStyle.SetTitleColor(1, "XYZ")
gStyle.SetTitleFont(42, "XYZ")
gStyle.SetTitleSize(0.1, "XYZ")
gStyle.SetTitleXOffset(1.1)
gStyle.SetTitleYOffset(1.2)
gStyle.SetTextFont(42)
gStyle.SetTextAlign(12)
gStyle.SetLabelColor(1, "XYZ")
gStyle.SetLabelFont(42, "XYZ")
gStyle.SetLabelOffset(0.007, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetLabelSize(0.0, "XYZ")
gStyle.SetAxisColor(1, "XYZ")
gStyle.SetStripDecimals(True)
gStyle.SetTickLength(-0.02, "XYZ")
gStyle.SetTickLength(0.0, "XYZ")
gStyle.SetNdivisions(509, "XYZ")
gStyle.SetPadTickX(0)
gStyle.SetPadTickY(0)
gROOT.ForceStyle()


colors = [kBlack,kRed,kGreen,kBlue]

#input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/M_LL_915/NoiseScan.root')
#input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-03-36/NoiseScan.root')
#input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-03-34/NoiseScan.root')


#FR 911
#input=TFile('/Users/lantonel/Xcross_Calibration_Results/robert/n00902data/bbond40_0417.root')

#RR 911
#input=TFile('/Users/lantonel/Xcross_Calibration_Results/robert/n00901data/bbond40_0422.root')

#LL 914
#input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-03-42/BBtesting.root')

#LL 915
#input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/M_LL_915/pxar_20150417_161149.root')

#TT 915
#input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-03-36/pxar_20150421_114558.root')

#FR 915
#input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-3-34/pxar.root')
input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-3-34/pxar_20150422_172026.root')

#CR 915
#input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-3-43/pxar.root')

#RR 915
#input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-2-42/pxar.root')

#FR 902 (x-rays)
#input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/M_FR_902_400V/FluxTest_Total.root')

#LL 914 (x-rays)
#input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-3-42/HR_08mA_40Hz_10sOK.root')


#TT 915 
#input=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-3-36/ROCAlignmentTest_BB3.root')
#input2=TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-3-36/ROCAlignmentTest_SCurves.root')


###############################################################################

# splits plots into two distributions of odd/even column
def makeColumnPlots(plots):

    outputFile = TFile("doubleColumnPlots.root", "RECREATE")
    outputFile.cd()

    for roc in range(16):
        plot = plots[roc]

        legend = TLegend(0.7181208,0.6945899,0.9496644,0.9441536)
        plot_name = "DoubleColumnSplit_C" + str(roc)
        oneDPlot = TH1F(plot_name,plot_name,255,0,255)
        oneDEvenPlot = TH1F("1deven","1deven",255,0,255)
        oneDOddPlot = TH1F("1dodd","1dodd",255,0,255)
        for x in range(1,plot.GetNbinsX()+1):
            for y in range(1,plot.GetNbinsY()+1):
                content = plot.GetBinContent(x,y)
                oneDPlot.Fill(content)
                if (x-1)%2 == 0:
                    oneDEvenPlot.Fill(content)
                else:
                    oneDOddPlot.Fill(content)                    

        mean = oneDPlot.GetMean()
        sigma = oneDPlot.GetRMS()

        plot_name = "DoubleColumnSplit_C" + str(roc)
        canvas = TCanvas(plot_name,"",-1)

        oneDPlot.SetLineWidth(6)
        oneDEvenPlot.SetLineWidth(2)
        oneDOddPlot.SetLineWidth(2)
        oneDEvenPlot.SetLineColor(kRed)
        oneDOddPlot.SetLineColor(kBlue)
        
        legend.AddEntry(oneDEvenPlot,"even columns")
        legend.AddEntry(oneDOddPlot,"odd columns")
        legend.AddEntry(oneDPlot,"all columns")
        
        oneDPlot.Draw()
        oneDEvenPlot.Draw("same")
        oneDOddPlot.Draw("same")
        legend.Draw()
        canvas.Write()

        oneDPlot.Delete()
        oneDEvenPlot.Delete()
        oneDOddPlot.Delete()

    outputFile.Close()


#        oneDPlot.Delete()
    


###############################################################################


# subtracts out the double-column variations
def doSubtraction(plots,normalizations):

    for roc in range(16):

        plots[roc].Add(normalizations[roc],-1)


###############################################################################

# rescales thr plots by subtracting chip mean
def rescalePlots(plots):

    for roc in range(16):
        plot = plots[roc]

        oneDPlot = TH1F("1d","1d",255,0,255)
        for x in range(1,plot.GetNbinsX()+1):
            for y in range(1,plot.GetNbinsY()+1):
                content = plot.GetBinContent(x,y)
                oneDPlot.Fill(content)

        mean = oneDPlot.GetMean()
        sigma = oneDPlot.GetRMS()
        oneDPlot.Delete()

        
        print "******* ROC",roc
        print mean, sigma
        

        for x in range(1,plot.GetNbinsX()+1):
            for y in range(1,plot.GetNbinsY()+1):
                content = plot.GetBinContent(x,y)
                content -= mean
                content /= sigma
                plot.SetBinContent(x,y,content)
        

###############################################################################

# rescales thr plots by subtracting chip mean
def rescalePlots_DoubleColumn(plots):

    for roc in range(16):
        plot = plots[roc]

        oneDEvenPlot = TH1F("1deven","1deven",255,0,255)
        oneDOddPlot = TH1F("1dodd","1dodd",255,0,255)
        for x in range(1,plot.GetNbinsX()+1):
            for y in range(1,plot.GetNbinsY()+1):
                content = plot.GetBinContent(x,y)
                if (x-1)%2 == 0:
                    oneDEvenPlot.Fill(content)
                else:
                    oneDOddPlot.Fill(content)                    

        mean_even = oneDEvenPlot.GetMean()
        sigma_even = oneDEvenPlot.GetRMS()
        mean_odd = oneDOddPlot.GetMean()
        sigma_odd = oneDOddPlot.GetRMS()
        oneDEvenPlot.Delete()
        oneDOddPlot.Delete()

        
#        print "******* ROC",roc
#        print mean, sigma
        

        for x in range(1,plot.GetNbinsX()+1):
            for y in range(1,plot.GetNbinsY()+1):
                content = plot.GetBinContent(x,y)
                if (x-1)%2 == 0:                
                    content -= mean_even
                    content /= sigma_even
                else:
                    content -= mean_odd
                    content /= sigma_odd
                plot.SetBinContent(x,y,content)
        

###############################################################################

# fill in units of 50um to account for larger edge pixels
# return merged plot
def mergePlots(plots):
    # 100um = 2
    # 150um = 3
    # 200um = 4
    # 300um = 6

    # ROCs have 52 columns (x) and 80 rows (y)
    
    # x bins are units of 150um (except for bigger edge pixels)
    rocBinEdgesX = [0]
    for x in range(0,3*51,3):
        rocBinEdgesX.append(x+6) # first bin is 6 wide
#    rocBinEdgesX.append(162)
    # y bins are units of 100um (except for bigger edge pixels)
    rocBinEdgesY = [0]
    for y in range(0,2*79,2):
        rocBinEdgesY.append(y+2) # first bin is 2 wide
#    rocBinEdgesY.append(164)

    # ROC plots are 162 wide by 162 high
    # we want to create a plot that's 8x2 ROCs
    moduleBinEdgesX = []
    for roc in range(8):  # 0 - 7
        for edge in rocBinEdgesX:
            moduleBinEdgesX.append(edge + 162*roc)
    moduleBinEdgesX.append(1296)  # add final bin by hand
    moduleBinEdgesY = []
    for roc in range(2):  # 0 - 1
        for edge in rocBinEdgesY:
            moduleBinEdgesY.append(edge + 162*roc)
    moduleBinEdgesY.append(324)  # add final bin by hand


    # create clone of plot with new bin sizes
    summaryPlot = TH2D("summaryPlot",
                       "",
                       len(moduleBinEdgesX)-1,
                       array('d',moduleBinEdgesX),
                       len(moduleBinEdgesY)-1,
                       array('d',moduleBinEdgesY))


    # fill new histogram with contents of original plots
    # start with ROC 0 at the top right, because reason

    # fill bottom row first
    for roc in range(8,16):
        plot = plots[roc]

        for x in range(1,plot.GetNbinsX()+1):
            for y in range(1,plot.GetNbinsY()+1):
                content = plot.GetBinContent(x,y)
                error = plot.GetBinError(x,y)
                summaryPlot.SetBinContent(x+52*(roc-8),y,content)
                summaryPlot.SetBinError(x+52*(roc-8),y,error)

    # fill top row next
    for roc in range(7,-1,-1):  # loop backwards so 0 is last
        plot = plots[roc]

        for x in range(1,plot.GetNbinsX()+1):
            for y in range(1,plot.GetNbinsY()+1):
                content = plot.GetBinContent(x,y)
                error = plot.GetBinError(x,y)
                summaryPlot.SetBinContent(x+52*(7-roc),y+80,content)
                summaryPlot.SetBinError(x+52*(7-roc),y+80,error)

    summaryPlot.SetMaximum(plots[0].GetMaximum())
    summaryPlot.SetMinimum(plots[0].GetMinimum())
    summaryPlot.GetXaxis().SetAxisColor(3,0)
    summaryPlot.GetYaxis().SetAxisColor(3,0)
    return summaryPlot

###############################################################################

# input a histogram and return a flipped version
def flipTopRow(plots):
    
    for roc in range(8):

        histo = plots[roc].Clone()
        histo.SetDirectory(0)
        histo.Reset()
        nBinsX = histo.GetNbinsX()
        nBinsY = histo.GetNbinsY()
        for x in range(1,nBinsX+1):
            for y in range(1, nBinsY+1):
                content = plots[roc].GetBinContent(x,y)
                error   = plots[roc].GetBinError(x,y)
                histo.SetBinContent(nBinsX-x+1, nBinsY-y+1, content)
                histo.SetBinError(nBinsX-x+1, nBinsY-y+1, error)

        plots[roc] = histo

###############################################################################

# gets the global min and max
# for each ROC, find mean & RMS
# set global range from min(mean-nSigma*RMS) to max(mean+nSigma*RMS)
# where min() and max() operate on the set of ROCs
def setZRange(plots):
    zMax = -999
    zMin = 999
    nSigma = 1

    for roc in range(16):
        plot = plots[roc]

        currentMax = plot.GetMaximum()
        currentMin = plot.GetMinimum()
        oneDPlot = TH1F("1d","1d",100,currentMin,currentMax)
        for x in range(1,plot.GetNbinsX()+1):
            for y in range(1,plot.GetNbinsY()+1):
                content = plot.GetBinContent(x,y)
                oneDPlot.Fill(content)

        mean = oneDPlot.GetMean()
        sigma = oneDPlot.GetRMS()
        oneDPlot.Delete()

        currentMax = mean + nSigma*sigma
        currentMin = mean - nSigma*sigma
        if currentMax > zMax:
            zMax = currentMax
        if currentMin < zMin:
            zMin = currentMin


    # reset min to 0 if it's negative
    if zMin < 0:
        zMin = 0


#    # for now (for thr plots)
#    zMin = 60
#    zMax = 110

    # for now (for rescaled plots)
#    zMin = -10
#    zMax = 10
#    zMin = -2.5
#    zMax = 2.5
#    zMin = 0

    # this included the palette as well
    for plot in plots:
        plot.SetMaximum(zMax)
        plot.SetMinimum(zMin)

###############################################################################

# draws 16 plots in the appropriate places
def drawPlot(summaryPlot):

    outputFile = TFile("moduleSummaryBareBB.root", "RECREATE")
    outputFile.cd()

    # draw canvas
    canvas = TCanvas("test","",-1)
    canvas.SetCanvasSize(SENSOR_WIDTH,SENSOR_HEIGHT)
    canvas.SetFixedAspectRatio()

    canvas.Draw()
    canvas.SetLogz()
    summaryPlot.Draw("col") # in color (without palette)

    canvas.Update()
    canvas.Write()
    outputFile.Close()
    canvas.SaveAs("moduleSummaryBareBB.pdf")
#    sys.exit(0)

###############################################################################

plots = []
version = '0'

# get plots
for roc in range(16):
#    plot_name = "Scurves/sig_scurvevcal_vcal_C" + str(roc) + "_V" + str(version)
    plot_name = "Scurves/thr_scurveVcal_Vcal_C" + str(roc) + "_V" + str(version)
#    plot_name = "BumpBonding/thr_calSMap_VthrComp_C" + str(roc) + "_V" + str(version)
#    plot_name = "HighRate/hitMap_daqbbtest_C" + str(roc) + "_V" + str(version)
#    plot_name = "BB3/rescaledThr_C" + str(roc) + "_V" + str(version)
#    plot_name = "BB3/thr_calSMap_VthrComp_C" + str(roc) + "_V" + str(version)
    plot = input.Get(plot_name)
#    print plot_name
    plot.SetTitle("")
#    plots.append(input.Get(plot_name))
    plots.append(plot)




#makeColumnPlots(plots)

#doSubtraction(plots, normalizations)

#rescalePlots(plots)
#rescalePlots_DoubleColumn(plots)
flipTopRow(plots)
setZRange(plots)
summaryPlot = mergePlots(plots)
drawPlot(summaryPlot)

