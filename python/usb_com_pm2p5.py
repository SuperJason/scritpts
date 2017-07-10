import serial  
import string

debug = 0

def hexShow(argv):  
  result = ''  
  hLen = len(argv)  
  for i in xrange(hLen):  
    hvol = ord(argv[i])  
    hhex = '%02x'%hvol  
    result += hhex+' '  
  print 'hexShow:',result  

t = serial.Serial('/dev/ttyUSB0', 9600)  
print t.portstr  
data = 0
data_hex = 0
buf = ''
cnt = 0
length = 0
num=0
while 1:
  data = t.read(1)
  if debug == 1:
    print '%d: %x' % (cnt,ord(data))
  if ord(data) == 0x42:
    buf = data
    cnt = 1
  elif ord(data) == 0x4d and cnt == 1 and ord(buf) == 0x42:
    buf += data
    cnt = 2
  elif cnt == 2:
    buf += data
    cnt = 3
    length = ord(data)
  elif cnt == 3:
    buf += data
    cnt = 4
    length = length * 256 + ord(data)
    if debug == 1:
      print 'length: %d' % length
  elif cnt < length:
    buf += data
    cnt += 1
  elif cnt == length and cnt != 0:
    #hexShow(buf)
    if debug == 1:
      print 'buf: %s' % buf 
      print 'buf[0]: %c' % buf[0]
    num += 1
    print '---------- %d ----------' % num
    print 'USA Std --> PM1.0[%d] -- PM2.5[%d] -- PM10[%d]' % (((ord(buf[4]) << 8) + ord(buf[5])), ((ord(buf[6]) << 8) + ord(buf[7])), ((ord(buf[8]) << 8) + ord(buf[9])))
    print 'Normal Std --> PM1.0[%d] -- PM2.5[%d] -- PM10[%d]' % (((ord(buf[10]) << 8) + ord(buf[11])), ((ord(buf[12]) << 8) + ord(buf[13])), ((ord(buf[14]) << 8) + ord(buf[15])))
    data = ''
    buf = ''
    cnt = 0
    length = 0
  else:
    data = ''
    buf = ''
    cnt = 0
    length = 0


