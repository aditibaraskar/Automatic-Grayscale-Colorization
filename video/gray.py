import numpy as np
import cv2

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('gray.avi',fourcc, 24.0, (512,384))
#cap = cv2.VideoCapture('input.avi')
cap = cv2.VideoCapture('fine2.avi')
#cap.set(cv2.cv.CV_CAP_PROP_FPS,5.0)

#cap = cv2.VideoCapture(0)
i=0
while(cap.isOpened()):
	ret, frame = cap.read()
	print ret,frame
	if frame is None:
		break
	elif ret is not True:
		break
	else:
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)		
		gray = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
		cv2.imshow('frame',gray)
		out.write(gray)
		#cv2.imwrite('./frames/frame_'+str(i)+'.jpg',gray)
		i=i+1
# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()