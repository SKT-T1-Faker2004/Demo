import os
import csv 
import numpy as np
import matplotlib.pyplot as plt

def plot(filename):
	os.chdir('/Users/ericzhou/Desktop/程序代码/Programming/Visual_Studio/Python/Projects/Lottery')
	with open(filename) as f:
		reader = csv.reader(f)
		next(reader)
		
		r1 = []; r2 = []; r3 = []; r4 = []; r5 = []; r6 = []; b1 = []
		for col in reader:
			r1.append(int(col[2])) 
			r2.append(int(col[3]))
			r3.append(int(col[4]))
			r4.append(int(col[5]))
			r5.append(int(col[6]))
			r6.append(int(col[7]))
			b1.append(int(col[8]))

	plt.subplot(111)
	plt.title("Red Odd Balls")
	l1, l3, l5, = plt.plot(r1,'ro-',r3,'yo-', r5,'go-')
	plt.legend(handles=[l1,l3,l5],labels=['r1','r3','r5'])
	plt.xlabel('Latest <--------------- Oldest') 
	plt.ylabel("Number")
	my_x_ticks = []
	my_y_ticks = np.arange(0, 35, 1)
	plt.xticks(my_x_ticks)
	plt.yticks(my_y_ticks)
	plt.show()

	plt.subplot(111)
	plt.title("Red Even Balls")
	l2, l4, l6, = plt.plot(r2,'co-',r4,'mo-',r6,'ko-')
	plt.legend(handles=[l2,l4,l6],labels=['l2','l4','l6'])
	plt.xlabel('Latest <--------------- Oldest')
	plt.ylabel("Number")
	my_x_ticks = []
	my_y_ticks = np.arange(0, 35, 1)
	plt.xticks(my_x_ticks)
	plt.yticks(my_y_ticks)
	plt.show()

	plt.subplot(111)
	plt.title("Blue Balls")
	l7, = plt.plot(b1,'bo-')
	plt.legend(handles=[l7],labels=['b1'])
	plt.xlabel('Latest <--------------- Oldest') 
	plt.ylabel("Number")
	my_x_ticks = []
	my_y_ticks = np.arange(0, 17, 1)
	plt.xticks(my_x_ticks)
	plt.yticks(my_y_ticks)
	plt.show()