#!/usr/bin/env python
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--file", dest="inputFileName",
                  help="path to input file")
parser.add_option("-m", "--mode", dest="mode", default = "pxar",
                  help="supported modes are 'pxar' (which is default) and 'pos' (pixel online software)")
(arguments, args) = parser.parse_args()

if not arguments.inputFileName:
    print "please specify input file";
    sys.exit(0)

from moduleSummaryPlottingTools import *

gROOT.SetBatch()

# add together appropriate 1D plots per ROC into a single 1D summary
dictionary1D = produce1DHistogramDictionary(arguments.inputFileName, arguments.mode)
add1DSummaryPlots(arguments.inputFileName, dictionary1D, arguments.mode)

# arrange 2D ROC plots into a single 2D summary plot
dictionary2D = produce2DHistogramDictionary(arguments.inputFileName, arguments.mode)
add2DSummaryPlots(arguments.inputFileName, dictionary2D, arguments.mode)
