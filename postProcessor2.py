import cv2
import csv
import numpy
from gco_python import pygco

def postProcess(img,centroids,probVal):
	m,n,_ = img.shape
	print m*n,probVal.shape,len(centroids)
	probVal = numpy.reshape(probVal,(m,n,len(centroids)))
	l = img[:,:,0]
	output_a = numpy.zeros(l.shape)
	output_b = numpy.zeros(l.shape)
	g = get_edges(l)
	output_labels = graphcut(probVal,centroids,g,l=1)	
	for i in range(m):
		for j in range(n):
			a,b = centroids[output_labels[i][j]][0],centroids[output_labels[i][j]][1]
			output_a[i][j] = a
			output_b[i][j] = b
	output_img = cv2.merge((l, numpy.uint8(output_a), numpy.uint8(output_b)))
	return output_img



def get_edges(img, blur_width=3):
		img_blurred = cv2.GaussianBlur(img, (0, 0), blur_width)
		vh = cv2.Sobel(img_blurred, -1, 1, 0)
		vv = cv2.Sobel(img_blurred, -1, 0, 1)

		#vh = vh/numpy.max(vh)
		#vv = vv/numpy.max(vv)
		
		#v = numpy.sqrt(vv**2 + vh**2)

		v = 0.5*vv + 0.5*vh
		#print('max pre-normalize: %f'%numpy.amax(v))
		# #v = v/numpy.amax(v)
		# cv2.imshow("Output",v)
		# cv2.waitKey()
		# cv2.destroyAllWindows()
		return v

def graphcut(label_costs,centroids,g,l=100):

		num_classes = len(centroids)
		#calculate pariwise potiential costs (distance between color classes)
		pairwise_costs = numpy.zeros((num_classes, num_classes))
		for ii in range(num_classes):
			for jj in range(num_classes):
				c1 = numpy.array(centroids[ii])
				c2 = numpy.array(centroids[jj])
				pairwise_costs[ii,jj] = numpy.linalg.norm(c1-c2)
		
		label_costs_int32 = (100*label_costs).astype('int32')
		pairwise_costs_int32 = (l*pairwise_costs).astype('int32')
		vv_int32 = (g).astype('int32')
		vh_int32 = (g).astype('int32')
		
		#vv_int32 = (1/numpy.clip(g,0.00001,10000)).astype('int32')
		#vh_int32 = (1/numpy.clip(g,0.00001,10000)).astype('int32')
		
		#perform graphcut optimization
		new_labels = pygco.cut_simple_vh(label_costs_int32, pairwise_costs_int32, vv_int32, vh_int32, n_iter=10, algorithm='swap') 

		#new_labels = pygco.cut_simple(label_costs_int32, pairwise_costs_int32, algorithm='swap')

		return new_labels

if __name__ == "__main__":
	tno = "10"
	img = cv2.imread("./temp/"+tno+"/labTempOut.jpg")
	#img = cv2.imread("./Images/"+tno+"/output.jpg");img = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
	probVal = []
	with open('./temp/'+tno+'/probVal', 'r') as csvfile:
		reader = csv.reader(csvfile)
		for r in reader:
			probVal.append(r)
	centroids = []
	with open('./temp/'+tno+'/centroids', 'r') as csvfile:
		reader = csv.reader(csvfile)
		for r in reader:
			centroids.append(r)
	centroids = numpy.array(centroids)
	centroids = centroids.astype('int32')
	probVal = numpy.array(probVal)
	probVal = probVal.astype('float')
	output = postProcess(img,centroids,probVal)
	output = cv2.cvtColor(output,cv2.COLOR_LAB2BGR)
	cv2.imshow("Output",output)
	cv2.waitKey()
	cv2.destroyAllWindows()