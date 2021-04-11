import cv2
import os

# Open the device at the ID 0
# Use the camera ID based on
# /dev/videoID needed
#cap = cv2.VideoCapture("/dev/video0", cv2.CAP_GSTREAMER)
video = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L)

#Check if camera was opened correctly
if not (video.isOpened()):
    print("Could not open video device")


# We need to set resolutions. 
# so, convert them from float to integer. 
frame_width = int(video.get(3)) 
frame_height = int(video.get(4)) 
   
size = (frame_width, frame_height) 
   
# Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
result = cv2.VideoWriter('filename.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         5, size) 
    
while(True): 
    ret, frame = video.read() 
  
    if ret == True:  
  
        # Write the frame into the 
        # file 'filename.avi' 
        result.write(frame) 
  
        # Display the frame 
        # saved in the file 
       
  
        # Press S on keyboard  
        # to stop the process 

  
    # Break the loop 
    else: 
        break
  
# When everything done, release  
# the video capture and video  
# write objects 
video.release() 
result.release() 
    
# Closes all the frames 
cv2.destroyAllWindows() 
   
print("The video was successfully saved") 

