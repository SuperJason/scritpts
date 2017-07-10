import sys

myString = 'Hello World!'

print myString

#print "%s is number %d!" % ("Python", 1)

#print >> sys.stderr, 'Fatal std error: invalid input!'

#logfile = open('mylog.txt', 'a')
#print >> logfile, 'Fatal logfile error: invalid input!'
#logfile.close()

#user = raw_input('Enter login name: ')
#print 'Your login is:', user

#num = raw_input('Enter a number: ')
#print 'Doubling your number is: %d' % (int(num) * 2)

# This is comment
def foo() :
    "This is another kind of comment"
    return True

# Operator, + - * / // **
# < <= > >= == != <>
# and or not

counter = 0
miles = 1000.0
name = 'Bob'
counter = counter + 1
counter += 1
kilometers = 1.609 * miles
print '%f miles is the same as %f km' % (miles, kilometers)
print 'counter = ', counter

# int long bool float complex
# bool (True, 1; False, 0)

# String
pystr = 'Python'
iscool = 'is cool!'

print pystr[0]
print pystr[2:5]
print iscool[:2]
print iscool[3:]
print iscool[-1]
print pystr + iscool
print pystr + ' ' + iscool
print pystr * 2
print '-' * 20
pystr = '''python
is cool'''
print pystr

aList = [1, 2, 3, 4]
print aList
print aList[0]
print aList[2:]
print aList[:3]
aList[1] = 5
print aList

aTuple = ('robots', 77, 93, 'try')
#aTuple[1] = 5

aDict = {'host': 'earth'}
print aDict
aDict['port'] = 80
print aDict
print aDict.keys()
print aDict['host']
for key in aDict:
    print key, aDict[key]


num = 0.9#num = raw_input('Enter a number: ')
x = float(num)
print '"x" is %f' % (x)
if x < .0:
    print '"x" must be at least 0!'
elif x < 1.0:
    print '"x" must be at least 1!'
else:
    print '"x" must be more than 1!'

while counter > 0:
    print 'loop #%d' % (counter)
    counter -= 1

print 'I like to use the Internet for'
for item in ['e-mail', 'net-surfing', 'homework', 'chat']:
    print item,
print

abc = 'abc'
for i in range(len(abc)):
    print abc[i], '[%d]' % i

sqdEvents = [x ** 2 for x in range(8) if not x % 2]
for i in sqdEvents:
    print i

try:
#    filename = raw_input('Enter file name: ')
    fobj = open(filename, 'r')
    for eachLine in fobj:
        print eachLine,
    fobj.close()
except IOError, e:
    print 'file open error:', e
