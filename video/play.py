import numpy as np
import cv2

cap = cv2.VideoCapture('fine2.avi')

while(cap.isOpened()):
    ret, frame = cap.read()

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print ret,frame
    if(frame is not None):
		cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if ret == False:
    	break
cap.release()
cv2.destroyAllWindows()