from config import *

for module in moduleNames:
    input=sorted(glob('/home/fnalpix?/ShareTestResults/'+module+'_ElComandanteTest_*/*_'+testName.capitalize()+'_*'))[-1]
    makeXML(input)
    
