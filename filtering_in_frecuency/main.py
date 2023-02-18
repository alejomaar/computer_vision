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
    
    type = 'ideal'
    threshold = 20
       
    fshift =  apply_fft(img)
    
    low_pass = LowPass(h,w)
    high_pass = HighPass(h,w)
    
    mask = high_pass.gaussian(10)
    
    fshift_edit = np.multiply(fshift,mask) 
    
    filtered_img = apply_ifft(fshift_edit)
    
    # Display the original image and the filtered image
    plt.subplot(131),plt.imshow(img, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(132),plt.imshow(mask, cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.subplot(133),plt.imshow(filtered_img, cmap = 'gray')
    plt.title('Filtered Image'), plt.xticks([]), plt.yticks([])
    plt.show()

if __name__=='__main__':    
    start()
    
    #cv2.imshow("img", img)


    #cv2.waitKey(0)
    #cv2.destroyAllWindows()