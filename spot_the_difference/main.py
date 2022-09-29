# @author: Manuel Alejandro Aponte
# Program to find difference between two images


import cv2
import numpy as np

def draw_circle(img,x,y,r):
    # Red color in BGR
    color = (0, 0, 255)
    #circle thickness 
    thickness = 1
    
    image = cv2.circle(img,(x,y), r, color, thickness)
    return image


def find_difference(img1,img2,verbose=False):
    # Resize images if necessary
    img1 = cv2.resize(img1, (500,300))
    img2 = cv2.resize(img2, (500,300))

    img_height = img1.shape[0]

    # Grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Gaussian Blur for noise removal
    gray1 = cv2.GaussianBlur(gray1,(5,5),0)
    gray2 = cv2.GaussianBlur(gray2,(5,5),0)


    # Find the difference between the two images
    # Calculate absolute difference between two arrays 
    diff = cv2.absdiff(gray1, gray2)
    
    thresh = cv2.threshold(diff, 5, 255, cv2.THRESH_BINARY)[1]


    # Dilation
    kernel = np.ones((5,5), np.uint8) 
    dilate = cv2.dilate(thresh, kernel, iterations=2)    

    # Get connected components and their information (location, width, height,size)   
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(dilate)   
    
    #Copy source image 
    final_img = img1.copy()
    
    #Draw a circle for each connected region
    #NOTE: [1:] for exclude background
    for stat,centroid in zip(stats[1:],centroids[1:]):
        x,y,w,h,area = stat
        cX, cY = centroid
        r = int(max(w,h)/2)
        cX= int(cX)
        cY= int(cY)
        
        draw_circle(final_img,cX,cY,r)
        
    if(verbose):
        dilate =  cv2.cvtColor(dilate, cv2.COLOR_GRAY2BGR) 
        
        img_row_1 = np.concatenate((img1, img2), axis=1) 
        img_row_2 = np.concatenate((dilate, final_img), axis=1) 
        img_gallery = np.concatenate((img_row_1, img_row_2), axis=0)
        # concatenate image Vertically        
        cv2.imshow("Gallery", img_gallery)
        
    return final_img
        

if __name__=='__main__':
    
    # Load the two images
    img1 = cv2.imread('img/city1.jpg')
    img2 = cv2.imread("img/city2.jpg")
    
    difference = find_difference(img1,img2,True)
    cv2.imshow("Differences", difference)

    cv2.waitKey(0)
    cv2.destroyAllWindows()