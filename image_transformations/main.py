# @author: Manuel Alejandro Aponte
# Program to find difference between two images

#Intersting resources:
#https://medium.com/analytics-vidhya/opencv-perspective-transformation-9edffefb2143

import cv2
import numpy as np

pts_source=[]


# Load image
image = cv2.imread('cards.jpg')
#image = cv2.resize(image, (400,600))
original_img= image.copy()


def draw_rectangle(action, x, y, flags, *userdata):
  # Referencing global variables 
    global pts_source,image

    if action != cv2.EVENT_LBUTTONDOWN:
        return
    len_corners=  len(pts_source)
    point = [x,y]  
    if(len_corners<3):            
        pts_source.append(point)
        draw_point(image,x,y)
    if(len_corners==3):
        pts_source.append(point)
        draw_point(image,x,y)
        print('Execute')   
        image2 = perspective_transform(original_img,np.float32(pts_source))
        cv2.imshow("window2", image2)
        #image = np.concatenate((original_img, undistorted_img), axis=1) 
         
    if(len_corners==4):
        pts_source=[]
        image= original_img.copy()
        pts_source.append(point)
        draw_point(image,x,y)
    
    
def draw_point(img,x,y):
    cv2.circle(img, (x,y), radius=5, color=(255, 0, 0), thickness=-1)
    
def get_dimensions():
    maxHeight= 712
    maxWidth = 512
    return np.float32([[0, 0], [0, maxHeight - 1], [maxWidth - 1, maxHeight - 1],[maxWidth - 1, 0]]),maxWidth,maxHeight
    
    
def perspective_transform(img,pts_source):
    
    pts_destination,maxWidth,maxHeight= get_dimensions()    
    M = cv2.getPerspectiveTransform(pts_source,pts_destination)
        
    transform_img = cv2.warpPerspective(img,M,(maxWidth,maxHeight))
    return transform_img

    
cv2.namedWindow("window")
cv2.setMouseCallback("window", draw_rectangle,image)



while True:
    # both windows are displaying the same img
    cv2.imshow("window", image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()