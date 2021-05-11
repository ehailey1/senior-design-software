import os

date = 'date "+%Y-%m-%d %T"'
getdate = os.popen(date)
readdate = getdate.read()
x = readdate.replace(" ", "T")
print(x)