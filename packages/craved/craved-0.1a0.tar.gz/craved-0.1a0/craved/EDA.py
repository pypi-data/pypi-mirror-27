"""Exploratory Data Analysis (EDA) - Clustering Toolkit
Authors : R.Mukesh, Nitin Shravan (BuddiHealth Technologies)

Dependencies: numpy, sklearn, pandas, matplotlib, hdbscan, seaborn, gapkmean(source included), h5py
version : Python 3.0

TODO : 	[1]	Hierarchial Clustering Techniques and associated metrics
		[2]	Check consistency of formula with use euclidean_distance(squared=True/False) 
"""

import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

import seaborn as sns

from sklearn.cluster import DBSCAN
from hdbscan import HDBSCAN
from sklearn.cluster import KMeans

from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from math import pow,floor

#downloaded source -- pip didn't work 
import gap

import pandas as pd
from sklearn.preprocessing import LabelEncoder,StandardScaler

#from itertools import combinations
import matplotlib.patches as mpatches

import h5py
import pickle

from time import time
#import warnings

from sklearn.neighbors import kneighbors_graph
from scipy.sparse.csgraph import laplacian

class EDA:
	def __init__(self,force_file=True,location="HOOD/"):
		"""
		Note: Don't miss '/' at the end of location string
		"""
		self.hdf5_file = None

		if force_file:
			print("Enter filename (without .hdf5)")
			self.filename = location+input().strip()+".hdf5"

			#Note: default file mode : 'a' (Read/write if exists, create otherwise)
			self.hdf5_file = h5py.File(self.filename,libver='latest')

	def load_data(self,data,labels=None):
		"""Load data externally processed in python into the EDA object
		
		keyword arguments --
		data -- Data matrix (dtype : np.array)
		labels -- Ground Truth Labels (if available)
		"""
		self.data=np.array(data)
		self.n_samples=self.data.shape[0]
		self.n_features=self.data.shape[1]

		if labels is not None:
			self.class_labels = labels

	'''
	#reads data matrix
	def read_data(self,filename,offset_top=1,offset_left=1,sep='\t'):

		data=[]
		line_number=0
		with open(filename,encoding="utf-8") as data_file:
			for line in data_file:
				line_number+=1

				if line_number > offset_top:
					data.append([float(x) for x in line.strip().split(sep)[offset_left:]])
		self.data=np.array(data)

		self.n_samples=self.data.shape[0]
		self.n_features=self.data.shape[1]
	'''

	def read_data(self,file_path,sep=',',header=None,label_cols=-1,normalize_labels=False,na_values=None):
		"""Read data and ground truth labels as an array from a file

		Keyword arguments -- 
		file_path -- corresponds to 'filepath_or_buffer' argument of pandas.read_csv()
		sep -- corresponds to 'sep' argument of pandas.read_csv() (default : ',')
		header -- corresponds to 'header' argument of pandas.read_csv() (default : None)
		label_cols -- an array of integer of 'ground truth' label columns in the file

		Note : By default drops all data points with attributes 'NA'
		"""
		data_frame = pd.read_csv(filepath_or_buffer=file_path,sep=sep,header=header,index_col=label_cols,na_values=na_values)
		data_frame.dropna(inplace=True)
		self.data = np.array(data_frame.values)
		self.class_labels = data_frame.index

		if normalize_labels is True:

			enc = LabelEncoder()
			label_encoder = enc.fit(self.class_labels)
			#original class names
			self.class_names = label_encoder.classes_
			self.class_labels = label_encoder.transform(self.class_labels)

		self.n_samples=self.data.shape[0]
		self.n_features=self.data.shape[1]

		del data_frame

	#Dummy coding of categorical attributes
	def dummy_coding(self, columns=None, retain_original=False):
		
		if retain_original:
			self.data_original = self.data.copy()

		if columns is None:
			print("Since columns=None, All attributes will be dummy coded ...")

		#convert data from np.ndarray to pd.DataFrame
		self.data = pd.DataFrame(self.data)
		self.data = pd.get_dummies(self.data,columns=columns).values
		self.n_features = self.data.shape[1]

	def sample_data(self,size=None,filename=None):
		#default size of bag is 10% of sample
		if size is None:
			size = int(0.1*self.n_samples)

		choosen_indices = np.random.choice(np.arange(self.n_samples),size=size,replace=False)

		data = self.data[list(choosen_indices)]
		labels = self.class_labels[list(choosen_indices)]

		sampled_bag = {"data":data,"target":labels}

		if filename is not None:
			pickle.dump(sampled_bag,open("DATASETS/"+filename+".p","wb"))

		return sampled_bag

	#perform repeated sampling of the dataset with replacement and store results in file
	def repeated_sampling(self,filename,n_iterations=10,size=None):
		
		for iteration in range(n_iterations):
			self.sample_data(size=size,filename=filename+str(iteration+1))


	def standardize_data(self):
		"""Standardization of data
		Reference :	[1] https://7264-843222-gh.circle-artifacts.com/0/home/ubuntu/scikit-learn/doc/_build/html/stable/auto_examples/preprocessing/plot_scaling_importance.html
					[2] Standarisation v/s Normalization : http://www.dataminingblog.com/standardization-vs-normalization/
		
		Tested : Mean and variance of data
		"""
		self.std_scale = StandardScaler().fit(self.data)
		self.std_scale.transform(self.data,copy=False)

	#Encoding categorical attributes by multiple columns
	#code to destandardise the dataset for visulisation/ metric evaluation
	def destandardize_data(self):
		self.std_scale.inverse_transform(self.data,copy=False)

	#computes euclidean distance matrix (for all pairs of data points)
	def comp_distance_matrix(self,metric='euclidean',params={}):
		"""TODO : Metrics to be supported:
		sklearn native : ['cityblock', 'cosine', 'euclidean', 'l1', 'l2','manhattan']
		scipy.spatial distances : ['braycurtis', 'canberra', 'chebyshev', 'correlation', 'dice', 'hamming', 'jaccard', 'kulsinski', 'mahalanobis',
        'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',' sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule']
		"""
		if self.hdf5_file is None:
			#if force_file is True and hdf5 file was successfully opened ...
			self.distance_matrix=pairwise_distances(self.data,metric=metric,**params)
			#raise MemoryError('Just Debugging ...')

		else:
			print("\nForce File is enabled, using HDF5 for distance matrix ...")

			print("\nEnter 'r' to read distance matrix"
				  "\nEnter 'w' to write distance matrix"
				  "\nMode : ",end='')
			mode=input().strip()

			if mode == 'r':
				self.distance_matrix = self.hdf5_file['distance_matrix']

			elif mode == 'w':
				if 'distance_matrix' in self.hdf5_file:
					del self.hdf5_file['distance_matrix']

				self.distance_matrix = self.hdf5_file.create_dataset("distance_matrix",(self.n_samples,self.n_samples),dtype='d')

				for data_index,data_point in enumerate(self.data):
					print(data_index)
					self.distance_matrix[data_index] = pairwise_distances([data_point],self.data,metric=metric,**params)

		#self.distance_matrix = np.zeros((self.n_samples,self.n_samples),dtype=np.float32)
		#for data1_index,data2_index in combinations(range(self.n_samples),2):
		#	self.distance_matrix[data1_index][data2_index] = self.distance_matrix[data2_index][data1_index] = euclidean_distance(self.data[data1_index],self.data[data2_index])

	#TODO : arrange k-dist in increasing order and plot
	#determines dbscan parameters
	def det_dbscan_params(self,min_samples=None,plot_scale=0.02):
		"""Heuristically determine min_sample and eps value for DBSCAN algorithm by visual inspection
	
		Keyword arguments --
		min_samples - minimum number of points in a pts. esp neighbourhood to be called a core point
		plot_scale - scale to compress the x-axis of plot (points v/s kdist plot)
		
		Note: Modified to work for large and small datasets
		"""
		if min_samples is None:
			if 2*self.n_features <= self.n_samples:
				min_samples=2*self.n_features
			else:
				raise Exception("please choose a value of min_samples <= no_samples")

		kdist=np.empty(self.n_samples,dtype=np.float64)
		data_index = 0

		for src_distances in self.distance_matrix:
			print(data_index)
			'''
			
			kmin_distances=np.copy(src_distances[:min_samples])
			kmin_sorted=np.sort(kmin_distances)
			#print(kmin_distances.dtype,kmin_sorted.dtype)

			del kmin_distances

			#print(kmin_sorted)

			for distance in src_distances[min_samples:]:
				#print(distance)

				if distance < kmin_sorted[min_samples-1]:
					index=min_samples-2
					while index>=0 :
						if kmin_sorted[index] > distance :
							kmin_sorted[index+1]=kmin_sorted[index]
							index -= 1
						else:
							break

					kmin_sorted[index+1]=distance

				#print(kmin_sorted)
			'''
			#print(kmin_sorted,end="\n\n")
			kmin_sorted = np.sort(src_distances)
			kdist[data_index] = kmin_sorted[min_samples-1]
			data_index += 1

			del kmin_sorted
		
		del data_index
		
		#sort in order
		kdist.sort()	
		
		#to avoid recomputation due to improper scale 
		self.kdist=np.copy(kdist)	
	
		#plot point vs k-dist
		plt.title("Finding DBSCAN parameters (min_samples, epsilon)")
		plt.xlabel("Points ====>> ")
		plt.ylabel("K-distance (k = "+str(min_samples)+")")
		plt.grid(True)

		x_points=np.arange(0.0,self.n_samples*plot_scale,plot_scale)
		plt.plot(x_points,kdist,"k")
		plt.show()

		print("Enter estimated value of eps : ")
		eps=float(input().strip())
		
		#f['dbscan_params'] = {'min_samples':min_samples,'eps':eps,'kdist':kdist}
		self.dbscan_params={"min_samples":min_samples,"eps":eps}

	def wk_inertia_stat(self,k_max,k_min=1,step=1):
		"""Estimate number of clusters by ELBOW METHOD
		
		References: 	[1]	Estimating the number of clusters in a data set via the gap statistic
					Tibshirani, Robert Walther, Guenther Hastie, Trevor
			    	[2] 	'ClusterCrit' for R library Documentation
		"""
		Wk_array = np.empty( floor((k_max-k_min)/step)+1 , dtype=np.float64 )
		inertia_array = np.empty( floor((k_max-k_min)/step)+1 , dtype=np.float64)

		#run kmeans and compute log(wk) for all n_clusters
		index = 0
		for no_clusters in range(k_min,k_max+1,step):

			kmeans_clusterer=KMeans(n_clusters=no_clusters)
			kmeans_clusterer.fit(self.data)

			Dr=np.zeros(no_clusters)
			#unique,Nr=np.unique(kmeans_clusterer.labels_,return_counts=True)
			#del unique

			#TODO: ensure that no cluster has zero points
			Nr = np.bincount(kmeans_clusterer.labels_)
			'''
			for i in range(self.n_samples-1):
				for j in range(i+1,self.n_samples):
					if kmeans_clusterer.labels_[i]==kmeans_clusterer.labels_[j]:
						Dr[kmeans_clusterer.labels_[i]] += pow(self.distance_matrix[i][j],2)
			'''
			for data_index in range(self.n_samples):
				data_cluster = kmeans_clusterer.labels_[data_index]
				Dr[data_cluster] += euclidean_distance(self.data[data_index],kmeans_clusterer.cluster_centers_[data_cluster],squared=True) 

			Wk=np.sum(Dr/2)
			Wk_array[index]=Wk
			inertia_array[index]=kmeans_clusterer.inertia_*100
			index += 1

			del kmeans_clusterer,Dr,Nr,Wk

			print("completed for K=",no_clusters)

		plt.title("Wk vs n_clusters")
		plt.xlabel("n_clusters")
		plt.ylabel("Wk")
		plt.grid(True)

		plt.plot(np.arange(k_min,k_max+1,step),Wk_array,"k")
		plt.show()

		plt.title("INTERIA TO FIND NUMBER OF CLUSTERS")
		plt.xlabel("n_clusters")
		plt.ylabel("inertia")

		plt.plot(np.arange(k_min,k_max+1,step),inertia_array,"k")
		plt.show()

	#TODO : determine the number of clusters by analysing the eigen-values of the Laplacian of Affinity Matrix
	#def eigengap(self, k_max, affinity='rbf', gamma=None, n_neighbors=10):
		"""Determine the no. of clusters by analysing the points in eigen-space
		
		References :	[1] Introduction to spectral clustering - Denis Hamad, Philippe Biela (Slide 29)
		"""
		

	#find no. of clusters - gap statistics
	def gap_statistics(self,k_max,k_min=1):
		"""Library used : gapkmeans (downloaded source : https://github.com/minddrummer/gap)
		GAP_STATISTICS : Correctness to be checked ...
		"""
		#refs=None, B=10
		gaps,sk,K = gap.gap.gap_statistic(self.data,refs=None,B=10,K=range(k_min,k_max+1),N_init = 10)
		
		plt.title("GAP STATISTICS")
		plt.xlabel("n_clusters")
		plt.ylabel("gap")

		plt.plot(K,gaps,"k",linewidth=2)
		plt.show()

	#gather results  by performing dbscan
	def perform_dbscan(self):
		'''
		TODO : use ELKI's DBSCAN algorithm instead of scikit learns algorithm
		Reference : https://stackoverflow.com/questions/16381577/scikit-learn-dbscan-memory-usage
		'''
		dbscan_clusterer=DBSCAN(**self.dbscan_params,metric="precomputed")
		dbscan_clusterer.fit(self.distance_matrix,hdf5_file=self.hdf5_file)
		self.dbscan_results={"parameters":dbscan_clusterer.get_params(),"labels":dbscan_clusterer.labels_,"n_clusters":np.unique(dbscan_clusterer.labels_).max()+1,'clusters':label_cnt_dict(dbscan_clusterer.labels_)}		

		print_dict(self.dbscan_results)

	def perform_hdbscan(self,min_cluster_size=15):
		hdbscan_clusterer=HDBSCAN(min_cluster_size)#,metric="precomputed")
		hdbscan_clusterer.fit(self.data)
		self.hdbscan_results={"parameters":hdbscan_clusterer.get_params(),"labels":hdbscan_clusterer.labels_,"probabilities":hdbscan_clusterer.probabilities_,"n_clusters":np.unique(hdbscan_clusterer.labels_).max()+1,'clusters':label_cnt_dict(hdbscan_clusterer.labels_)}

		print_dict(self.hdbscan_results)

	#TODO : needs to be corrected
	def perform_spectral_clustering(self, no_clusters, affinity='rbf', gamma=1.0, n_neighbors=10, pass_labels = False, n_init=10, force_manual=False):

		if force_manual:
			if not hasattr(self,"distance_matrix"):
				self.comp_distance_matrix()

			if affinity == 'rbf':
				self.affinity_matrix = np.exp(-gamma * self.distance_matrix**2)

			elif affinity == 'nearest_neighbors':
				self.affinity_matrix = kneighbors_graph(self.data,n_neighbors=n_neighbors,include_self=True).toarray()


			else:
				raise Exception("Affinity is NOT recognised as VALID ...")

			print("Computed Affinity Matrix ...")

			#laplacian matrix of graph
			lap, dd = laplacian(self.affinity_matrix, normed=True, return_diag=True)
			lap *= -1
			print("Computed Graph Laplacian ...")

			lambdas, diffusion_map = np.linalg.eigh(lap)
			print("Performed Eigen-decomposition ...")

			embedding = diffusion_map.T[(self.n_samples-no_clusters):] * dd

			#deterministic vector flip
			sign = np.sign(embedding[range(embedding.shape[0]),np.argmax(np.abs(embedding),axis=1)])
			embedding = embedding.T * sign

			if no_clusters == 2:
				visualise_2D(embedding.T[0],embedding.T[1],(self.class_labels) if pass_labels==True else None)
			
			elif no_clusters == 3:
				visualise_3D(embedding.T[0],embedding.T[1],embedding.T[2],(self.class_labels) if pass_labels==True else None)

			print("Performing K-Means clustering in eigen-space")
			kmeans_clusterer = KMeans(n_clusters=no_clusters,n_jobs=-1)
			kmeans_clusterer.fit(embedding)

			spectral_params = {"affinity":affinity, "gamma":gamma, "n_neighbors":n_neighbors, "n_init":n_init}

			self.spectral_results = {"parameters":spectral_params, "labels":kmeans_clusterer.labels_,"n_clusters":np.unique(kmeans_clusterer.labels_).max()+1,"clusters":label_cnt_dict(kmeans_clusterer.labels_)}


		else: 
			spectral_clusterer=SpectralClustering(n_clusters=no_clusters, gamma=gamma, affinity=affinity, n_neighbors=n_neighbors, n_init=n_init)
			spectral_clusterer.fit(self.data,y=(self.class_labels if pass_labels is True else None))
			self.spectral_results={"parameters":spectral_clusterer.get_params(),"labels":spectral_clusterer.labels_,"n_clusters":np.unique(spectral_clusterer.labels_).max()+1,"clusters":label_cnt_dict(spectral_clusterer.labels_)}

		print_dict(self.spectral_results)

		#gaussian kernel affinity matrix
		#self.affinity_matrix = spectral_clusterer.affinity_matrix_

	def perform_kmeans(self,no_clusters,params={'n_jobs':-1}):
		#start_time = time()
		kmeans_clusterer=KMeans(n_clusters=no_clusters,**params)
		kmeans_clusterer.fit(self.data)
		#print("-- %s seconds --"%(time()-start_time))

		self.kmeans_results={"parameters":kmeans_clusterer.get_params(),"labels":kmeans_clusterer.labels_,"n_clusters":no_clusters,'clusters':label_cnt_dict(kmeans_clusterer.labels_),"cluster_centers":kmeans_clusterer.cluster_centers_,"inertia":kmeans_clusterer.inertia_}     

		print_dict(self.kmeans_results)

	def perform_hierarchial(self,no_clusters,params={}):
		hierarchial_clusterer=AgglomerativeClustering(n_clusters=no_clusters,**params)
		hierarchial_clusterer.fit(self.data,hdf5_file=self.hdf5_file)
		
		self.hierarchial_results={"parameters":hierarchial_clusterer.get_params(),"labels":hierarchial_clusterer.labels_,"n_clusters":no_clusters,'clusters':label_cnt_dict(hierarchial_clusterer.labels_)}     

		print_dict(self.hierarchial_results)

def label_cnt_dict(labels):
	unique, counts = np.unique(labels, return_counts=True)
	return dict(zip(unique, counts))

def print_dict(dictionary):
	for key,value in dictionary.items():
		print(key,value,sep=" : ")

def visualise_2D(x_values,y_values,labels=None,class_names=None):
	"""Visualise clusters of selected 2 features"""

	sns.set_style('white')
	sns.set_context('poster')
	sns.set_color_codes()

	plot_kwds = {'alpha' : 0.5, 's' : 50, 'linewidths':0}

	frame = plt.gca()
	frame.axes.get_xaxis().set_visible(False)
	frame.axes.get_yaxis().set_visible(False)

	if labels is None:
		plt.scatter(x_values,y_values,c='b',**plot_kwds)

	else:
		pallete=sns.color_palette('dark',np.unique(labels).max()+1)
		colors=[pallete[x] if x>=0 else (0.0,0.0,0.0) for x in labels]
		plt.scatter(x_values,y_values,c=colors,**plot_kwds)
		legend_entries = [mpatches.Circle((0,0),1,color=x,alpha=0.5) for x in pallete]

		if class_names is None:
			legend_labels = range(len(pallete))

		else:
			legend_labels = ["class "+str(label)+" ( "+str(name)+" )" for label,name in enumerate(class_names)]

		plt.legend(legend_entries,legend_labels,loc='best')
		
	plt.show()


def visualise_3D(x_values,y_values,z_values,labels=None):
	"""Visualise clusters of selected 3 features -- plotly"""
	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')

	plot_kwds = {'alpha' : 0.5, 's' : 50, 'linewidths':0}

	if labels is None:
		ax.scatter(x_values,y_values,z_values,c='b',**plot_kwds)

	else:
		pallete=sns.color_palette('dark',np.unique(labels).max()+1)
		colors=[pallete[x] if x>=0 else (0.0,0.0,0.0) for x in labels]
		ax.scatter(x_values,y_values,z_values,c=colors,**plot_kwds)

	plt.show()

def euclidean_distance(vector1,vector2,squared=False):
	"""calculates euclidean distance between two vectors
	Keyword arguments:
	vector1 -- first data point (type: numpy array)
	vector2 -- second data point (type: numpy array)
	squared -- return square of euclidean distance (default: False)
	"""
	euclidean_distance=np.sum((vector1-vector2)**2,dtype=np.float64)
	if squared is False:
		euclidean_distance=np.sqrt(euclidean_distance,dtype=np.float64)
	return euclidean_distance
