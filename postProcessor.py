import cv2
import csv
import numpy
def postProcess(img,centroids,probVal,blur=15):

	l,a,b = cv2.split(img)
	a = cv2.medianBlur(a, blur)
	b = cv2.medianBlur(b, blur)
	output = cv2.merge((l,a,b))
	output = cv2.cvtColor(output,cv2.COLOR_LAB2BGR)
	return output

if __name__ == "__main__":
	no = "1"
	blur = 45
	img = cv2.imread("./temp/"+no+"/BGRTempOut.jpg")
	img = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
	probVal = []
	with open('./temp/'+no+'/probVal', 'r') as csvfile:
		reader = csv.reader(csvfile)
		for r in reader:
			probVal.append(r)
	centroids = []
	with open('./temp/'+no+'/centroids', 'r') as csvfile:
		reader = csv.reader(csvfile)
		for r in reader:
			centroids.append(r)
	centroids = numpy.array(centroids)
	centroids = centroids.astype('int32')
	probVal = numpy.array(probVal)
	probVal = probVal.astype('float')
	output = postProcess(img,centroids,probVal,blur = blur)
	output = cv2.cvtColor(output,cv2.COLOR_LAB2BGR)
	before = cv2.cvtColor(img,cv2.COLOR_LAB2BGR)
	cv2.imwrite("./Images/"+no+"/output.jpg",output)
	cv2.imshow("Before",before)
	cv2.imshow("After",output)
	cv2.waitKey()
	cv2.destroyAllWindows()