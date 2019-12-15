"""
K-Means Segmentation Problem
(Due date: Nov. 25, 11:59 P.M., 2019)
The goal of this task is to segment image using k-means clustering.

Do NOT modify the code provided to you.
Do NOT import ANY library or API besides what has been listed.
Hint: 
Please complete all the functions that are labeled with '#to do'. 
You are allowed to add your own functions if needed.
You should design you algorithm as fast as possible. To avoid repetitve calculation, you are suggested to depict clustering based on statistic histogram [0,255]. 
You will be graded based on the total distortion, e.g., sum of distances, the less the better your clustering is.
"""


import utils
import numpy as np
import json
import time

def find_diff(a,b):
    return np.sqrt((a-b)**2)
  
def kmeans(img,k):
    """
    Implement kmeans clustering on the given image.
    Steps:
    (1) Random initialize the centers.
    (2) Calculate distances and update centers, stop when centers do not change.
    (3) Iterate all initializations and return the best result.
    Arg: Input image;
         Number of K. 
    Return: Clustering center values;
            Clustering labels of all pixels;
            Minimum summation of distance between each pixel and its center.  
    """
    # TODO: implement this function.
    temp_img=np.copy(img)
    img_arr=np.asarray(img)
    
    
    #get uniquie values of intensities
    unique_intensities,count=np.unique(img_arr,return_counts=True)
    length_intensities=len(unique_intensities)
    #print(unique_intensities,count)
    
    #all initializations
    min_clusters=[]
    min_sum=999999999999
    #iterate all initializations
    for x in range(length_intensities): 
        for j in range(length_intensities):
            if x!=j+x and j+x<length_intensities:
                #get centroids
                centroids=[unique_intensities[x],unique_intensities[x+j]]
                #print("current centroid: ",centroids)
                prev_centroids=[]
                
                #iterate till no change in centroids-K-Means Loop
                while centroids!=prev_centroids:
                    clusters=[]
                    count_clusters=[]
                    #form an list to store clusters
                    for i in range(k):
                        clusters.append([])
                        count_clusters.append([])
                    #min distances
                    elements=0 
                    mean=0
                    #for each unique intensity value find the clusters and minimum distances
                    for i,ele in enumerate(unique_intensities):
                        cluster_sum=[]
                        flag=False
                        for centroid in centroids:
                            distance=find_diff(ele,centroid)
                            #print(distance,cluster_sum)
                            #handle same centroids
                            if distance in cluster_sum:
                                flag=True
                            else:
                                flag=False
                            cluster_sum.append(distance)
                        #assign to cluster
                        if not flag:
                            index=np.argmin(np.asarray(cluster_sum))
                        else:
                            #print("IN ELSE")
                            index=np.random.randint(0,len(cluster_sum))
                            flag=False
                            
                        #print(index,cluster_sum)
                        #index=np.argmin(np.asarray(cluster_sum))
                        elements+=count[i]*cluster_sum[index]
                        mean=count[i]*ele
                        count_clusters[index].append(count[i])
                        clusters[index].append(mean)
                    new_centroids=[]
                    for l in range(k):
                        final_mean=int(round(np.sum(np.asarray(clusters[l]))/np.sum(np.asarray(count_clusters[l]))))
                        new_centroids.append(final_mean)
                    #update centroids
                    prev_centroids=centroids
                    centroids=new_centroids
                    #print("Here: ",prev_centroids,centroids)

                #get min value of centers by comparing the distances
                if elements<min_sum:
                    min_sum=elements
                    min_clusters=centroids
                print("Current centroid:",centroids)
    
    #form the mage array with values equal to clusters indices            
    for i,element in enumerate(img):
        for j,col_element in enumerate(element):
            cluster_sum=[]
            for centroid in min_clusters:
                cluster_sum.append(find_diff(col_element,centroid))
            index=np.argmin(np.asarray(cluster_sum))
            temp_img[i][j]=index   
    #print(temp_img)
    return min_clusters,temp_img,min_sum

def visualize(centers,labels):
    """
    Convert the image to segmentation map replacing each pixel value with its center.
    Arg: Clustering center values;
         Clustering labels of all pixels. 
    Return: Segmentation map.
    """
    # TODO: implement this function.
    temp_img=np.copy(labels)
    for i,element in enumerate(labels):
        for j,col_element in enumerate(element):
            for k,val in enumerate(centers):
                
                if col_element==k:
                    temp_img[i][j]=val
    
    print(temp_img)
    t=np.asarray(temp_img)
    return t.astype(np.uint8)
     
if __name__ == "__main__":
    img = utils.read_image('lenna.png')
    k = 2

    start_time = time.time()
    centers, labels, sumdistance = kmeans(img,k)
    result = visualize(centers, labels)
    end_time = time.time()

    running_time = end_time - start_time
    print(running_time)

    centers = list(centers)
    with open('results/task1.json', "w") as jsonFile:
        jsonFile.write(json.dumps({"centers":centers, "distance":sumdistance, "time":running_time}))
    utils.write_image(result, 'results/task1_result.jpg')
