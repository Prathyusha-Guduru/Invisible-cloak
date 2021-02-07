#import necessary libraries
import cv2
import numpy as np
import time
# print("Everything clear")
#Creating VideoCapture object
cap  = cv2.VideoCapture(0)
time.sleep(3) #Giving time for the camera to warm up 

background = 0
for i in range(30):
    ret,background = cap.read() #Capturing multiple images of static background to reduce noise
    background = np.flip(background,axis=1)
while True:
    
    ret,img = cap.read()
    img = np.flip(img,axis = 1)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #Creating mask for the red colored cloth
    lower_red = np.array([0,120,70])
    upper_red  = np.array([10,255,255])
    mask1 = cv2.inRange(hsv,lower_red,upper_red)

    lower_red = np.array([170,120,70])
    upper_red  = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_red,upper_red)

    mask = mask1+mask2

    #Segmenting out the detected red colored cloth 
    mask1 = cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    mask2 = cv2.bitwise_not(mask1)

    res1 = cv2.bitwise_and(img,img,mask = mask2)
    res2 = cv2.bitwise_and(background,background,mask = mask1)

    final_output = cv2.addWeighted(res1,1,res2,1,0)
    cv2.imshow('Magic',final_output)
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()