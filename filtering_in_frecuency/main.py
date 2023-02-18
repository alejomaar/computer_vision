import cv2
import numpy as np
import matplotlib.pyplot as plt
from filter.low_pass import LowPass
from filter.high_pass import HighPass


def apply_fft(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)    
    return fshift

def apply_ifft(fshift):
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    return img_back
    
#magnitude_spectrum = 20*np.log(np.abs(fshift))

def start():
    img = cv2.imread("city.jpg",0)
    img = cv2.resize(img, (500,300))
    h,w =  img.shape
       
    fshift =  apply_fft(img)
    
    low_pass = LowPass(h,w)
    high_pass = HighPass(h,w)
    
    mask = high_pass.ideal(20)
    
    fshift_edit = np.multiply(fshift,mask) 
    
    img_back = apply_ifft(fshift_edit)
    
    plt.imshow(img_back, cmap = 'gray')
    plt.show()

if __name__=='__main__':    
    start()
    
    #cv2.imshow("img", img)


    #cv2.waitKey(0)
    #cv2.destroyAllWindows()