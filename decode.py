import sys

bits = ''

while True:
    i=raw_input()
    if i.strip()=='': break
    bits+=i.split('=')[1].strip()

bits=bits[bits.find('0'):]

# Check Header
print bits[:12],
if bits[:12]=='011111111100': 
    print '   (Header)'
else:
    print '   (Header - bits',
    for i in range(1,9):
        if bits[i]=='0':
            print i, 
    for j in range(10,12):
        if bits[j]=='1':
            print j,
    print 'flipped)'

# Check Event No
print bits[12:20],
if bits[12:20]=='00000001': print '       (Event No)'
else:
    print '       (Event No is not one!)'

# Check Data ID
print bits[20:28],'       (Data ID)'
# NEED TO TEST A TBM TO DETERMINE GOOD VALUES

# Check Trailer
print bits[28:40],
if bits[28:40]=='011111111110': print '   (Trailer)'
else:
    print '   (Trailer - bits',
    for i in range(29,36):
        if bits[i]=='0':
            print i-27,
    if bits[39]=='1':
            print '39',
    print 'flipped)'

# Check Event Info
print bits[40:50],'     (Event Info)'
if bits[40]=='1': print 'No Token Pass!'
if bits[41]=='0': print 'TBM Reset not sent'
if bits[42]=='0': print 'ROC Reset not sent'
if bits[43]=='1': print 'Sync Error'
if bits[44]=='1': print 'Sync Trigger'
if bits[45]=='1': print 'Clear Trigger Cntr'
if bits[46]=='0': print 'Cal Trigger'
if bits[47]=='1': print 'Stack Full'
if bits[48]=='1': print 'Auto Reset Sent'
if bits[49]=='1': print 'Pkam Reser Sent'



# Check Stack Count
print bits[50:56],
if bits[50:56]=='000001':print'         (Stack Count)'
else:
    print '       (Stack Count is not one!)'
