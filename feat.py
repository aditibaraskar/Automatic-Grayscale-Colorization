#indexing system not cartesian x=rows y=col
import cv2
import numpy

def extractFeatures(l,x,y,surf):
	windowSize = 10
	size = (2*windowSize)**2

	m,n = l.shape
	if x >= windowSize: 
		xLeftTop = x - windowSize
	else:
		xLeftTop = 0
	if y >= windowSize:
		yLeftTop = y - windowSize
	else:
		yLeftTop = 0

	if x < m - windowSize: 
		xRightBot = x + windowSize
	else:
		xRightBot = m
	if y < n - windowSize:
		yRightBot = y + windowSize
	else:
		yRightBot = n
	
	window = l[xLeftTop:xRightBot,yLeftTop:yRightBot]
	mean = numpy.mean(window)
	variance = numpy.var(window)/1000

	octave2 = cv2.GaussianBlur(l,(0,0),1)
	octave3 = cv2.GaussianBlur(l,(0,0),2)
	kp = cv2.KeyPoint(y,x,20)
	_,descriptor = surf.compute(l,[kp])
	_,descriptor2 = surf.compute(octave2,[kp])
	_,descriptor3 = surf.compute(octave3,[kp])

	if window.shape[0]*window.shape[1]==size:
		dft = numpy.abs(numpy.fft.fft(window.flatten()))
	else:
		dft = numpy.zeros(size)

	return numpy.concatenate(([mean,variance],descriptor[0],descriptor2[0],descriptor3[0],dft))


