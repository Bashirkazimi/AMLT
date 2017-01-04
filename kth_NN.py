import numpy
import logging
import time
import math

logger = logging.getLogger(__name__)

class KthNN(object):
    """This class models the kth nearest neighbour distance model,
    given the data, types of inputs, k, n
    """

    def __init__(self, data, input_types, header,k, n):
        """Constructor.

        :param data:
            data, in the shape of list of lists where rows are instances
            of data and columns are attributes of instances.
        :param input_types:
            a list indicating the types of each attribute in an instances
            of the data set, like "ordinal" or "nominal".
        :param header:
            a list containing the names of each column (for printing out info)
        :param k:
            the k in the kthNN algorithm
        :param n:
            the n in the kthNN algorirthm, how many elements to set as outlier
        """

        self.data = data
        self.input_types = input_types
        self.header = header
        self.k = k
        self.n = n
        self.top_n_outliers = numpy.zeros(shape =(n,len(self.data[0])))
        self.computed = False
        self.filtered_data = []
        self.filtered = False
        self.running_time =0
    def run(self): # function called by get_n_outliers function;
        if self.computed:
            return
        self.computed = True
        print("Run dee-kay-en")

        start = time.time()
        # top n instances to be returned as outliers
        top_n_list = []
        n = 0
        j = 0
        # iterate through instances in the dataset
        for d1 in self.data:
            # keep track of the distances to k nearest neighbours
            k_nearest = []
            k = 0 # keeps track of how many neighbours have been added 
            for d2 in self.data:
                    distance = self.calculate_distance(d1, d2)
                    if k < self.k:
                        k_nearest.append(distance) 
                        k = k+1
                    else:
                        #max_index = k_nearest.index(max(k_nearest))
                        #k_nearest[max_index] = distance
                        max_dist = max(k_nearest)
                        if max_dist > distance:
                            k_nearest.remove( max_dist )
                            k_nearest.append(distance)
            kth_distance = max(k_nearest)
            if n < self.n:
                top_n_list.append((j,d1,kth_distance))            
                n = n+1    
            else:
                n=n+1
                min_dist = float('Inf')
                index = -1 # index of instance in the top n list to be outlier
                i = 0
                for (ii,d,distance) in top_n_list:
                    if distance < min_dist:
                        min_dist = distance
                        index = i        
                    i = i+1
                if kth_distance > min_dist:    
                    top_n_list[index] = (j,d1,kth_distance)        
            j = j+1 # index of data instance in dataset
        self.running_time = time.time() - start
        print "Finding outliers using dee-kay-en took {} seconds!".format(time.time() - start)   
        self.top_n_outliers = top_n_list   
        out_data = []
        for (i,d,distance) in self.top_n_outliers:
             out_data.append(d)
        out_data2 = [d[0] for d in out_data]     
        count_data=0
        for d in self.data:
            count_data=count_data+1
            if d[0] not in out_data2:
                self.filtered_data.append(d)
        self.filtered = True  
    def get_running_time(self):
        return self.running_time     
    def calculate_distance(self, data1, data2):
        # claculate euclidean distance between data points
        total = numpy.sqrt( sum((data1[1:] - data2[1:])**2 ) )           
        return total
    def get_n_outliers(self): # return the outliers only (index in the original data, instance info, kth-distance ).
        if self.computed == False:
            self.run()
        ret = []    
        for (index,data,distance) in self.top_n_outliers:
              ret.append((index,data))  
        return ret       
    def get_headers(self): # return attribute names
        return self.header
    def filter_n_outliers(self): # return data excluding the outliers
        if self.computed == False:
            self.run()     
        return self.filtered_data                  
    def get_original_data(self):
        return self.data
    def get_k():
        return self.k 
    def get_n():
        return self.n           