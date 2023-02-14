import cv2
import numpy as np

if __name__=='__main__':
    
    # Load the two images
    img = cv2.imread("city2.jpg")
    img = cv2.resize(img, (500,300))
    
    cv2.imshow("Differences", img)


    cv2.waitKey(0)
    cv2.destroyAllWindows()