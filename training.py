from sklearn import svm
def train(X,classes,k):
	#print len(X)
	svm_classifier = []
	for i in range(k):
		svm_classifier.append(svm.SVC(gamma=0.1))
		y = (classes==i).astype(int)
		#print y.shape
		print y
		svm_classifier[i].fit(X,y)
	return svm_classifier