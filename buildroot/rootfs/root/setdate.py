import os

date = 'date "+%Y-%m-%d %T"'
getdate = os.popen(date)
readdate = getdate.read()
x = readdate.replace(" ", "T")
print(x)

currentdate = 'rdate -p time.nist.gov'
getcurrentdate = os.popen(currentdate)
y = readcurrentdate = getcurrentdate.read()
yy = y.split(' ')
print(yy[2])
