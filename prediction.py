import cv2
import numpy
from sklearn import svm
from feat import extractFeatures
import csv

def predict(svm_classifier,l,centroid,scaler,pca):
	m,n = l.shape
	qnt = []
	k = len(centroid)
	probabilityVal = []
	surfDescriptorExtractor = cv2.DescriptorExtractor_create("SURF")
	surfDescriptorExtractor.setBool('extended', True)
	next_percent = 0
	for x in range(m):
		for y in range(n):
			feat = [extractFeatures(l,x,y,surfDescriptorExtractor)]
			feat = scaler.transform(feat)
			feat = pca.transform(feat)
			ans = []
			for z in range(k):
				ans.append(svm_classifier[z].decision_function(feat)[0][0])
			probabilityVal.append(ans)
			qnt.append(numpy.where(ans==max(ans))[0][0])
			if( (float)(x*n+y)/(m*n) * 100 >= next_percent):
				print  "Percentage completed : ",next_percent,"%"
				next_percent = next_percent +1
	print "Percentage completed : 100 %"
	output = centroid[qnt]
	output = numpy.array(output)
	output = numpy.reshape(output,(m,n,2))
	a = output[:,:,0]
	b = output[:,:,1]
	a = numpy.array(a,dtype='uint8')	
	b = numpy.array(b,dtype='uint8')

	img = numpy.squeeze(cv2.merge((l,a,b)))
	probabilityVal = numpy.array(probabilityVal)
	return img,probabilityVal