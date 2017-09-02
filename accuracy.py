import cv2
import csv
import numpy
from scipy.cluster.vq import vq

# All image paths should be of RGB images
# centroidsPath should be a csv file of centroids
def calculateAccuracy(originalImagePath,predictedImagePath,centroidsPath):
	originalImage = cv2.imread(originalImagePath)
	predictedImage = cv2.imread(predictedImagePath)
	predicted = cv2.cvtColor(predictedImage,cv2.COLOR_BGR2LAB)
	original = cv2.cvtColor(originalImage,cv2.COLOR_BGR2LAB)
	centroids = []
	with open(centroidsPath,"r") as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			centroids.append(row)
	ans = []
	centroids = numpy.array(centroids).astype('int')
	
	l = predicted[:,:,0]
	a = predicted[:,:,1]
	b = predicted[:,:,2]
	m,n = a.shape
	ab = numpy.squeeze(cv2.merge((a.flatten(),b.flatten())))
	qnt,_ = vq(ab,centroids)
	qnt = numpy.reshape(qnt,(m,n))
	predictedAB = centroids[qnt]
	
	l = original[:,:,0]
	a = original[:,:,1]
	b = original[:,:,2]
	m,n = a.shape
	ab = numpy.squeeze(cv2.merge((a.flatten(),b.flatten())))
	qnt,_ = vq(ab,centroids)
	qnt = numpy.reshape(qnt,(m,n))
	originalAB = centroids[qnt]
	
	correct = 0
	wrong = 0
	total = 0
	for x in range(originalAB.shape[0]):
		for y in range(originalAB.shape[1]):
			if (originalAB[x][y][0]==predictedAB[x][y][0]) & (originalAB[x][y][1]==predictedAB[x][y][1]):
				correct = correct + 1
			else:
				wrong = wrong + 1
			total = total + 1
	print "Total Number of pixels : ",total
	print "Number of pixels accurately predicted : ",correct
	print "Accuracy Percentage : ",(float)(correct)/total * 100
	cv2.imshow("Original",originalImage)
	cv2.imshow("Predicted",predictedImage)
	cv2.waitKey()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	testCaseNumber = "10"
	originalImage = "./Images/"+testCaseNumber+"/2.jpg"
	outputImage = "./Images/"+testCaseNumber+"/output.jpg"
	calculateAccuracy(originalImage,outputImage,"./temp/"+testCaseNumber+"/centroids")