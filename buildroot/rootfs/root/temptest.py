import os

while True:
    in_temp_object_raw = "cat /sys/bus/iio/devices/iio\:device0/in_temp_object_raw"
    temp0 = os.popen(in_temp_object_raw,'r',1)
    temp0convert = (9/5)*(0.02*int(temp0.read())-273.15)+32
    temperature0 = "{:.2f}".format(temp0convert)
    print(f'temperature = {temperature0}\N{DEGREE SIGN}C\n')
