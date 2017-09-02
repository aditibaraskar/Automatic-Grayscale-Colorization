import numpy as np
import cv2

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 24.0, (512,384))
#cap = cv2.VideoCapture('input.avi')
cap = cv2.VideoCapture('save.avi')
cap.set(cv2.cv.CV_CAP_PROP_FPS,5.0)

#cap = cv2.VideoCapture(0)
startWriting = 0
training = 0
while(cap.isOpened()):
	ret, frame = cap.read()
	if frame is None:
		break
	elif ret is not True:
		break
	else:	
		if cv2.waitKey(1) & 0xFF == ord('a'):
			if startWriting == 0:
				startWriting = 1
			else:
				break
		cv2.imshow('frame',frame)
		if(startWriting == 1):
			out.write(frame)
			cv2.imshow('saving',frame)
		if(training < 98 and training>48):
			cv2.imwrite("training.jpg",frame)
			out.write(frame)
			training = training + 1
		else:
			training = training + 1
		

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()