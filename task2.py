"""
Denoise Problem
(Due date: Nov. 25, 11:59 P.M., 2019)
The goal of this task is to denoise image using median filter.

Do NOT modify the code provided to you.
Do NOT import ANY library or API besides what has been listed.
Hint: 
Please complete all the functions that are labeled with '#to do'. 
You are suggested to use utils.zero_pad.
"""


import utils
import numpy as np
import json

def median_filter(img):
    """
    Implement median filter on the given image.
    Steps:
    (1) Pad the image with zero to ensure that the output is of the same size as the input image.
    (2) Calculate the filtered image.
    Arg: Input image. 
    Return: Filtered image.
    """
    # TODO: implement this function.
    #number of row and cols padding will, be equal to length of rows and columns minus 2 respectively
    img_arr=np.asarray(img)
    padding_rows=1
    padding_cols=1
    padded_image=utils.zero_pad(img_arr,padding_rows,padding_cols)
    #copied the padded image to a temporary variable to modify the convolution changes
    temp_array=np.copy(img_arr)
    
    for i in range(len(padded_image)-2):
        for j in range(len(padded_image[0])-2):
            #created patches of each matrices which overlap with kernel
            xmin=i
            xmax=i+3
            ymin=j
            ymax=j+3
            patch = padded_image[xmin: xmax]
            patch = [row[ymin: ymax] for row in patch]
            median=np.median(patch)
            temp_array[i][j]=median
    #print(temp_array)
    return temp_array

def mse(img1, img2):
    """
    Calculate mean square error of two images.
    Arg: Two images to be compared.
    Return: Mean square error.
    """    
    # TODO: implement this function.
    numerator_diff=0
    #print(len(img1),len(img2),len(img1[0]),len(img2[0]))
    for i in range(len(img1)):
        for j in range(len(img1[0])):
            numerator_diff+=(img1[i][j]-img2[i][j])**2
    mse=numerator_diff/(len(img1)*len(img1[0]))
    
    return mse      
    

if __name__ == "__main__":
    img = utils.read_image('lenna-noise.png')
    gt = utils.read_image('lenna-denoise.png')

    result = median_filter(img)
    error = mse(gt, result)

    with open('results/task2.json', "w") as file:
        json.dump(error, file)
    utils.write_image(result,'results/task2_result.jpg')


