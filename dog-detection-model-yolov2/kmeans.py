import random
import numpy as np
from iou_yolo import iou_yolo

def kmeans(data, num_clusters=5, max_iters=10):
    # CITATION: https://fairyonice.github.io/Part_1_Object_Detection_with_Yolo_for_VOC_2014_data_anchor_box_clustering.html
    # data: [[width, height]...[width, height]]
    
    # Setting Seed
    random.seed(10)
    
    # Initializing the cluster each data point belows to
    nearestClusters = np.zeros((data.shape[0],))
    newClusters = np.ones((data.shape[0],))
        
    # Setting the initial centroids
    initialCentroidIndexes = random.sample(range(0, data.shape[0]), num_clusters)
    
    # Extracting the centroids
    centroids = data[initialCentroidIndexes,:]
    
    # Defining iteration counter
    i = 0
    
    # Ending when either max_iters is reached or the clusters don't change
    while (i < max_iters) and ~np.all(nearestClusters == newClusters):
        
        # Assignment the new clusters as the all clusters
        nearestClusters = newClusters
    
        # Defining array to hold the centroid distances
        centroidDistances = np.zeros((data.shape[0], num_clusters))

        # Computing the distance to the centroids for each point
        for cluster in range(0,num_clusters):        
            centroidDistances[:,cluster] = 1 - iou_yolo(centroids[cluster,:],data)
        
        # Determining each points cluster
        newClusters = np.argmin(centroidDistances,axis=1)
        
        # Computing the new clusters by taking the mean of the width and heights respectively
        # for all points in the respective cluster
        for cluster in range(0, num_clusters):
            centroids[cluster, :] = np.mean(data[newClusters == cluster,:],axis=0)
        
        # Incrementing Counter
        i += 1
        
    # Computing each points distance to its cluster centroid
    
    centroidIOUs = np.max(np.negative(centroidDistances-1),axis=1)
    
    meanCentroidIOU = np.mean(centroidIOUs)       

    return newClusters, centroids, meanCentroidIOU, i