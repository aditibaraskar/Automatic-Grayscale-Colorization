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
from modelSvm import modelSvm

def colorVideo(trainingImagePath,VideoPath,k):

	centroid, svm_classifier, scaler, pca = modelSvm(trainingImagePath,k)
	fourcc = cv2.cv.CV_FOURCC(*'XVID')
	out = cv2.VideoWriter('output.avi',fourcc, 24.0, (512,384))
	cap = cv2.VideoCapture('gray.avi')
	startWriting = 0
	while(cap.isOpened()):
		ret, frame = cap.read()
		if frame is None:
			break
		elif ret is not True:
			break
		else:	
			frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			outputImage,probabilityValues = predict(svm_classifier,frame,centroid,scaler,pca)
			outputImage = postProcess(outputImage,centroid,probabilityValues)
			out.write(outputImage)
			cv2.imshow('Colored',outputImage)
	cap.release()
	out.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	colorVideo('./fine.jpg','whatever',10)