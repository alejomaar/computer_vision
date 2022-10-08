import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt


def adaptativeThresolding(img, block_size=25,strength=7): 
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, strength)
    return thresh

def adaptativeMean(img, block_size=25,strength=7): 
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, strength)
    return thresh

def globalThresolding(img, thresold): 
    T, thresh = cv2.threshold(img, thresold, 255,cv2.THRESH_BINARY)
    return thresh
    
if __name__=='__main__':
    #1) Read images
    image = cv2.imread('img/book.png',0)
    mask = cv2.imread('img/mask.png',0)
    
    #2) Get ROI
    img_mask = cv2.bitwise_or(image, image, mask = mask)
    
    #3 Apply different thresolding
    adapThresold = adaptativeThresolding(img_mask,25,7)
    meanThresold = adaptativeMean(img_mask,25,7)
    globalThresold = globalThresolding(img_mask,180)
    
    #4 Show results 
    titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [image, globalThresold, meanThresold, adapThresold]
    for i in range(4):
        plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()



