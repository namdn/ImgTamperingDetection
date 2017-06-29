#!/usr/bin/python3
import sys
import os
import numpy as np

# processData.py - receives via argument a list of .dat files (as generated by separateImages.py).
# It joins all the images represented in the files, applies PCA to them (transforming its attributes),
# and then randomly divides them into two files (train.dat and test.dat) for testing and training the
# classifiers. After applying PCA, this scripts shows the relevance of each new attribute and asks how many attributes
# should be used in the output files. It uses the k'ths most relevant attributes. It also asks for the fraction
# of instances that should go on the test set.

TEST_FILE = "test.dat"
TRAIN_FILE = "train.dat"

def pca(data):
	scaled = np.apply_along_axis(lambda col : (col - np.mean(col))/np.std(col), 0, data)
	cov = np.cov(scaled, rowvar=False)
	(eigval, eigvec) = np.linalg.eig(cov)

	relevances = 100 * eigval / np.sum(eigval)
	np.set_printoptions(precision=3, suppress=True)
	
	print("Relevances: ", end='')
	print(relevances)
	return np.matmul(scaled, eigvec)

data = None

for i in range(1, len(sys.argv)):
	datafile = open(sys.argv[i], "r")
	if data is None:
		data = np.loadtxt(datafile)
	else:
		data = np.concatenate((data, np.loadtxt(datafile)))
	datafile.close()

np.random.shuffle(data)

data[:, 1:] = pca(data[:, 1:])

x = int(input("How many features should be used?\n"))

data = data[:, 0:x+1]

print("There were %d instances detected. What fraction of them should go to the TESTING set?" % data.shape[0])
TEST_FRACTION = float(input())

lim = round(TEST_FRACTION * data.shape[0])

formatStr = "%1.0f" + " %1.6f" * (data.shape[1]-1)

testFile = open(TEST_FILE, "wb")
np.savetxt(testFile, data[0:lim], fmt=formatStr)
testFile.close()

trainFile = open(TRAIN_FILE, "wb")
np.savetxt(trainFile, data[lim:], fmt=formatStr)
trainFile.close()
