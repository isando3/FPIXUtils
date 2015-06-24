import sys


bits = '' # ends when this string is seen
startpt = '0'
def checkCode(reference,real):
    flipped=[j+1 for j in range(len(reference)) if reference[j]!=real[j]]
    print "bits ",
    print flipped,
    print " are flipped)"

while True:

    i=raw_input()
    if i.strip()=='': break
    bits+=i.split('=')[1].strip()


n=bits.find(startpt)
if n==-1:
    print
    print 'Something is wrong!!!'
    print
    print bits
    exit()
else:
    bits=bits[bits.find(startpt):]
    
    header = bits[:12]
    eventid = bits[12:20]
    dataid = bits[20:28]
    trailer = bits[28:40]
    eventinfo = bits[40:50]
    stackcount = bits[50:56]

#Reference
    headerref = '011111111100'
    eventidref = '00000001'
    dataidref1 = '00000000'
    dataidref2 = '01000000'
    dataidref3 = '10110000'
    dataidref4 = '11000000'
    trailerref = '011111111110'
    eventinforef = '0110001000'
    stackcountref = '000001'

    print header,
    if header == '011111111100': print '       (Header)'
    else:
        print '       (Header :', 
        checkCode(headerref,header)

    print eventid,
    if eventid==eventidref: print '           (Event No)'
    else:
        print '           (Event No :',
        checkCode(eventidref,eventid)
    print dataid,
    if dataid== dataidref1:
        print '           (Data ID)'
    elif dataid== dataidref2:
        print '           (Data ID)'
    elif dataid== dataidref3:
        print '           (Data ID)'
    elif dataid== dataidref4:
        print '           (Data ID)'
    else:
        print '           (Somthing wrong in the data id, please check the TBM documentation)'
    print trailer,
    if trailer==trailerref: print '       (Trailer)'
    else:
        print '       (Trailer :',
        checkCode(trailerref,trailer)

    print eventinfo,
    if eventinfo==eventinforef:
        print'         (Event Info)'
    elif bits[40]== '1':
        if bits[42]=='1':
            if bits[46]=='1':
                print'         (Event Info: No Token Pass Sync Error)'
            else:
                print'         (Event Info: No Token Pass and Sync Error, please reset the timing)'
        elif bits[46]=='1':
            print'         (Event Info: No Token Pass and Stack full.)'
        else:
            print'         (Event Info: No Token Pass)'
    elif bits[42]=='1':
        if bits[46]=='1':
            print'         (Event Info: Sync Error and Stack Full, please reset the timing)'
        else:
            print'         (Event Info: Sync Error, please reset the timing)'
    elif bits[46]=='1':
        print'         (Event Info: Stack Full!)'
    else:
        print '        (Event Info :',
        checkCode(eventinforef,eventinfo)
    print stackcount,
    if stackcount == stackcountref: print '             (Stack Count)'
    else:
        print '             (Stack Count :',
        checkCode(stackcountref,stackcount)

