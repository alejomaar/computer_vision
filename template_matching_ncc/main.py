import numpy as np
import cv2
import matplotlib.pyplot as plt
from imutils.object_detection import non_max_suppression


if __name__=='__main__':
    #1) Read images
    img = cv2.imread('base.png')
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    template = cv2.imread('template.png',0)
    height,width= template.shape
    
    match = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    
    thresh = 0.9
    (y_points, x_points) = np.where(match >= thresh)
    print(len(y_points))
    boxes = list()
  
    # store co-ordinates of each bounding box
    # we'll create a new list by looping
    # through each pair of points
    for (x, y) in zip(x_points, y_points):
        
        # update our list of boxes
        boxes.append((x, y, x + width, y + height))
        
    boxes = non_max_suppression(np.array(boxes))
    print(len(boxes))

    for (x1, y1, x2, y2) in boxes:
        
        # draw the bounding box on the image
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0),2)

    cv2.imshow("window", img)
    #plt.imshow(image)
    #plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()