import cv2
import csv
import numpy
import os
import sys
from quant import quantization 
from getKeyPointFeatures import getKeyPointFeatures
from training import train
from prediction import predict
from sklearn.decomposition import PCA
from sklearn import preprocessing
from postProcessor import postProcess
def main_function(testCaseNumber):
	t1 = cv2.getTickCount()
	
	#Defining constants
	basePath = "./Images/"
	print "Example Number : ", testCaseNumber
	tNo = "1"
	pNo = "2"
	testCaseNumber = str(testCaseNumber)
	trainingImagePath = basePath+testCaseNumber+"/"+tNo+".jpg"
	grayscaleImagePath = basePath+testCaseNumber+"/"+pNo+"G.jpg"
	outputImagePath = basePath+testCaseNumber+"/output.jpg"
	k = 5
	try:
		os.stat("./../temp/"+testCaseNumber+"/")
	except:
		os.mkdir("./../temp/"+testCaseNumber+"/")
	#Reading Training Image
	trainingImage = cv2.imread(trainingImagePath)
	trainingImage = cv2.cvtColor(trainingImage,cv2.COLOR_BGR2LAB)
	m,n,_ = trainingImage.shape
	print "Color Quantization : "
	#Preprocessing variable from image
	l = trainingImage[:,:,0]
	a = trainingImage[:,:,1]
	b = trainingImage[:,:,2]
	
	scaler = preprocessing.MinMaxScaler()
	pca = PCA(32)

	qab,centroid = quantization(a,b,k)
	print centroid
	# with open('./../temp/'+testCaseNumber+'/centroids', 'w') as csvfile:
	# 	writer = csv.writer(csvfile)
	# 	[writer.writerow(r) for r in centroid]

	t2 = cv2.getTickCount()
	t = (t2 - t1)/cv2.getTickFrequency()
	print "Time for quantization : ",t," seconds"
	
	print "Feature extraction : "
	feat,classes = getKeyPointFeatures(l,qab)
	print "Length of feature descriptor before PCA : ",len(feat[0])
	feat = scaler.fit_transform(feat)
	feat = pca.fit_transform(feat)
	print "Length of feature descriptor after PCA : ",len(feat[0])
	
	t3 = cv2.getTickCount()
	t = (t3 - t2)/cv2.getTickFrequency()
	print "Time for feature extraction : ",t," seconds"
	
	print "Training : "
	svm_classifier = train(feat,classes,k)
	t4 = cv2.getTickCount()
	t = (t4 - t3)/cv2.getTickFrequency()
	print "Time for training: ",t," seconds"

	print "Prediction : "
	grayscaleImage = cv2.imread(grayscaleImagePath,0)
	outputImage,probabilityValues = predict(svm_classifier,grayscaleImage,centroid,scaler,pca)
	#Writing temporary objects to disk
	#Remove later
	#cv2.imwrite("./../temp/"+testCaseNumber+"/labTempOut.jpg",outputImage)
	#outputTempImageBGR = cv2.cvtColor(outputImage,cv2.COLOR_LAB2BGR)
	#cv2.imwrite("./../temp/"+testCaseNumber+"/BGRTempOut.jpg",outputTempImageBGR)
	#with open('./../temp/'+testCaseNumber+'/probVal', 'w') as csvfile:
	#	writer = csv.writer(csvfile)
	#	[writer.writerow(r) for r in probabilityValues]
		
	outputImage = postProcess(outputImage,centroid,probabilityValues)

	t5 = cv2.getTickCount()
	t = (t5 - t4)/cv2.getTickFrequency()
	print "Time for prediction : ",t," seconds"	
	t = (t5 - t1)/cv2.getTickFrequency()
	print "Total time : ",t," seconds"
	outputImage = cv2.cvtColor(outputImage,cv2.COLOR_LAB2BGR)
	trainingImage = cv2.cvtColor(trainingImage,cv2.COLOR_LAB2BGR)
	cv2.imwrite(outputImagePath,outputImage)
	cv2.imshow("Training",trainingImage)
	cv2.imshow("Original",grayscaleImage)
	cv2.imshow("Predicted",outputImage)
	cv2.waitKey()
	cv2.destroyAllWindows()
if __name__=="__main__":
	testCaseNumber = 10
	if len(sys.argv)>=1:
		testCaseNumber = sys.argv[1]
	main_function(testCaseNumber)