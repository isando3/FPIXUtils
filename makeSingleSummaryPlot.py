#!/usr/bin/env python

from moduleSummaryPlottingTools import *
from ROOT import *

gROOT.SetBatch()

inputFile = TFile('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-2-04/BBtests_trimmed.root')

produceLessWebSummaryPlot(inputFile, 'BumpBonding/thr_calSMap_VthrComp', ".")



#canvas = produceSummaryPlot('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-2-04/BBtests_trimmed.root',
#                            'BumpBonding/thr_calSMap_VthrComp')

#canvas = produceSummaryPlot('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-2-22_ElComandanteTest_2015-06-30_14h09m_1435691373/001_FPIXTest_p17/HighRate2000s_0715.root',
#                            'HighRate/hitMap_daqbbtest')

#canvas = produceSummaryPlot('/Users/lantonel/PlotsAndTables/pXarSharedResults/P-A-2-22_ElComandanteTest_2015-06-30_14h09m_1435691373/001_FPIXTest_p17/HighRate2000s_0715.root',
#                            'Scurves/thr_scurveVcal_Vcal')


#saveCanvasToNewFile(canvas,"test3.root")
