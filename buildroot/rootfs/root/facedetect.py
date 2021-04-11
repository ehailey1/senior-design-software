import cv2
import os
from time import perf_counter

# Open the device at the ID 0
# Use the camera ID based on
# /dev/videoID needed
#cap = cv2.VideoCapture("/dev/video0", cv2.CAP_GSTREAMER)
face_cascade = cv2.CascadeClassifier('/root/haarcascade_frontalface_default.xml')
video = cv2.VideoCapture("/dev/video1", cv2.CAP_V4L)

#Check if camera works
if not (video.isOpened()):
    print("Could not open video device")

#Commands for printing temperatures
in_temp_object_raw = "cat /sys/bus/iio/devices/iio\:device0/in_temp_object_raw"
in_temp1_object_raw = "cat /sys/bus/iio/devices/iio\:device0/in_temp1_object_raw"
# We need to set resolutions. 
# so, convert them from float to integer. 

x = 320
y = 240
video.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
video.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))

size = (x, y) 
   
# Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
result = cv2.VideoWriter('filename.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         7, size) 
time = 0
# temperature = process.read()
while True:
    #Print your fps, make sure you aren't dropping too many frames.
    dif = perf_counter() - time
    fps = "{:.2f}".format(1/dif)
    print(f'frequency = {fps} Hz')

    #Read and convert 16-bit temp value to degrees Celsius.
    temp0 = os.popen(in_temp_object_raw,'r',1)
    temp0convert = 0.02*int(temp0.read())-273.15
    temperature0 = "{:.2f}".format(temp0convert)
    # temp1 = os.popen(in_temp1_object_raw,'r',1)
    # temp1convert = 0.02*int(temp1.read())-273.15
    # temperature1 = "{:.2f}".format(temp1convert)
    # print(f'temperature one = {temperature1}\N{DEGREE SIGN}C\n')
    print(f'temperature = {temperature0}\N{DEGREE SIGN}C\n')
    
    time = perf_counter()
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
    # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            print(x)
            print(y)
    # Display
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
