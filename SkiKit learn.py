#-*- coding: utf-8 -*-
print "Starting..."
import numpy as np
import numpy.random as rnd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as img
import scipy.ndimage.filters as filters
import pandas as pd
import os,time,seaborn as sns
from math import exp,sqrt,sin,pi,cos
import datetime as datetime

print u"Finished importing"
# plt.style.use('ggplot')
sns.set(font_scale=1.4)
sns.set_style("ticks",
	{
	'axes.grid':            True,
	'grid.linestyle':       u':',
	'legend.numpoints':     1,
	'legend.scatterpoints': 1,
	'axes.linewidth':       1,
	'xtick.direction':      'in',
	'ytick.direction':      'in',
	'xtick.major.size': 	5,
 	'xtick.minor.size': 	1.0,
	'legend.frameon':       True,
	'ytick.major.size': 	5,
 	'ytick.minor.size': 	1.0
	})


iris = sns.load_dataset('iris')

#get target array y and feature matrix X
X_iris = iris.drop('species', axis=1)
y_iris = iris['species']

"""learning lin reg"""
a=raw_input("Use lin reg? \n")
if a != "n":
	#generate some random data to fit linear
	plt.figure("Lin Reg")
	rng = np.random.RandomState(42)
	x = 10 * rng.rand(50)
	y = 1 * x - 1 + rng.randn(50)
	plt.scatter(x, y);
	#import the lin reg class... every method is a seperate class in skykit learn
	from sklearn.linear_model import LinearRegression
	#create model and parameters
	model_lin=LinearRegression(fit_intercept=True)
	#make X a matrix of size [n_samples, n_features]
	X = x[:, np.newaxis]
	#fit the data
	model_lin.fit(X, y)
	print "lin coeff: ",model_lin.coef_,model_lin.intercept_
	#create line with fitted model
	def f(x):
		return model_lin.coef_*x+model_lin.intercept_
	fit_y=map(f, x)
	plt.scatter(x,fit_y,color="r")

	"""interpolation"""
	#create new x points to test the  fit
	x_new = np.linspace(-1, 11)
	X_new = x_new[:, np.newaxis]
	#predict data
	y_fit2 = model_lin.predict(X_new)
	#plot prediction
	plt.figure("Prediction")
	plt.scatter(x, y)
	plt.plot(x_new, y_fit2);


"""Gaussian naive Bayes"""
a=raw_input("Use Naive Bayes?\n")
if a != "n":
	#generate training and testing samples 
	from sklearn.cross_validation import train_test_split
	Xtrain, Xtest, ytrain, ytest = train_test_split(X_iris, y_iris,random_state=1)
	#classify (gaussian needs no keywords/parameters)
	from sklearn.naive_bayes import GaussianNB # 1. choose model class
	model_guass = GaussianNB()                       # 2. instantiate model_guass
	model_guass.fit(Xtrain, ytrain)                  # 3. fit model_guass to data
	y_model = model_guass.predict(Xtest)             # 4. predict on new data
	#get accuracy
	from sklearn.metrics import accuracy_score
	print "score: ",accuracy_score(ytest, y_model)


"""Dimension reduction with principal component analysis (PCA)"""
a=raw_input("Use Dimensions?\n")
if a != "n":
	from sklearn.decomposition import PCA  # 1. Choose the model class
	model = PCA(n_components=2)            # 2. Instantiate the model with hyperparameters
	model.fit(X_iris)                      # 3. Fit to data. Notice y is not specified!
	X_2D = model.transform(X_iris)         # 4. Transform the data to two dimensions
	iris['PCA1'] = X_2D[:, 0]
	iris['PCA2'] = X_2D[:, 1]
	sns.lmplot("PCA1", "PCA2", hue='species', data=iris, fit_reg=False,legend=True,size=7)
	plt.subplots_adjust(left=0.15, right=0.75)
		# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


"""Clustering"""
a=raw_input("Use Clustering?\n")
if a != "n":
	from sklearn.mixture import GMM      # 1. Choose the model class
	model = GMM(n_components=3,covariance_type='full')  # 2. Instantiate the model with hyperparameters
	model.fit(X_iris)                    # 3. Fit to data. Notice y is not specified!
	y_gmm = model.predict(X_iris)        # 4. Determine cluster labels
	iris['cluster'] = y_gmm
	sns.lmplot("PCA1", "PCA2", data=iris, hue='species', col='cluster', fit_reg=False,legend_out=False);


plt.show()