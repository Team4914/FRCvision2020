import cv2 
import numpy as np

from gpiozero import LED

align = LED(5)
right = LED(6)
left = LED(13)

align.off()
right.off()
left.off()

cap = cv2.VideoCapture(0)

kernel = np.ones((5,5),np.uint16)

#80-90 86-129 255-255
#lower_target1 = np.array([82,128,255]) 
#upper_target1 = np.array([99,255 , 255])

lower_target1 = np.array([78,89,255]) 
upper_target1 = np.array([92,166 , 255])

while(1):        
    # Captures the live stream frame-by-frame 
    _, frame = cap.read()  
    # Converts images from BGR to HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, lower_target1, upper_target1)
    morph = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
    

    #try:
    contours, hierarchy = cv2.findContours(morph, 1, 2)
    if len(contours) < 1:
        continue
    
    cnt = contours[0]
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    
    print cx, " ", cy
    if cx>250 and cx<350:
        align.on()
        right.off()
        left.off()
    
    elif cx < 250:
        right.on()
        left.off()
        align.off()
    elif cx > 350:
        right.off()
        left.on()
        align.off()
    else:
        right.off()
        left.off()
        align.off()
    result = cv2.bitwise_and(frame,frame, mask= mask) 
    cv2.circle(result, (cx,cy), 10, (0,0,255), -1)
    #cv2.imshow('frame',frame)
    
    #below for debug
    cv2.imshow('mask',result)
    #cv2.imshow('result',morph) 

    k = cv2.waitKey(5) & 0xFF
    if k == 27: 
        break
  
# Destroys all of the HighGUI windows. 
cv2.destroyAllWindows() 
  
# release the captured frame 
cap.release()

