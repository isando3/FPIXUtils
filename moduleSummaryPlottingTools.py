#!/usr/bin/env python
from ROOT import *
from array import array

# true dimensions of a sensor in 10^-4 m (active area + periphery)
PERIPHERY = 12.  # 1.2 mm
ROC_SIZE = 81.  # 8.1 mm 
SENSOR_WIDTH  = 8 * ROC_SIZE
SENSOR_HEIGHT = 2 * ROC_SIZE
PLOT_UNIT = 50. # fill plots in 50 um width bins
X_UNIT = int(150./PLOT_UNIT)
Y_UNIT = int(100./PLOT_UNIT)
# ROCs have 52 columns (x) and 80 rows (y)
N_COLS = 52
N_ROWS = 80
# ROC plots are 162 wide by 162 high in 50 um units
ROC_PLOT_SIZE = X_UNIT * 50 + 2 * (2 * X_UNIT)  # 50 normal cols + 2 wide ones
MODULE_X_PLOT_SIZE = 8 * ROC_PLOT_SIZE
MODULE_Y_PLOT_SIZE = 2 * ROC_PLOT_SIZE


###############################################################################                                                                                                                                                                                                              
# function to process the 16 histograms and flip bin contents of the top half
# input a set of histograms and return a flipped version of the top ones
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

# input 16 plots (one per ROC) and return one merged plot with variable bins
# fill in units of 50um to account for larger edge pixels
def makeMergedPlot(plots):

    flipTopRow(plots)

    # x bins are units of 150um (except for bigger edge pixels)
    rocBinEdgesX = [0]
    for x in range(0,X_UNIT*(N_COLS-1),X_UNIT):
        rocBinEdgesX.append(x+2*X_UNIT) # first bin is twice as wide

    # y bins are units of 100um (except for bigger edge pixels)
    rocBinEdgesY = [0]
    for y in range(0,Y_UNIT*(N_ROWS-1),Y_UNIT):
        rocBinEdgesY.append(y+Y_UNIT)

    # we want to create a plot that's 8x2 ROCs

    moduleBinEdgesX = []
    for roc in range(8):  # 0 - 7
        for edge in rocBinEdgesX:
            moduleBinEdgesX.append(edge + ROC_PLOT_SIZE*roc)
    moduleBinEdgesX.append(8 * ROC_PLOT_SIZE)  # add final bin by hand

    moduleBinEdgesY = []
    # add bottom row of rocs
    for edge in rocBinEdgesY:
        moduleBinEdgesY.append(edge)
    # add top row of rocs
    moduleBinEdgesY.append(ROC_PLOT_SIZE)  # add last bin by hand
    for edge in reversed(rocBinEdgesY):
        moduleBinEdgesY.append(2 * ROC_PLOT_SIZE - edge)

    
    # create clone of plot with new bin sizes
    plotName = plots[0].GetName().rstrip("0")
    summaryPlot = TH2D(plotName,
                       "",
                       len(moduleBinEdgesX)-1,
                       array('d',moduleBinEdgesX),
                       len(moduleBinEdgesY)-1,
                       array('d',moduleBinEdgesY))
    summaryPlot.SetStats(False)
    SetOwnership(summaryPlot, False)  # avoid going out of scope at return statement                                                                                                                                                                                                            

    # fill new histogram with contents of original plots
    # put ROC 0 at the top right, because reason

    # fill bottom row first
    for roc in range(8,16):
        plot = plots[roc]

        for x in range(1,plot.GetNbinsX()+1):
            for y in range(1,plot.GetNbinsY()+1):
                content = plot.GetBinContent(x,y)
                error = plot.GetBinError(x,y)
                summaryPlot.SetBinContent(x+N_COLS*(roc-8),y,content)
                summaryPlot.SetBinError(x+N_COLS*(roc-8),y,error)

    # fill top row second
    for roc in range(7,-1,-1):  # loop backwards so 0 is last
        plot = plots[roc]

        for x in range(1,plot.GetNbinsX()+1):
            for y in range(1,plot.GetNbinsY()+1):
                content = plot.GetBinContent(x,y)
                error = plot.GetBinError(x,y)
                summaryPlot.SetBinContent(x+N_COLS*(7-roc),y+N_ROWS,content)
                summaryPlot.SetBinError(x+N_COLS*(7-roc),y+N_ROWS,error)

    return summaryPlot

###############################################################################

# gets the global min and max
# for each ROC, finds mean & RMS
# sets global range according to global min and max
# ignores any points outside a nSigma window around the ROC mean
# returns zmin and zmax
def findZRange(plots):
    zMax = -999
    zMin = 999
    nSigma = 5

    for roc in range(16):
        plot = plots[roc].Clone()

        rocMax = plot.GetMaximum()
        rocMin = plot.GetMinimum()
        oneDPlot = TH1F("1d","1d",100,rocMin,rocMax)
        for x in range(1,plot.GetNbinsX()+1):
            for y in range(1,plot.GetNbinsY()+1):
                content = plot.GetBinContent(x,y)
                oneDPlot.Fill(content)

        mean = oneDPlot.GetMean()
        sigma = oneDPlot.GetRMS()
        oneDPlot.Delete()

        plot = plots[roc].Clone()  #reset plot
        while rocMax > mean + nSigma*sigma:
            maxBin = plot.GetMaximumBin()
            plot.SetBinContent(maxBin,-999)
            rocMax = plot.GetMaximum()
        plot = plots[roc].Clone()  #reset plot
        while rocMin < mean - nSigma*sigma:
            minBin = plot.GetMinimumBin()
            plot.SetBinContent(minBin,999)
            rocMin = plot.GetMinimum()

        if rocMax > zMax:
            zMax = rocMax
        if rocMin < zMin:
            zMin = rocMin

    return (zMin,zMax)

###############################################################################

# pass this function a plot and a list with two elements - [zMin,zMax]
def setZRange(plot, range):

    plot.SetMinimum(range[0])
    plot.SetMaximum(range[1])

###############################################################################

# input a summary merged plot and draw it on a canvas
# add axis ticks and labels
# return canvas
def setupSummaryCanvas(summaryPlot):

    canvas = TCanvas(summaryPlot.GetName(),"",-1)

    # use numbers that are factors of ROC_SIZE to avoid rounding errors
    topMargin = 2 * ROC_SIZE/3.
    bottomMargin = 2 * ROC_SIZE/3.
    leftMargin = 2 * ROC_SIZE/3.
    rightMargin = 2 * ROC_SIZE

    canvas.SetBorderMode(0)
    canvas.SetBorderSize(0)
    canvasWidth = int(SENSOR_WIDTH + leftMargin + rightMargin)
    canvasHeight = int(SENSOR_HEIGHT + topMargin + bottomMargin)
    canvas.SetCanvasSize(canvasWidth, canvasHeight)
    canvas.SetFixedAspectRatio()
    SetOwnership(canvas, False)  # avoid going out of scope at return statement

    gPad.SetBorderMode(0)
    gPad.SetBorderSize(0)
    gPad.SetLeftMargin(leftMargin/canvasWidth)
    gPad.SetRightMargin(rightMargin/canvasWidth)
    gPad.SetTopMargin(topMargin/canvasHeight)
    gPad.SetBottomMargin(bottomMargin/canvasHeight)

    summaryPlot.Draw("colz a") # in color (without axes)
    SetOwnership(summaryPlot, False)  # avoid going out of scope at return statement

    canvas.Update()
    palette = summaryPlot.GetListOfFunctions().FindObject("palette")
    palette.SetX1NDC((canvasWidth-2*rightMargin/3.)/canvasWidth)
    palette.SetX2NDC((canvasWidth-rightMargin/2.)/canvasWidth)
    palette.SetY1NDC(0.05)
    palette.SetY2NDC(0.95)
    palette.SetLabelSize(0.06)


    # START ADDING AXES

    tickLength = 7
    textBoxWidth = 20
    axisLabels = []

    # x-axis ticks
    x_start = 0

    # 8 ROCS
    for roc in range(8):
        # 5 ticks per ROC - at 0,10,20,30,40
        xoffset = 0
        for i in range(5):
            if i is 1:
                xoffset += 10 * X_UNIT + X_UNIT  # account for wider edge pixel
            elif i > 1:
                xoffset += 10 * X_UNIT
            x1 = x_start+xoffset
            x2 = (MODULE_X_PLOT_SIZE-x_start)-xoffset

            text1 = TPaveText(x1-textBoxWidth/2.,
                              -1*(tickLength + textBoxWidth + 5),
                              x1+textBoxWidth/2.,
                              -1*(tickLength + 5),
                              "NB")
            text1.AddText(str(10*i))
            axisLabels.append(text1)

            text2 = TPaveText(x2-textBoxWidth/2.,
                              MODULE_Y_PLOT_SIZE + tickLength + textBoxWidth + 5,
                              x2+textBoxWidth/2.,
                              MODULE_Y_PLOT_SIZE + tickLength + 5,
                              "NB")
            text2.AddText(str(10*i))
            axisLabels.append(text2)

            line1 = TLine()
            line2 = TLine()
            if i is 0:
                line1.DrawLine(x1,
                               tickLength/5.,
                               x1,
                               -2*tickLength)
                line2.DrawLine(x2, 
                               MODULE_Y_PLOT_SIZE - tickLength/5.,
                               x2,
                               MODULE_Y_PLOT_SIZE + 2*tickLength)
            else:
                line1.DrawLine(x1,
                               tickLength/5.,
                               x1,
                               -1*tickLength)
                line2.DrawLine(x2,
                               MODULE_Y_PLOT_SIZE - tickLength/5.,
                               x2,
                               MODULE_Y_PLOT_SIZE + 1*tickLength)

        # move to next ROC
        x_start += ROC_PLOT_SIZE

    # y-axis ticks
    # this should be easier since 80 is divisible by 10
    y_offset = 0
    for tick in range(17):

        text1 = TPaveText(-1*(tickLength + textBoxWidth + 5),
                          y_offset - textBoxWidth/2.,
                          -1*(tickLength + 5),
                          y_offset + textBoxWidth/2.,
                          "NB")
        text2 = TPaveText(MODULE_X_PLOT_SIZE + tickLength + 5,
                          y_offset - textBoxWidth/2.,
                          MODULE_X_PLOT_SIZE + tickLength + textBoxWidth + 5,
                          y_offset + textBoxWidth/2.,
                          "NB")

        if tick < 8:
            text1.AddText(str(10*tick))
            text2.AddText(str(10*tick))
        else:
            text1.AddText(str(160-10*tick))
            text2.AddText(str(160-10*tick))

        axisLabels.append(text1)
        axisLabels.append(text2)

        line1 = TLine()
        line2 = TLine()
        if tick % 8 is 0:
            line1.DrawLine(0,
                           y_offset,
                           -2 * tickLength,
                           y_offset)
            line2.DrawLine(MODULE_X_PLOT_SIZE,
                           y_offset,
                           2 * tickLength + MODULE_X_PLOT_SIZE,
                           y_offset)
        else:
            line1.DrawLine(0,
                           y_offset,
                           -1 * tickLength,
                           y_offset)
            line2.DrawLine(MODULE_X_PLOT_SIZE,
                           y_offset,
                           1 * tickLength + MODULE_X_PLOT_SIZE,
                           y_offset)
        if tick is 7 or tick is 8:
            y_offset += 10 * Y_UNIT + Y_UNIT  # account for larger edge pixels 
        else:
            y_offset += 10 * Y_UNIT


    # roc labels for bottom row
    for roc in range(8):
        rocLabel = TPaveText(ROC_PLOT_SIZE/2. + ROC_PLOT_SIZE*roc - textBoxWidth*2,
                          -(4*textBoxWidth),
                          ROC_PLOT_SIZE/2. + ROC_PLOT_SIZE*roc + textBoxWidth*2,
                          -(2*textBoxWidth),
                          "NB")
        rocLabel.AddText("C"+str(roc+8))
        axisLabels.append(rocLabel)

    # roc labels for top row
    for roc in range(8):
        rocLabel = TPaveText(ROC_PLOT_SIZE/2. + ROC_PLOT_SIZE*roc - textBoxWidth*2,
                             (4*textBoxWidth) + MODULE_Y_PLOT_SIZE,
                             ROC_PLOT_SIZE/2. + ROC_PLOT_SIZE*roc + textBoxWidth*2,
                             (2*textBoxWidth) + MODULE_Y_PLOT_SIZE,
                             "NB")
        rocLabel.AddText("C"+str(7 -roc))
        axisLabels.append(rocLabel)

    for label in axisLabels:
    
        label.SetFillColor(0)
        label.SetTextAlign(22)
        label.SetTextFont(42)
        label.Draw()
        SetOwnership(label,False)  # avoid going out of scope at return statement

    return canvas

###############################################################################

def saveCanvasToNewFile(canvas,outputFileName):

    outputFile = TFile(outputFileName, "RECREATE")
    outputFile.cd()
    canvas.Write()
    outputFile.Close()

###############################################################################

def addCanvasToFile(canvas,inputFileName,directory=""):

    outputFile = TFile(outputFileName, "UPDATE")
    outputFile.cd(directory)
    canvas.Write()
    outputFile.Close()

###############################################################################

# pass in the input file and location of relevant histogram
# return the canvas with the finished summary plot
def produceSummaryPlot(inputFileName, pathToHistogram, version=0):

    inputFile = TFile(inputFileName)                                                                                                                                                                                                
    plots = []
    
    # get plots
    for roc in range(16):
        plotPath = pathToHistogram + "_C" + str(roc) + "_V" + str(version)
        plot = inputFile.Get(plotPath)
        plotName = pathToHistogram.split("/")[1]  # remove directory from name
        plot.SetName(plotName + "_V" + str(version) + "_Summary" + str(roc))
        plots.append(plot)

    summaryPlot = makeMergedPlot(plots)
    zRange = findZRange(plots)
    setZRange(summaryPlot,zRange)

    summaryCanvas = setupSummaryCanvas(summaryPlot)
    saveCanvasToNewFile(summaryCanvas,"test2.root")

#    gROOT.GetListOfCanvases().ls()
    return summaryCanvas


#    plotPath = "Scurves/sig_scurvevcal_vcal_C" + str(roc) + "_V" + str(version)
#    plotPath = "Scurves/thr_scurveVcal_Vcal_C" + str(roc) + "_V" + str(
#    plotPath = "BumpBonding/thr_calSMap_VthrComp_C" + str(roc) + "_V" + str(version)
#    plotPath = "HighRate/hitMap_daqbbtest_C" + str(roc) + "_V" + str(version)
#    plotPath = "BB3/rescaledThr_C" + str(roc) + "_V" + str(version)
#    plotPath = "BB3/thr_calSMap_VthrComp_C" + str(roc) + "_V" + str(version)



###############################################################################

# temporary altered version of produceSummaryPlot for use in lessWeb.py
def produceLessWebSummaryPlot(inputFile, pathToHistogram, outputDir, version=0):

    plots = []
    
    # get plots
    for roc in range(16):
        plotPath = pathToHistogram + "_C" + str(roc) + "_V" + str(version)
        plot = inputFile.Get(plotPath)
        plotName = pathToHistogram.split("/")[1]  # remove directory from name
        plot.SetName(plotName + "_V" + str(version) + "_Summary" + str(roc))
        plots.append(plot)

    summaryPlot = makeMergedPlot(plots)
    zRange = findZRange(plots)
    setZRange(summaryPlot,zRange)

    summaryCanvas = setupSummaryCanvas(summaryPlot)

    outputFileName = pathToHistogram.replace("/","_")
    summaryCanvas.SaveAs(outputDir + "/" + outputFileName + ".png")
