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

def modelSvm(trainingImagePath,k):
	t1 = cv2.getTickCount()
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

	return(centroid,svm_classifier,scaler,pca)