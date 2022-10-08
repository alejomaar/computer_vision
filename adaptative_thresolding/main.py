import numpy as np
import cv2
import pandas as pd


if __name__=='__main__':
    #1) Read images
    image = cv2.imread('img/book.png',0)
    mask = cv2.imread('img/mask.png',0)
    
    
    image = cv2.GaussianBlur(image, (3, 3), 0)
    colored_portion = cv2.bitwise_or(image, image, mask = mask)
    
    thresh1 = cv2.adaptiveThreshold(colored_portion, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 7)
    
    cv2.imshow('window',thresh1)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()



