import cv2
import numpy
from scipy.cluster.vq import kmeans,vq
def quantization(a,b,k):
	m,n = a.shape
	ab = numpy.squeeze(cv2.merge((a.flatten(),b.flatten())))
	centroid,_ = kmeans(ab,k)
	qnt,_ = vq(ab,centroid)
	qnt = numpy.reshape(qnt,(m,n))
	return qnt,centroid