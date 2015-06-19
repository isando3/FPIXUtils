import sys

header='011111111100'


bits = '' # ends when this string is seen
while True:
    i=raw_input()
    if i.strip()=='': break
    bits+=i.split('=')[1].strip()

n=bits.find(header)
if n==-1:
    print
    print 'No header found!!!'
    print
    print bits
    exit()
else:
    bits=bits[bits.find(header):]
    print
    print bits[:12],
    if bits[:12]=='011111111100': print '   (Header)'
    print bits[12:20],
    if bits[12:20]=='00000001': print '       (Event No)'
    print bits[20:28],'       (Data ID)'
    print bits[28:40],
    if bits[28:40]=='011111111110': print '   (Trailer)'
    elif bits[28:40]=='000001111110': print '   (Trailer - bits 2-5 flipped)'
    print bits[40:48],'       (Event Data)'
    print bits[48:56],'       (Stack Count)'
