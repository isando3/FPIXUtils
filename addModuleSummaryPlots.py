#!/usr/bin/env python
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--file", dest="inputFileName",
                  help="path to input file")
(arguments, args) = parser.parse_args()

if not arguments.inputFileName:
    print "please specify input file";
    sys.exit(0)

from moduleSummaryPlottingTools import *

gROOT.SetBatch()

# add together appropriate 1D plots per ROC into a single 1D summary
dictionary1D = produce1DHistogramDictionary(arguments.inputFileName)
add1DSummaryPlots(arguments.inputFileName, dictionary1D)

# arrange 2D ROC plots into a single 2D summary plot
dictionary2D = produce2DHistogramDictionary(arguments.inputFileName)
add2DSummaryPlots(arguments.inputFileName, dictionary2D)
