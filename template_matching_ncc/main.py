import numpy as np
import cv2
import matplotlib.pyplot as plt


if __name__=='__main__':
    #1) Read images
    image = cv2.imread('upload1.jpg',0)
    template = cv2.imread('template.jpg',0)
    
    ncc = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    #cv2.imshow("window", image)
    plt.imshow(ncc,'gray')
    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()