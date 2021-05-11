import cv2
import os
import requests
import ledscript
import NetworkManager
from time import perf_counter
import time

#url for http post 
url = 'https://192.168.1.13:4717/TempDatas/Create'
# Open the device at the ID 0
# Use the camera ID based on /dev/videoID needed
face_cascade = cv2.CascadeClassifier('/root/haarcascade_frontalface_default.xml')
video = cv2.VideoCapture("/dev/video1", cv2.CAP_V4L)

#Check if camera works
if not (video.isOpened()):
    print("Could not open video device")

#Commands for printing temperatures
in_temp_object_raw = "cat /sys/bus/iio/devices/iio\:device0/in_temp_object_raw"
in_temp1_object_raw = "cat /sys/bus/iio/devices/iio\:device0/in_temp1_object_raw"

#Timestamps
setdate = 'date -s "2021-04-28 10:37:56"'
date = 'date "+%Y-%m-%d %T"'
getdate = os.popen(date)


# We need to set resolutions. 
# so, convert them from float to integer. 
x = 320
y = 240
video.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
video.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))

size = (x, y) 
ledstate = ledscript.connectedcolor()   

# Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
result = cv2.VideoWriter('filename.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         7, size) 



def checkconnection():
  global previousconnectionstate
  stream = os.popen('ping -c 4 google.com')
  output = stream.read()
  print(output)
  if not output: 
    print('IP unreachable')
    if previousconnectionstate == True:
      ledscript.disconnectedcolor()
      previousconnectionstate = False
      time.sleep(10)
    print("You are Disconnected") 
  else: 
    print('IP reachable')
    ledscript.connectedcolor()
    previousconnectionstate = True
    print("You are Connected")



if __name__ == "__main__":
    count = 0
    newcount = 0
    timer = 0
    previousconnectionstate = True
    time.sleep(10)
    os.popen(setdate)
    while True:
        print(previousconnectionstate)
        #Print your fps, make sure you aren't dropping too many frames.
        dif = perf_counter() - timer
        fps = "{:.2f}".format(1/dif)
        print(f'frequency = {fps} Hz')

        #Read and convert 16-bit temp value to degrees Celsius.
        temp0 = os.popen(in_temp_object_raw,'r',1)
        temp0convert = 0.02*int(temp0.read())-273.15
        temperature0 = "{:.2f}".format(temp0convert)
        print(f'temperature = {temperature0}\N{DEGREE SIGN}C\n')
        
        getdate = os.popen(date)
        readdate = getdate.read()
        thedate = readdate.replace(" ","T")
        thetime = thedate.replace("\n",'"')
        thetime = thetime.replace("\r",'')
        thetime = '"'+thetime

        timer = perf_counter()
        if count > 100:
            checkconnection()
            count = 0
        
        # Read the frame
        ret, frame = video.read()
        if ret == True:
        # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect the faces, Note: Can improve framerate by increasing min size & scale
            faces = face_cascade.detectMultiScale(
                frame,
                scaleFactor=2.0,
                minNeighbors=5,
                minSize=(40, 40),
            )
            singleshot = True;
        # Draw the bounding box around person's face
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                print(x)
                print(y)
                # print(time)
                if x:
                    myobj = {
                        "tempdDataID" : 10,
                        "temperature" : float(temperature0)*(9/5)+32,
                        "x" : int(x),
                        "y" : int(y),
                        "w" : int(w),
                        "h" : int(h),
                        # "time" : readdate.replace(" ", "T")
                        # "time" : "2021-04-28T11:28:19"
                        "time" : thetime.replace('"','')
                    }
                    try:
                        z = requests.post(url, json=myobj, verify=False, timeout=.5)
                        ledscript.bullseyecolor()
                        ledscript.bullseyecolorfade()
                        ledscript.connectedcolor()
                    except requests.Timeout:
                        if previousconnectionstate == True and newcount > 5:
                            ledscript.webunavailablecolor()
                            ledscript.connectedWAcolor()
                            newcount = 0
                        else:
                            pass
                    except requests.ConnectionError:
                        if previousconnectionstate == False and newcount > 5:
                            ledscript.webunavailablecolor()
                            ledscript.disconnectedWAcolor()
                            newcount = 0
                        else:
                            pass
                    count = 0
        newcount = newcount + 1
        count = count + 1
        if ret == True:
            result.write(frame)
        else: 
            break
        
        # Stop if escape key is pressed
        #k = cv2.waitKey(30) & 0xff
        #if k==27:
        #    break
    # Release the VideoCapture object

    video.release() 
    result.release() 
        
    # Closes all the frames 
    cv2.destroyAllWindows() 
    
    print("The video was successfully saved") 
