import numpy
import logging
import time
import math
import random
import kmeans_numpy as KM

logger = logging.getLogger(__name__)

class BisectingKMeansModel(object):
    """This class models the bisecting k-means model,
    given the data, types of inputs, k
    """

    def __init__(self, data, input_types, header,k, num_iters):
        """Constructor.

        :param data:
            data, in the shape of list of lists where rows are instances
            of data and columns are attributes of instances.
        :param input_types:
            a list indicating the types of each attribute in an instances
            of the data set, like Ordinal or Nominal.
        :param header:
            a list containing the names of each column (for printing out info)
        :param k:
            the k in the k-means algorithm
        
        """

        self.data = data
        self.input_types = input_types
        self.header = header
        self.k = k
        self.num_iters = num_iters
        self.computed = False
        self.filtered_data = []
        self.filtered = False
        self.sample_set = []
        self.running_time = 0
        self.centeroids = []*k
        self.clusters = {}
    def run(self): # function called by get_n_outliers function;
        if self.computed:
            return
        self.computed = True
        print("Run bisecting k-means")
        
       
        start = time.time()
        mydata = self.data[:]
        
        num_clusters = 0
        while num_clusters != self.k:
            kmeans = KM.KMeansModel(mydata, self.input_types, self.header,2, self.num_iters) 
            clusters = kmeans.get_clusters()
            max_length = 0
            index = 0
            for i in range(2):
                if clusters[i].ndim > 1:
                    compare_with = len(clusters[i])
                else:
                    compare_with = 1    
                if max_length < compare_with:
                    max_length = compare_with
                    index = i
            mydata = clusters[index][:]
            for i in range(2):
                if i != index:
                    self.clusters[num_clusters] = clusters[i]                        
            num_clusters += 1  
        self.running_time = time.time() - start        
        print "Bisecting KMeans took {} seconds!".format(time.time() - start)   
    
    def get_running_time(self):
        return self.running_time
    def get_headers(self): # return attribute names
        return self.header
    def get_clusters(self): # return clusters
        if self.computed == False:
            self.run()     
        return self.clusters                  
    def get_original_data(self):
        return self.data
    def get_k():
        return self.k 
    def get_num_iters():
        return self.num_iters
 