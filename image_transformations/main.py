# @author: Manuel Alejandro Aponte
# Undistort images through perspective transformation

#Intersting resources:
#https://medium.com/analytics-vidhya/opencv-perspective-transformation-9edffefb2143

import cv2
import numpy as np

#Points selected by user 
pts_source=[] #Xcoordinate,Ycoordinate

# Load image
image = cv2.imread('cards.jpg')

# Preserve the original image
original_img= image.copy()


def click_event(action, x, y, flags, *userdata):
    # Referencing global variables 
    global pts_source,image

    if action != cv2.EVENT_LBUTTONDOWN:
        return
    len_corners=  len(pts_source)
    point = [x,y]  
    
    #Draw new point in screen
    if(len_corners<3):            
        pts_source.append(point)
        draw_point(image,x,y)
        
    #Draw undistorted perspective  
    if(len_corners==3):
        pts_source.append(point)
        draw_point(image,x,y)
        image2 = perspective_transform(original_img,np.float32(pts_source))
        cv2.imshow("window2", image2)

    #Clear all points     
    if(len_corners==4):
        pts_source=[]
        image= original_img.copy()
        pts_source.append(point)
        draw_point(image,x,y)
    
    
def draw_point(img,x,y):
    cv2.circle(img, (x,y), radius=3, color=(200, 100, 0), thickness=-1)
    
def get_dimensions():
    maxHeight= 712
    maxWidth = 512
    return np.float32([[0, 0], [0, maxHeight - 1], [maxWidth - 1, maxHeight - 1],[maxWidth - 1, 0]]),maxWidth,maxHeight
    
    
def perspective_transform(img,pts_source):
    
    pts_destination,maxWidth,maxHeight= get_dimensions()    
    M = cv2.getPerspectiveTransform(pts_source,pts_destination)
        
    transform_img = cv2.warpPerspective(img,M,(maxWidth,maxHeight))
    return transform_img


if __name__=='__main__':
    #Set configuration
    cv2.namedWindow("window")
    cv2.setMouseCallback("window", click_event,image)
    
    #While for interactive mode
    while True:

        cv2.imshow("window", image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()