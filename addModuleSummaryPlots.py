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

dictionary = produceHistogramDictionary(arguments.inputFileName)
addSummaryPlots(arguments.inputFileName, dictionary)
