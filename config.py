shifter="John Stupak"

moduleNames=["P-A-3-22",
             "M_TT_915",
             #"P-A-3-06",
             "P-A-3-34"
             ]

from datetime import datetime
time=datetime.now()

###############################3

for m in moduleNames:
    if len(m)!=8:
        raise Exception("Invalid module name")

if __name__=='__main__':
    print "Shifter:",shifter
    print "Modules:",moduleNames
    print "Time:",time
