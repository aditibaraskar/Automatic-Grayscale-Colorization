import cv2
import numpy
from feat import extractFeatures
def getKeyPointFeatures(l,ab):
	m,n = l.shape
	surfDescriptorExtractor = cv2.DescriptorExtractor_create("SURF")
	surfDescriptorExtractor.setBool('extended', True)
	keyPointFeat = []
	classes = []
	numberOfKeyPoints = 5000
	for i in range(numberOfKeyPoints):
		x=numpy.random.uniform(m)
		y=numpy.random.uniform(n)
		keyPointFeat.append(extractFeatures(l,x,y,surfDescriptorExtractor))
		classes.append(ab[x][y])
	keyPointFeat = numpy.array(keyPointFeat)
	classes = numpy.array(classes)
	return keyPointFeat,classes