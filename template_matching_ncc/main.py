import numpy as np
import cv2
import matplotlib.pyplot as plt
from imutils.object_detection import non_max_suppression


def getOrientations(img):
    height, width = img.shape[:2]
    # get the center coordinates of the image to create the 2D rotation matrix
    center = (width/2, height/2)
    
    searchingAngles = [0,90,180,270]
    
    imgOrientations = []
    for angle in searchingAngles:
        #Matrix for rotate image around the center
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1) 
        # rotate the image using cv2.warpAffine
        rotated_image = cv2.warpAffine(src=img, M=rotate_matrix, dsize=(width, height))
        imgOrientations.append(rotated_image)
    return imgOrientations

def mixMatches(matches):
    return np.maximum.reduce(matches)
    


if __name__=='__main__':
    #1) Read images
    img = cv2.imread('base.png')
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    template_origin = cv2.imread('template.png')
    template_gray = cv2.cvtColor(template_origin,cv2.COLOR_BGR2GRAY)
    
    #2) Generate template in different directions    
    templates = getOrientations(template_gray)
    
    #3) Get the Template Matching Correlation Coefficient Normalized
    matches = list(map(lambda template: cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED),templates))
    match = mixMatches(matches)

    
    plt.imshow(match,'gray')
    plt.show()
    #4) Get coordinates of matching points using thresold
    thresh = 0.8
    (y_points, x_points) = np.where(match >= thresh)
    
    #5) Get the bounding boxes
    boxes = list()
    (height,width)= template_gray.shape
    # store co-ordinates of each bounding box
    for (x, y) in zip(x_points, y_points):
        
        # update our list of boxes
        boxes.append((x, y, x + width, y + height))
    #Filter nearby bounding boxes    
    boxes = non_max_suppression(np.array(boxes))
    print(f'There are {len(boxes)} matches')

    #6 Draw matchines
    for (x1, y1, x2, y2) in boxes:        
        # draw the bounding box on the image
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0),2)

    cv2.imshow("window", img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()