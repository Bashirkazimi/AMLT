import numpy
import logging
import time
import math
import random

logger = logging.getLogger(__name__)

class KMeansModel(object):
    """This class models the k-means model,
    given the data, types of inputs, k
    KMeansModel(self, data, input_types, header,k, num_iters)
    """

    def __init__(self, data, input_types, header,k, num_iters):
        """Constructor.

        :param data:
            data, in the shape of numpy array of arrays.
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
        #print self.data
        self.running_time = 0
        self.centeroids = numpy.zeros(shape= (k,len(self.data[0])) )
        self.clusters = {}
    def run(self): # function called by get_n_outliers function;
        if self.computed:
            return
        self.computed = True
        print("Run k-means")
        
        ci = 0
        myRange = random.sample(range(0, len(self.data)), self.k)
        for count in myRange:
            self.centeroids[ci] =  self.data[count] 
            ci = ci+1
        start = time.time()
        
        
        for i in range(self.num_iters):
            self.clusters = {}  
            for d in self.data:
                centeroid_index = self.get_most_similar_centeroid(d, self.centeroids)
                if centeroid_index in self.clusters:
                    self.clusters[centeroid_index] = numpy.vstack((self.clusters[centeroid_index],d))
                else:
                    self.clusters[centeroid_index] = d
            for j in range(self.k):
                if j not in self.clusters:
                    rand_num = random.sample(range(0, len(self.data)), 1)
                    self.clusters[j] = self.data[rand_num[0]]         
            add=0
            for i in range(len(self.clusters)):
                add = add+len(self.clusters[i])
            for j in range(self.k):
                cluster_mean = self.get_cluster_mean(self.clusters[j])        
                self.centeroids[j] = cluster_mean # 0 is for excluded instance ID
            
        self.running_time = time.time() - start        
        print "Regular KMeans took {} seconds!".format(time.time() - start)   
        
    def get_running_time(self):
        return self.running_time
    def get_centeroids(self): # return the centroids.
        if self.computed:
            return self.centeroids
        else:
            self.run()
        return self.centeroids    
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
    def get_most_similar_centeroid(self, data_instance, centeroids):    
        similarity = float('Inf')
        index = 0

        for c in range(len(centeroids)):
            current_similarity = self.calculate_similarity(centeroids[c],data_instance)
            if current_similarity < similarity:
                similarity = current_similarity
                cen_index = c
        return cen_index
    def get_cluster_mean(self,cluster):
        #numpy_array = numpy.array([a[1:] for a in cluster]) # exclude instance ID                
        #ret = numpy.mean(numpy_array, axis = 0)
        #ret = numpy.insert(ret,0,0) # for excluding ID
        #return ret
        return cluster.mean(axis=0)
    def calculate_similarity(self,centeroid, data_instance):
        
        total = numpy.sqrt( sum((centeroid[1:] - data_instance[1:])**2 ) )
        """    
        s = [(a-b)**2 for a,b in zip(centeroid[1:],data_instance[1:])]
        my_sum = sum(s)
        
        return math.sqrt(my_sum)
        """
        return total
    def predict(self):
        y = []
        for d in self.data:
              id = d[0]
              for i in self.clusters:
                  if self.clusters[i][0] == id:
                      y.append[i]
                      break
        return y              
